#!/bin/bash
# /root/light-ethereum/check_balance.sh

# 设置变量
datadir="/root/light-ethereum/data"

# 余额列表
Balance_processor=()
Balance_normal=()

# 查询账户
result0=$(geth --datadir $datadir/data_processor --exec "eth.accounts" attach)
echo "$result0"

# 检查查询是否成功
if [ $? -eq 0 ]; then
    # 移除方括号，并将逗号替换为换行符
    addresses=$(echo "$result0" | tr -d '[]' | tr ',' '\n')

    # 将地址列表转为数组
    address_array=($addresses)

    # 获取余额
    echo ">>>>>>>> processor acounts' balance [ether] <<<<<<<<<"
    for address in "${address_array[@]}"; do
	    balance=$(geth --datadir $datadir/data_processor --exec " web3.fromWei(eth.getBalance($address), 'ether')" attach)
	    Balance_processor+=("$balance")
            echo "$address : $balance"
	    echo "-------------------"
    done
else
    echo "Error executing Geth query."
fi


# 查询账户
result1=$(geth --datadir $datadir/data_normal --exec "eth.accounts" attach)
echo "$result1"

# 检查查询是否成功
if [ $? -eq 0 ]; then
    # 移除方括号，并将逗号替换为换行符
    addresses=$(echo "$result1" | tr -d '[]' | tr ',' '\n')

    # 将地址列表转为数组
    address_array=($addresses)

    # 获取余额
    echo ">>>>>>>> normal acounts' balance [ether] <<<<<<<<<"
    for address in "${address_array[@]}"; do
            balance=$(geth --datadir $datadir/data_normal --exec " web3.fromWei(eth.getBalance($address), 'ether')" attach)
            Balance_normal+=("$balance")
	    echo "$address : $balance"
            echo "-------------------"
    done
else
    echo "Error executing Geth query."
fi

