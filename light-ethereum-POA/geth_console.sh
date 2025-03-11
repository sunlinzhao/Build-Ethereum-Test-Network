#!/bin/bash
# /root/light-ethereum/geth_console.sh

# 设置变量
data_dir="/root/light-ethereum/data"
# 检查是否提供了足够的参数
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <data_directory>"
  exit 1
fi

data_directory="$data_dir/data_$1"

# 启动 geth 控制台并执行命令
geth --datadir "$data_directory" attach
