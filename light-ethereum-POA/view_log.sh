#!/bin/bash
# /root/light-ethereum/view_log.sh

# 设置变量
data_dir="/root/light-ethereum/data"
# 检查是否提供了足够的参数
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <data_directory>"
  exit 1
fi

data_directory="$data_dir/$1.log"

# 查看日志
tail -200f "$data_directory"
