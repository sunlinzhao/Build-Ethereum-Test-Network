#!/bin/bash
# /root/light-ethereum/send_enode.sh

# 待上传文件路径
local_dir="/root/light-ethereum/data/cross_enode.txt"

# 远程服务配置信息
# 远程服务IPs
remote_servers=("8.130.102.188" "8.130.88.17" "8.130.141.74" "8.130.67.48")
# 远程服务账户
remote_user="root"
# 远程服务密码
remote_password="Sun990923"
# 远程服务文件路径
# remote_dir="/root/ethereum/data/data_boot/"
remote_dir="/root/light-ethereum/data/other_cross_enode/"

# 获取本机公网IP
pub_IP=$(curl ipinfo.io/ip)
# 使用 sed 替换 _ 到 . 之间的内容为本机IP
r_local_dir=$(echo "$local_dir" | sed "s/_.*./_$pub_IP.txt/")

# 使用 mv 命令修改文件名
mv "$local_dir" "$r_local_dir"

echo "$r_local_dir"

# 循环
for IP in "${remote_servers[@]}"; do
    # 上传文件
    expect -c "
    spawn scp -r $r_local_dir $remote_user@$IP:$remote_dir
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
