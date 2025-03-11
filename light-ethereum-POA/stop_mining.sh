#!/bin/bash
# /root/light-ethereum/stop_mining.sh

# 设置变量
data_dir="/root/light-ethereum/data"
# 结束挖矿
geth --datadir $data_dir/data_miner  --exec "miner.stop()" attach
