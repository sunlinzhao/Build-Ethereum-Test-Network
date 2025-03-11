import {Worker, isMainThread, parentPort, workerData} from 'worker_threads';  //使用多线程

import readTxtFileToArray from './readFromTxt.js';
import {
    createHttpUrls,
    divideTxSeq,
    classifyNodes,
    delay,
    random_delay,
    waitForKeypress,
    getValueFromJSON
} from './utilities.js';
import fs from "fs";

//ip地址
const ips = ['8.130.102.188', '8.130.88.17', '8.130.141.74', '8.130.67.48'];
//http端口
const ports = ['9001', '9002', '9003'];

// 子任务文件
const subWorkFile = 'D:\\MyProject\\JS\\sendTransaction.js';
const subMonitorFile = 'D:\\MyProject\\JS\\monitor.js';

const data_file_which = "D:\\MyProject\\JS\\resource\\data_file.txt";
const data_file = await readTxtFileToArray(data_file_which);
//分片划分
const jsonFilePath = data_file[1]
// ---------------------------------------------------------------------------------------------------------------------
const index = parseInt(data_file[4]);
const communityType = ["communities0", "communities1", "communities2", "communities3"];
const methods = ["TALA", "TxAllo", "ShardCutter", "Random"];
const communities = getValueFromJSON(jsonFilePath, communityType[index]);
console.log('----------communities----------');
console.log(communities);

const accounts = getValueFromJSON(data_file[0], "accounts");

const data = {
    "communities": communities,
    "data_file": jsonFilePath,
    "dataset":  data_file[3],
    "methods": methods[index],
    "index": index,
    "accounts_count": accounts.length,
}

// 获取当前时间戳，秒级
const timestampInSeconds = Math.floor(Date.now() / 1000);
const directory = `D:\\MyProject\\JS\\resource\\result\\${timestampInSeconds}` + '_' + data_file[3];
// 检查目录是否存在，如果不存在则创建
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
    fs.mkdirSync(directory + "\\CST", { recursive: true });
    fs.mkdirSync(directory + "\\Tx", { recursive: true });
    fs.mkdirSync(directory + "\\index", { recursive: true });
}

// 写入communities数据到结果
fs.writeFileSync(directory + '\\communities.json', JSON.stringify(data));


// 节点分类
const {
    miner_httpUrls,
    miner_accounts,
    miner_count,
    processor_httpUrls,
    processor_accounts,
    processor_count,
    normal_httpUrls,
    normal_accounts,
    normal_count
} = await classifyNodes(ips, ports);

//继续标志
// let continueFlag = false;
// let continueCount = 0;
// let continue0 = false;
// let continue1 = false;
// let continue2 = false;
// let continue3 = false;
// let continues = [continue0, continue1, continue2, continue3];

// 连接到节点
const miners = [];
const processors = [];
const normals = [];
const monitors = [];

// 在主线程中
if (isMainThread) {

    // 交易完成计时器
    let counter = 0;

    // 监控节点子任务
    const monitor = new Worker(subMonitorFile, {workerData: {index: `monitor`, url: [], params: [], timestamp: timestampInSeconds}});
    // 监听子线程的消息
    monitor.on('message', messageFromWorker => {
        // console.log(`Main thread received message from thread 【${messageFromWorker.threadIndex}】:`, messageFromWorker);
        // if(messageFromWorker.operation === 'continue'){
        //     continueFlag = true;
        // }
    });
    monitors.push(monitor);

    // 矿工线程子任务
    for (let i = 0; i < miner_httpUrls.length; i++) {
        const miner = new Worker(subWorkFile, {workerData: {index: `miner_${i}`, url: miner_httpUrls[i], params: [], timestamp: timestampInSeconds}});
        // 监听子线程的消息
        miner.on('message', messageFromWorker => {
            console.log(`Main thread received message from thread 【${messageFromWorker.threadIndex}】:`, messageFromWorker);
        });
        miners.push(miner);
    }

    // 跨分片处理线程子任务
    for (let i = 0; i < processor_httpUrls.length; i++) {
        const processor = new Worker(subWorkFile, {
            workerData: {
                index: `processor_${i}`,
                url: processor_httpUrls[i],
                params: [communities, normal_accounts, processor_accounts, null],
                timestamp: timestampInSeconds
            }
        });
        // 监听子线程的消息
        processor.on('message', messageFromWorker => {
            console.log(`Main thread received message from thread 【${messageFromWorker.threadIndex}】:`, messageFromWorker);
        });
        processors.push(processor);
    }

    // 交易线程子任务
    for (let i = 0; i < normal_httpUrls.length; i++) {
        const begin = normal_count.slice(0, i).reduce((normal_count, val) => normal_count + val, 0);
        const normal = new Worker(subWorkFile, {
            workerData: {
                index: `normal_${i}`,
                url: normal_httpUrls[i],
                params: [communities, normal_accounts, processor_accounts, begin, normal_count[i]],
                timestamp: timestampInSeconds
            }
        });
        // 监听子线程的消息
        normal.on('message', async messageFromWorker => {
            console.log(`Main thread received message from thread 【${messageFromWorker.threadIndex}】:`, messageFromWorker);
            if (messageFromWorker.operation === 'CST') {
                console.log('=========ready CST=========', messageFromWorker.params);
                processors[messageFromWorker.params[0]].postMessage({
                    operation: 'CST',
                    params: [messageFromWorker.params, '1000000000000']
                    // (1000000000*(Math.floor(Math.random()*5))).toString()
                });
            }
            // if (messageFromWorker.operation === 'continue') {
            //     continueCount += 1;
            // }
            if (messageFromWorker.operation === 'done') {
                counter++; // 累加交易
                if(counter === normal_httpUrls.length) {
                    await delay(10000);
                    // 关闭连接
                    closeThreads(processors);
                    closeThreads(normals);
                    closeThreads(miners);
                    closeThreads(monitors);
                }
            }
        });
        normals.push(normal);
    }

    console.log('----------start_tx----------');


    // 启动监控指标
    // startMonitor(worker);

    // 不能循环去处理交易，应该取出每个节点的交易序列，交给各自的子线程去做
    await startWork(normals);

    //交易信号
    async function startWork(workers) {
        startMonitor(monitors);
        let done_flag = false;
        for (let i=0; i<communities.length; i++) {
            if (i===communities.length-1) {
                done_flag = true;
            }

            for (const worker of workers) {
                const amount = '1000000000000';
                const times = 8; // 交易次数
                worker.postMessage({operation: 'send_tx', params: [amount, communities[i], times], "flag": done_flag});
            }
            // await waitForKeypress(); //等待按键事件
            // while (!continueFlag && continueCount < 4) await delay(10000);
            // continueFlag = false;
            // continueCount = 0;
            // 记录单个分片指标
            await delay(20000); //等待20秒
            monitors[0].postMessage({operation: 'record', params: i});
        }
    }

    //开始监控
    function startMonitor(workers) {
        workers.forEach(worker => {
            worker.postMessage({operation: 'start_monitor', params: true});
        });
    }

    // 关闭信号
    function closeThreads(workers) {
        workers.forEach(worker => {
            worker.postMessage({operation: 'close', params: true});
        });
    }
}

//'error': 当工作线程发生错误时触发。
// 'exit': 当工作线程退出时触发。
//'online': 当工作线程变为在线状态时触发。
//'messageerror': 当无法序列化或发送消息时触发。

