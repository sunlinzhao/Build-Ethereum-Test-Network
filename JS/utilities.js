import Web3 from "web3";
import getNodeInfo from "./getNodeInfo.js";
import fs from "fs";
import readline from "readline";

// 拼接节点http服务访问地址
export function createHttpUrls(ips, ports) {
    const httpUrls = [];

    // 遍历每个IP
    for (const port of ports) {
        const urls = [];
        // 遍历每个端口
        for (const ip of ips) {
            const url = `http://${ip}:${port}`;
            urls.push(url);
        }
        httpUrls.push(urls);
    }
    return httpUrls;
}

// 节点进行分类
export async function classifyNodes(ips, ports) {
    //http-rpc服务地址
    const httpUrls = createHttpUrls(ips, ports);
    console.log(httpUrls);

    const miner_httpUrls = httpUrls[0];
    const miner_nodeInfo = await getNodeInfo(miner_httpUrls);
    const miner_accounts = miner_nodeInfo[0];
    const miner_balances = miner_nodeInfo[1];
    const miner_count = miner_nodeInfo[2];
    console.log('----------miner nodeInfo----------');
    console.log(miner_balances);
    console.log(miner_accounts);

    const processor_httpUrls = httpUrls[1];
    const processor_nodeInfo = await getNodeInfo(processor_httpUrls);
    const processor_accounts = processor_nodeInfo[0];
    const processor_balances = processor_nodeInfo[1];
    const processor_count = processor_nodeInfo[2];
    console.log('----------processor nodeInfo----------');
    console.log(processor_balances);
    console.log(processor_accounts);

    const normal_httpUrls = httpUrls[2];
    const normal_nodeInfo = await getNodeInfo(normal_httpUrls);
    const normal_accounts = normal_nodeInfo[0];
    const normal_balances = normal_nodeInfo[1];
    const normal_count = normal_nodeInfo[2];
    console.log('----------normal nodeInfo----------');
    console.log(normal_balances);
    console.log(normal_accounts);

    return {
        miner_httpUrls,
        miner_accounts,
        miner_count,
        processor_httpUrls,
        processor_accounts,
        processor_count,
        normal_httpUrls,
        normal_accounts,
        normal_count
    };
}

// 判断是否跨分片
export function isCrossShard(communities, tx) {
    const communityIndex1 = communities.findIndex(community => community.includes(tx[0]));
    const communityIndex2 = communities.findIndex(community => community.includes(tx[1]));

    return [communityIndex1 !== communityIndex2, communityIndex1]; // 返回是否跨分片，以及跨分片处理节点下标

}

// 划分交易序列
export function divideTxSeq(Tx_seq, count) { // 参数为交易序列和实际每个节点账户数量列表
    const div_tx_seq=[];
    let acc = 0;
    for (let i = 0; i < count.length; i++) {
        const temp = Tx_seq.slice(acc,acc+count[i]);
        const txs  = []
        for (let j = 0; j < temp.length; j++){
            txs.push(...temp[j]);
        }
        div_tx_seq.push(txs);
        acc+=count[i];
    }
    return div_tx_seq;
}

//关闭连接
export function closeConnection(web3Objects) {
    web3Objects.forEach(web3 => {
        web3.currentProvider.disconnect();
    });
}


// 延时函数
export async function delay(time) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, time);
    });
}

// 延时函数
export async function random_delay(minTime, maxTime) {
    const randomTime = Math.floor(Math.random() * (maxTime - minTime + 1)) + minTime;

    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, randomTime);
    });
}

// 从JSON中读取数据
export function getValueFromJSON(filePath, key) {
    try {
        const fileData = fs.readFileSync(filePath, 'utf-8');
        const jsonObject = JSON.parse(fileData);
        return jsonObject[key];
    } catch (error) {
        console.error('Error reading JSON file:', error);
        return null;
    }
}

// 选择一个交易目标
export function chooseNextNode(pDistribute, index, explorationRate) {
    const probabilities = pDistribute[index];
    const randomIndex = getRandomIndex(probabilities, explorationRate);
    if (randomIndex === index) {
        return chooseNextNode(pDistribute, index, explorationRate);
    }
    return randomIndex;
}

// 辅助函数 - 根据概率从分布选择随机索引
// export function getRandomIndex(probabilities) {
//     const randomValue = Math.random();
//
//     let cumulativeProbability = 0;
//     for (let i = 0; i < probabilities.length; i++) {
//         cumulativeProbability += probabilities[i];
//         if (randomValue <= cumulativeProbability) {
//             return i; // 返回随机索引
//         }
//     }
// }
export function getRandomIndex(probabilities, explorationRate) {
    const randomValue = Math.random();

    let cumulativeProbability = 0;
    for (let i = 0; i < probabilities.length; i++) {
        cumulativeProbability += probabilities[i];
        if (randomValue <= cumulativeProbability) {
            // 判断是否进行探索
            if (Math.random() < explorationRate) {
                // 随机选择其他节点
                const otherNodes = probabilities.map((_, index) => index);
                otherNodes.splice(i, 1); // 移除当前节点
                return otherNodes[Math.floor(Math.random() * otherNodes.length)];
            } else {
                return i; // 返回随机索引
            }
        }
    }
}

// 等待按键事件
export function waitForKeypress() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise(resolve => {
        rl.question('按下任意键或回车继续...', () => {
            rl.close();
            resolve();
        });
    });
}


