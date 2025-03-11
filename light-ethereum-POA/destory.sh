#!/bin/bash
# /root/light-ethereum/destory.sh

# 结束所有geth相关进程
sudo pkill -f 'geth'
# 结束引导节点进程
sudo pkill bootnode

# 等待3秒钟
sleep 1

# 查看'geth'相关进程
# ps aux | grep "geth"

# 删除相关文件
rm -rf /root/light-ethereum/data/*

# 删除缓存
# rm -rf /root/.ethash/*

