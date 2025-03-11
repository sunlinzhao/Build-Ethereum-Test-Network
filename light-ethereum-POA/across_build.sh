#!/bin/bash
# /root/light-ethereum/across_build.sh

# 指定存储节点唯一标识的文件夹路径
folder_path="/root/light-ethereum/data/other_cross_enode/"
# 建立交叉连接的节点存储路径
data_dir="/root/light-ethereum/data"

node=("miner" "processor" "normal")
node_num=${#node[@]}


# 遍历文件夹中的文件
for file in "$folder_path"/*; do
    if [ -f "$file" ]; then
        # 使用 while read 逐行读取文件内容
        while IFS= read -r enode; do
        	for ((i=0; i<$node_num; i++)); do 
                # 使用 geth 添加节点
                geth --datadir $data_dir/data_${node[i]} --exec "admin.addPeer($enode)" attach

                # 检查 geth 命令是否执行成功
                if [ $? -eq 0 ]; then
                    echo "Node added successfully: $enode"
                else
                    echo "Failed to add node: $enode"
                fi
                
                # 生成一个 1 到 2 之间的随机数
		random_time=$(( (RANDOM % 1) + 1 ))
                sleep $random_time
                
            done
        done < "$file"
    fi
done

