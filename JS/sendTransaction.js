import Web3 from "web3";
import {isMainThread, parentPort, workerData} from 'worker_threads'; //使用多线程
import {chooseNextNode, delay, getValueFromJSON, isCrossShard, random_delay} from './utilities.js';
import fs from "fs";
import readTxtFileToArray from "./readFromTxt.js";

// workerData 主线程传来的参数
const url = workerData.url;
const web3 = new Web3(new Web3.providers.HttpProvider(url));
const [communities, normal_accounts, processor_accounts, begin, count] = workerData.params;

// 线程编号
const threadIndex = workerData.index;

const timestamp = workerData.timestamp;

// 统计跨分片交易数量
let length = 0;
// 本节点账户范围
let accounts = [];
if (threadIndex.includes(("normal"))) {
    length = communities.length;
    accounts = normal_accounts.slice(begin, begin + count);
}

let CSTs = new Array(length).fill(0);
let Txs = [];

// 读取概率转移矩阵
const data_file_which = "D:\\MyProject\\JS\\resource\\data_file.txt";
const data_file = await readTxtFileToArray(data_file_which);
const p_d = getValueFromJSON(data_file[2], 'p_d');

// 自由交易概率
// let p = 0.08;
// let d = [1000, 1500]
// if (parseInt(data_file[4])===0) {
//     p = 0.01;
//     d = [500, 1000]
// }

// 子线程执行
if (!isMainThread) {
    // 在子线程中监听主线程的消息
    parentPort.on('message', async messageFromMain => {
        console.log(`Thread ${threadIndex} received message from main thread:`, messageFromMain);

        // 根据不同的操作执行不同的代码
        switch (messageFromMain.operation) {
            case 'send_tx':
                // 执行发送交易操作，使用 messageFromMain.params
                console.log(`Thread 【${threadIndex}】 executing 【send_tx】 with params:`, messageFromMain.params);

                const amount = messageFromMain.params[0];
                const community = messageFromMain.params[1];
                const times = messageFromMain.params[2];

                for (let i = 0; i < times; i++) {
                    for (let from_index of community) {
                        if (new Set(accounts).has(normal_accounts[from_index])) {
                            const to_index = chooseNextNode(p_d, from_index, p);
                            const tx = [from_index, to_index];

                            Txs.push(tx);

                            const result = isCrossShard(communities, tx);
                            if (result[0]) { //跨分片片交易
                                console.log(`跨分片交易:`, tx);
                                await send_tx(normal_accounts[tx[0]], processor_accounts[result[1] % 4], amount, true); // 4 个跨分片交易处理节点，%4
                                // 统计跨分片交易数量
                                CSTs[result[1]] += 1;
                                await random_delay(1000, 1500);
                                await delay(2000);
                                // 向主线程发送CST消息
                                parentPort.postMessage({threadIndex, operation: 'CST', params: [result[1] % 4, tx[1]]});
                            } else {
                                console.log('分片内交易:', tx);
                                await send_tx(normal_accounts[tx[0]], normal_accounts[tx[1]], amount, false);
                            }
                            await random_delay(d[0], d[1]);
                        }
                    }
                }
                // 向主线程发送完成消息
                if (messageFromMain.flag) { //最后一个社区执行完，给主线程发送完成消息
                    parentPort.postMessage({threadIndex, operation: 'done', params: true});
                }
                // else {
                //     parentPort.postMessage({threadIndex, operation: 'continue', params: true}); // 继续下一个社区
                // }
                break;
            case 'CST':
                await delay(2000);
                console.log(`Thread 【${threadIndex}】 executing 【CST】 with params:`, messageFromMain.params);
                await send_tx(processor_accounts[messageFromMain.params[0][0]], normal_accounts[messageFromMain.params[0][1]], messageFromMain.params[1], true);
                await random_delay(d[0], d[1]);
                break;

            case 'close':
                // 断开连接，结束进程
                console.log(`Thread 【${threadIndex}】 executing 【close】 with params:`, messageFromMain.params);
                // 关闭连接
                web3.currentProvider.disconnect();

                if (threadIndex.includes(("normal"))) {
                    const data_file_which = "D:\\MyProject\\JS\\resource\\data_file.txt";
                    const data_file = await readTxtFileToArray(data_file_which);
                    // 指定文件路径和文件名
                    const filePath0 = `D:\\MyProject\\JS\\resource\\result\\${timestamp}_${data_file[3]}\\CST\\${threadIndex}.json`;
                    // 写入数据
                    fs.writeFileSync(filePath0, JSON.stringify(CSTs));

                    // 指定文件路径和文件名
                    const filePath1 = `D:\\MyProject\\JS\\resource\\result\\${timestamp}_${data_file[3]}\\Tx\\${threadIndex}.json`;
                    // 写入数据
                    fs.writeFileSync(filePath1, JSON.stringify(Txs));
                }

                // 退出线程
                process.exit();
                break;

            // 添加更多操作的处理
            default:
                console.error(`Thread 【${threadIndex}】 received unknown operation:`, messageFromMain.operation);
        }

        // 向主线程发送消息
        // parentPort.postMessage({threadIndex, result: `Thread 【${threadIndex}】 completed its task`});

    });
}

// 定义获取账户的函数
const getAccounts = () => {
    return new Promise(async (resolve, reject) => {
        await web3.eth.getAccounts((error, accounts) => {
            if (error) {
                reject(error);
            } else {
                resolve(accounts);
            }
        });
    });
};

// 定义解锁账户函数
const unlockAccount = (address, password, duration) => {
    return new Promise(async (resolve, reject) => {
        await web3.eth.personal.unlockAccount(address, password, duration, (error, unlocked) => {
            if (error) {
                reject(error);
            } else {
                resolve(unlocked); 
            }
        });
    });
};

// 定义转账函数
const sendTransaction = (from, to, value, flag) => {
    return new Promise(async (resolve, reject) => {
        // 获取当前时间戳
        const currentTimestamp = Date.now();
        // 构建输入数据, 将时间戳转换为十六进制
        const inputHex = '0x0' + currentTimestamp.toString(16); // 将时间戳作为交易输入数据, 保证长度为偶数
        if (flag) { // 跨分片交易随机等待
            await random_delay(1000, 2000);
        }
        web3.eth.sendTransaction({
            from: from,
            to: to,
            value: value,
            data: inputHex
        }, (error, transaction) => {
            if (error) {
                reject(error);
            } else {
                resolve(transaction);
            }
        });
    });
};

// 定义整体操作的函数
const send_tx = async (fromAccount, toAccount, num, flag) => {
    try {

        // // 获取账户余额
        // const balance = web3.utils.fromWei(web3.eth.getBalance(fromAccount).toString(), 'wei');
        // // 将 Wei 转换为 BigNumber 对象
        // const balanceInBN = web3.utils.toBN(balance);
        // // 除以 1000，计算交易金额
        // const transactionAmount = balanceInBN.divn(1000)
        // // 将结果转换为字符串
        // const transactionAmountStr = transactionAmount.toString();

        // console.log('Transaction from ', fromAccount, 'to', toAccount);
        // 转账操作
        // await sendTransaction(fromAccount, toAccount, web3.utils.fromWei(num, 'wei'), flag);
        const transaction = await sendTransaction(fromAccount, toAccount, web3.utils.fromWei(num, 'wei'), flag);
        // const transaction = await sendTransaction(fromAccount, toAccount, web3.utils.fromWei(transactionAmountStr, 'wei'));
        // console.log('Transaction sent:', transaction);

    } catch (error) {
        console.error('Error:', error);
    }
};