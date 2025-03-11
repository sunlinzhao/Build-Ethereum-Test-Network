#!/bin/bash
# /root/light-ethereum/start_mining.sh

# 设置变量
data_dir="/root/light-ethereum/data"

# 开启挖矿
geth --datadir $data_dir/data_miner  --exec "miner.start(3)" attach
