#!/bin/bash
# /root/light-ethereum/buildLink.sh

# 设置变量
data_dir="/root/light-ethereum/data"
output_file="$data_dir/cross_enode.txt"



# 获取节点标识列表
node_identifiers=()

echo "Node Identifiers:"
# 生成节点标识列表

miner_enode=$(geth --datadir $data_dir/data_miner --exec "admin.nodeInfo.enode" attach)
node_identifiers+=("$miner_enode")
echo "- $miner_enode"
processor_enode=$(geth --datadir $data_dir/data_processor --exec "admin.nodeInfo.enode" attach)
node_identifiers+=("$processor_enode")
echo "- $processor_enode"
normal_enode=$(geth --datadir $data_dir/data_normal --exec "admin.nodeInfo.enode" attach)
node_identifiers+=("$normal_enode")
echo "- $normal_enode"


# 检查文件是否存在
if [ -f "$output_file" ]; then
  # 如果文件存在，则删除
  rm "$output_file"
  echo "File '$output_file' deleted."
else
  echo "File '$output_file' does not exist. And it will be created!"
fi

# 获取本机公网IP
pub_IP=$(curl -s ipinfo.io/ip)

# 输出到文件
for enode in "${node_identifiers[@]}"; do
  # 使用 sed 替换 @ 到 : 之间的内容为公网IP
  r_enode=$(echo "$enode" | sed "s/@.*:/@$pub_IP:/")
  echo "$r_enode" >> "$output_file"
done
