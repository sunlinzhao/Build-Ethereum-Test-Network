import Web3 from "web3";
import fs from "fs";
import {isMainThread, parentPort, workerData} from 'worker_threads'; //使用多线程
import {delay} from "./utilities.js";
import readTxtFileToArray from "./readFromTxt.js";

// 连接到以太坊节点
const web3 = new Web3('ws://8.130.102.188:30301');

// 存储交易时间戳的数组
let transactionTimestamps = [];
let blockTimestamps = [];
let blockTimes = [];
let blockTransactions = [];
let Delays = [];
let Throughputs = [];
let AverageDelays = [];

const threadIndex = workerData.index;
const timestamp = workerData.timestamp;

// web3.eth.getBlockNumber()
//     .then(blockNumber => console.log(`Current block number: ${blockNumber}`))
//     .catch(console.error);
//
// const block = await web3.eth.getBlock('latest', true);
// console.log(block.transactions);

if (!isMainThread) {
    let subscription;
    // 在子线程中监听主线程的消息
    parentPort.on('message', async messageFromMain => {
        console.log(`Thread ${threadIndex} received message from main thread:`, messageFromMain);
        switch (messageFromMain.operation) {
            case 'start_monitor':
                // 订阅新区块头
                subscription = web3.eth.subscribe('newBlockHeaders', handleNewBlock)
                    .on("changed", handleConnected)
                    .on("data", handleData)
                    .on("error", handleError);
                break;
            case 'close':
                await delay(10000);

                // 停止订阅
                if (subscription) {
                    await new Promise((resolve, reject) => {
                        subscription.unsubscribe((error, success) => {
                            if (error) {
                                console.error(error);
                                reject(error);
                            } else {
                                console.log(success);
                                resolve(success);
                            }
                        });
                    });
                }
                web3.currentProvider.disconnect();
                process.exit();
                break;
            case 'record':
                // 将数据组织为对象
                const data = {
                    transactionTimestamps,
                    blockTimestamps,
                    blockTimes,
                    blockTransactions,
                    Delays,
                    Throughputs,
                    AverageDelays,
                };

                // 将数据转换为 JSON 格式
                const jsonData = JSON.stringify(data, null, 2);

                const data_file_which = "D:\\MyProject\\JS\\resource\\data_file.txt";
                const data_file = await readTxtFileToArray(data_file_which);

                // 指定文件路径和文件名
                const filePath = `D:\\MyProject\\JS\\resource\\result\\${timestamp}_${data_file[3]}\\index\\community_${messageFromMain.params}.json`;

                // 将 JSON 数据写入文件
                fs.writeFileSync(filePath, jsonData, 'utf-8');

                console.log('Data has been written to json file.');

                // 清空记录
                transactionTimestamps = [];
                blockTimestamps = [];
                blockTimes = [];
                blockTransactions = [];
                Delays = [];
                Throughputs = [];
                AverageDelays = [];
                break;

            default:
                console.error(`Thread 【${threadIndex}】 received unknown operation:`, messageFromMain.operation);

        }
    })
}


// 处理新区块的回调函数
function handleNewBlock(error, result) {
    if (!error) {
        // 获取区块信息
        web3.eth.getBlock(result.hash, true)
            .then(async block => {
                // 处理交易信息
                // await handleTransactions(block.transactions);
                // console.log(block.transactions)
            })
            .catch(console.error);
    } else {
        console.error(error);
    }
}

// 处理连接事件的回调函数
function handleConnected(subscriptionId) {
    console.log(subscriptionId);
}

// 处理数据事件的回调函数
async function handleData(blockHeader) {
    try {
        // 异步操作，不会阻塞其他事件监听器
        const block = await web3.eth.getBlock(blockHeader.hash, true);
        console.log("---------------- Block number : ", block.number);
        if (block.transactions.length > 0){
            await handleTransactions(block.transactions, block.timestamp, block.transactions.length);
            // const pendingTx = await web3.eth.getPendingTransactions();
            // if (pendingTx.length === 0) {
            //     // 向主线程发送continue消息
            //     parentPort.postMessage({threadIndex, operation: 'continue', params: true});
            // }
        }
    } catch (err) {
        console.error(err);
    }
}

// 处理错误事件的回调函数
function handleError(error) {
    console.error(error);
}

// 处理交易信息的函数
async function handleTransactions(transactions, blockTime, num) {

    // 区块时间戳是以秒为单位，且是区块创建时间，不合适
    const blockTimestamp = Date.now(); // 转换为毫秒

    // 存储区块打包时间戳
    blockTimestamps.push(blockTimestamp);
    // 存储区块创建时间
    blockTimes.push(blockTime);
    // 存储交易数量
    blockTransactions.push(num);

    for (const transaction of transactions) {
        // 将十六进制字符串转换为十进制整数
        const transactionTimestamp = parseInt(transaction.input, 16); // 转换为毫秒
        const delay = blockTimestamp - transactionTimestamp;

        // 存储交易时间戳
        transactionTimestamps.push(transactionTimestamp);
        Delays.push(delay);

        // console.log(`Transaction hash: ${transaction.hash}`);
        // console.log(`Timestamp: ${new Date(transactionTimestamp).toISOString()}`);
        // console.log(`Delay: ${delay} ms`);
    }

    // 计算吞吐量和平均延迟
    const throughput = transactionTimestamps.length / ((blockTimestamp - transactionTimestamps[0]) / 1000);
    const averageDelay = Delays.reduce((sum, delay) => sum + delay, 0) / transactionTimestamps.length;

    console.log(`Throughput: ${throughput.toFixed(2)} tx/s`);
    console.log(`Average Delay: ${averageDelay.toFixed(2)} ms`);
    Throughputs.push(throughput);
    AverageDelays.push(averageDelay);
}