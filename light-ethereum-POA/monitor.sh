#!/bin/bash
# /root/light-ethereum/monitor.sh

# 设置变量
data_dir="/root/light-ethereum/data"
network_id=123456
ws_port=30301
port=8595
password_file="$data_dir/.passwd"  # 密码文件路径
accounts_directory="/root/light-ethereum/data/Accounts"
validators_directory="/root/light-ethereum/data/Validators"  # 验证者账户文件路径
num_file="/root/light-ethereum/node_num.txt"
# 指定存储节点唯一标识的文件夹路径
folder_path="/root/light-ethereum/data/other_cross_enode/"

# 检查文件是否存在
if [ -e "$num_file" ]; then
    # 读取文件中的数字
    read -r number < "$num_file"
else
    echo "$num_file is not exist."
fi

num_accounts=$number  # 设置创建的账户数量

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



echo "run monitor node..."

# 初始化 genesis.json 文件
geth init --datadir $data_dir/data_monitor $data_dir/../genesis.json
# 创建 monitor 节点
nohup geth --datadir $data_dir/data_monitor --networkid $network_id --port $port --syncmode full --snapshot=false --maxpeers 1000 --nodiscover --allow-insecure-unlock --ws --ws.addr 0.0.0.0 --ws.port $ws_port --ws.api 'net,eth,web3,personal' --ws.origins "*" 2> $data_dir/monitor.log &

sleep 1
echo "Monitor node started on ETH port $port, WS port $ws_port"
echo "-----------------------------------"

echo "MONITOR  LINKING OTHRT NODES..."

# 遍历文件夹中的文件
# 遍历文件夹中的文件
for file in "$folder_path"/*; do
    if [ -f "$file" ]; then
        # 使用 while read 逐行读取文件内容
        while IFS= read -r enode; do
            # 使用 geth 添加节点
            geth --datadir $data_dir/data_monitor --exec "admin.addPeer($enode)" attach
            # 检查 geth 命令是否执行成功
            if [ $? -eq 0 ]; then
            echo "Node added successfully: $enode"
            else
            echo "Failed to add node: $enode"
            fi

            # 生成一个 1 到 2 之间的随机数
            random_time=$(( (RANDOM % 1) + 1 ))
            sleep $random_time
        done < "$file"
    fi
done
