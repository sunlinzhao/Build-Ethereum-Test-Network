#!/bin/bash
# /root/light-ethereum/unlockAccount.sh
datadir="/root/light-ethereum/data"

result0=$(geth --datadir $datadir/data_processor --exec "eth.accounts" attach)
echo "$result0"

# 检查查询是否成功
if [ $? -eq 0 ]; then
    # 移除方括号，并将逗号替换为换行符
    addresses=$(echo "$result0" | tr -d '[]' | tr ',' '\n')

    # 将地址列表转为数组
    address_array=($addresses)

    # 解锁账户
    for address in "${address_array[@]}"; do
	    unlock=$(geth --datadir $datadir/data_processor --exec "personal.unlockAccount($address,'123456',60000)" attach)
	    # 检查结果并输出相应消息
	    if [ "$unlock" == "true" ]; then
		    echo "Unlock success!"
	    else
		    echo "Unlock failed!"
	    fi
    done
else
    echo "Error executing Geth query."
fi

result1=$(geth --datadir $datadir/data_normal --exec "eth.accounts" attach)
echo "$result1"

# 检查查询是否成功
if [ $? -eq 0 ]; then
    # 移除方括号，并将逗号替换为换行符
    addresses=$(echo "$result1" | tr -d '[]' | tr ',' '\n')

    # 将地址列表转为数组
    address_array=($addresses)

    # 解锁账户
    for address in "${address_array[@]}"; do
	    unlock=$(geth --datadir $datadir/data_normal --exec "personal.unlockAccount($address,'123456',60000)" attach)
	    # 检查结果并输出相应消息
            if [ "$unlock" == "true" ]; then
                    echo "Unlock success!"
            else
                    echo "Unlock failed!"
            fi
    done
else
    echo "Error executing Geth query."
fi


result2=$(geth --datadir $datadir/data_miner --exec "eth.accounts" attach)
echo "$result2"

# 检查查询是否成功
if [ $? -eq 0 ]; then
    # 移除方括号，并将逗号替换为换行符
    addresses=$(echo "$result2" | tr -d '[]' | tr ',' '\n')

    # 将地址列表转为数组
    address_array=($addresses)

    # 解锁账户
    for address in "${address_array[@]}"; do
            unlock=$(geth --datadir $datadir/data_miner --exec "personal.unlockAccount($address,'123456',60000)" attach)
            # 检查结果并输出相应消息
            if [ "$unlock" == "true" ]; then
                    echo "Unlock success!"
            else
                    echo "Unlock failed!"
            fi
    done
else
    echo "Error executing Geth query."
fi
