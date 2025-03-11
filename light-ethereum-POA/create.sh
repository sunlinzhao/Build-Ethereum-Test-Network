#!/bin/bash
# /root/light-ethereum/create.sh
# 设置变量
data_dir="/root/light-ethereum/data"
network_id=123456

miner_port=8545
miner_http_port=9001

processor_port=8546
processor_http_port=9002

normal_port=8547
normal_http_port=9003

password_file="$data_dir/.passwd"  # 密码文件路径
accounts_directory="/root/light-ethereum/data/Accounts"
validators_directory="/root/light-ethereum/data/Validators"  # 验证者账户文件路径
num_file="/root/light-ethereum/node_num.txt"

# 检查文件是否存在
if [ -e "$num_file" ]; then
    # 读取文件中的数字
    read -r number < "$num_file"
else
    echo "$num_file is not exist."
fi

num_accounts=$number  # 设置创建的账户数量

accounts=()
# 检查目录是否存在
if [ ! -d "$accounts_directory" ]; then
    echo "Error: Directory $accounts_directory does not exist."
    exit 1
fi

# 遍历目录下的每个文件
for file in "$accounts_directory"/*; do
    # 检查是否是文件
    if [ -f "$file" ]; then
        echo "Reading lines from file: $file"
        
        # 逐行读取文件内容并存储到数组
        while IFS= read -r line; do
            accounts+=("$line")
        done < "$file"
        
        # 打印每个文件的内容列表
        echo "Contents of $file:"
        for content in "${lines[@]}"; do
            echo "$content"
        done
        echo "------------------------"
    fi
done

# 构建账户余额 JSON 字符串 / 24 eth
accounts_json="{"
for account in "${accounts[@]}"; do
    accounts_json+="\"$account\":{\"balance\":\"24000000000000000000\"},"
done
# 移除末尾的逗号
accounts_json="${accounts_json%,}"
accounts_json+="}"



m_accounts=()
# 检查目录是否存在
if [ ! -d "$validators_directory" ]; then
    echo "Error: Directory $validators_directory does not exist."
    exit 1
fi

# 遍历目录下的每个文件
for file in "$validators_directory"/*; do
    # 检查是否是文件
    if [ -f "$file" ]; then
        echo "Reading lines from file: $file"

        # 逐行读取文件内容并存储到数组
        while IFS= read -r line; do
            m_accounts+=("$line")
        done < "$file"

        # 打印每个文件的内容列表
        echo "Contents of $file:"
        for content in "${lines[@]}"; do
            echo "$content"
        done
        echo "------------------------"
    fi
done

# 构建账户余额 JSON 字符串 / 24 eth
m_accounts_json="{"
for account in "${m_accounts[@]}"; do
    m_accounts_json+="\"$account\":{\"balance\":\"24000000000000000000\"},"
done
# 移除末尾的逗号
m_accounts_json="${m_accounts_json%,}"
m_accounts_json+="}"
#-----------------------------------------------------------POA

# 连接 32 个零字节
extradata="0x0000000000000000000000000000000000000000000000000000000000000000"
# 将所有签名者地址连接到 extradata 中
for account in "${m_accounts[@]}"; do
  # 删除账户的前缀 "0x"，并将其转换为长度为 64 的字符串
  account_hex="${account:2}"

  # 将账户添加到 extradata 中
  extradata="${extradata}${account_hex}"
done

# 再次连接 65 个零字节
extradata="${extradata}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

# 使用 sed 删除字符串前后的大括号
trim_accounts_json=$(echo "$accounts_json" | sed 's/{\(.*\)}/\1/')
trim_m_accounts_json=$(echo "$m_accounts_json" | sed 's/{\(.*\)}/\1/')

alloc_json="{$trim_accounts_json,$trim_m_accounts_json}"

#-----------------------------------------------------------POA

# 修改创世区块配置（初始资金）
genesis_json='{
  "config": {
    "chainId": 1701,
    "homesteadBlock": 0,
    "eip150Block": 0,
    "eip155Block": 0,
    "eip158Block": 0,
    "byzantiumBlock": 0,
    "clique": {
    "period": 3,
    "epoch": 30000
  }
  },
  "difficulty": "0x1",
  "extraData": "'$extradata'",
  "gasLimit": "8000000",
  "nonce": "0x0",
  "coinbase": "0x0000000000000000000000000000000000000000",
  "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "timestamp": "0x00",
  "alloc": '$alloc_json'
}'

echo "$genesis_json"
echo "-----------------------------------"

# 输出修改后的 genesis_json
# echo "$genesis_json"

# 检查 genesis.json 文件是否存在
if [ -f "genesis.json" ]; then
    # 如果存在，删除文件
    rm genesis.json
fi

# 输出 genesis_json 到 genesis.json 文件
echo "$genesis_json" > genesis.json

echo "run miner node..."
# 初始化 genesis.json 文件
geth init --datadir $data_dir/data_miner $data_dir/../genesis.json
# 创建矿工节点
nohup geth --datadir $data_dir/data_miner --networkid $network_id --port $miner_port --http --http.addr 0.0.0.0 --http.vhosts "*" --http.port $miner_http_port --http.api 'net,eth,web3,personal' --http.corsdomain "*" --syncmode full --snapshot=false --mine --nodiscover --allow-insecure-unlock 2> $data_dir/miner.log &

sleep 1
echo "Miner node started on ETH port $miner_port, HTTP port $miner_http_port"
echo "-----------------------------------"

echo "run processor node..."
# 初始化 genesis.json 文件
geth init --datadir $data_dir/data_processor $data_dir/../genesis.json
# 创建CST处理节点
nohup geth --datadir $data_dir/data_processor --networkid $network_id --port $processor_port --http --http.addr 0.0.0.0 --http.vhosts "*" --http.port $processor_http_port --http.api 'net,eth,web3,personal' --http.corsdomain "*" --syncmode full --snapshot=false --nodiscover --allow-insecure-unlock 2> $data_dir/processor.log &
sleep 1
echo "Processor node started on ETH port $processor_port, HTTP port $processor_http_port"
echo "-----------------------------------"

echo "run normal node..."
# 初始化 genesis.json 文件
geth init --datadir $data_dir/data_normal $data_dir/../genesis.json
# 创建交易节点
nohup geth --datadir $data_dir/data_normal --networkid $network_id --port $normal_port --http --http.addr 0.0.0.0 --http.vhosts "*" --http.port $normal_http_port --http.api 'net,eth,web3,personal' --http.corsdomain "*" --syncmode full --snapshot=false --nodiscover --allow-insecure-unlock 2> $data_dir/normal.log &
sleep 1
echo "Normal node started on ETH port $normal_port, HTTP port $normal_http_port"
echo "-----------------------------------"

# 建立必要目录
mkdir $data_dir/other_cross_enode

echo "OK"
