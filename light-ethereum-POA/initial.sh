#!/bin/bash
# /root/light-ethereum/initial.sh
# 设置变量
data_dir="/root/light-ethereum/data"
password_file="$data_dir/.passwd"  # 密码文件路径
accounts_file="/root/light-ethereum/data/Accounts"  # 新增账户文件路径
validators_file="/root/light-ethereum/data/Validators"	# 验证者账户文件路径
num_file="/root/light-ethereum/node_num.txt"

# Check if the directory exists, if not, create it
if [ ! -d "$accounts_file" ]; then
    mkdir $accounts_file
    echo "Directory created: $(dirname "$accounts_file")"
fi

# Check if the directory exists, if not, create it
if [ ! -d "$validators_file" ]; then
    mkdir $validators_file
    echo "Directory created: $(dirname "$validators_file")"
fi

# 检查文件是否存在
if [ -e "$num_file" ]; then
    # 读取文件中的数字
    read -r number < "$num_file"
    echo "There are $number normal accounts will be created. Please waiting..."
else
    echo "$num_file is not exist."
fi

num_accounts=$number  # 设置创建的账户数量

# 生成密码文件
echo "123456" > $password_file

# 创建矿工节点账户
echo "create miner account ..."
result0=$(geth account new --password $password_file --datadir $data_dir/data_miner)

m_account=$(echo "$result0" | grep -oP '0x[a-fA-F0-9]{40}')
#----------------------------------------------------------------- POA

# 创建跨分片处理账户
echo "create processor account ..."
result1=$(geth account new --password $password_file --datadir $data_dir/data_processor)
p_account=$(echo "$result1" | grep -oP '0x[a-fA-F0-9]{40}')

accounts=()
accounts+=("$p_account") # 跨分片处理账户也需要初始资金

echo "create normal account ..."
# 循环创建账户
for ((i=0; i<$num_accounts; i++)); do
    # 创建账户
    account=$(geth account new --password $password_file --datadir $data_dir/data_normal)
    # 提取账户信息
    default_account=$(echo "$account" | grep -oP '0x[a-fA-F0-9]{40}')
    
    accounts+=("$default_account")
    echo "$default_account"
    
    echo "---------------------------------------"
done

# 获取本机公网IP
pub_IP=$(curl -s ipinfo.io/ip)
# 将 accounts 数组中的每个元素写入文件
for account in "${accounts[@]}"; do
  echo "$account" >> "$accounts_file/accounts_$pub_IP.txt"
  echo "$account" >> "$data_dir/accounts.txt"
done

# 远程服务配置信息
# 远程服务IPs
remote_servers=("8.130.102.188" "8.130.88.17" "8.130.141.74" "8.130.67.48")
# 远程服务账户
remote_user="root"
# 远程服务密码
remote_password="Sun990923"
# 远程服务文件路径
remote_dir="/root/light-ethereum/data/Accounts/"
local_dir=$accounts_file/accounts_$pub_IP.txt

echo "$local_dir"

# 循环
for IP in "${remote_servers[@]}"; do
    # 上传文件
    expect -c "
    spawn scp -r $local_dir $remote_user@$IP:$remote_dir
    expect {
        \"*assword:\" {
            send \"$remote_password\r\"
            exp_continue
        }
        \"yes/no\" {
            send \"yes\r\"
            exp_continue
        }
        eof
    }
    "

    # Check scp command
    if [ $? -eq 0 ]; then
        echo "Upload file success!"
    else
        echo "File upload fail"
    fi
done

m_accounts=()
m_accounts+=("$m_account")
# 将 accounts 数组中的每个元素写入文件
for account in "${m_accounts[@]}"; do
  echo "$account" >> "$validators_file/validators_$pub_IP.txt"
  echo "$account" >> "$data_dir/validators.txt"
done

remote_dir="/root/light-ethereum/data/Validators/"
local_dir=$validators_file/validators_$pub_IP.txt



echo "$local_dir"

# 循环
for IP in "${remote_servers[@]}"; do
    # 上传文件
    expect -c "
    spawn scp -r $local_dir $remote_user@$IP:$remote_dir
    expect {
        \"*assword:\" {
            send \"$remote_password\r\"
            exp_continue
        }
        \"yes/no\" {
            send \"yes\r\"
            exp_continue
        }
        eof
    }
    " 

    # Check scp command
    if [ $? -eq 0 ]; then
        echo "Upload file success!"
    else
        echo "File upload fail"
    fi
done
#-------------------------------------------------------------------- POA
