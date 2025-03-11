// 示例用法
import {chooseNextNode, getValueFromJSON} from "./utilities.js";
import readline from 'readline';

// const jsonFilePath = 'D:\\MyProject\\Python\\Community_Detection\\result\\1704956929\\mat\\ETH.json';
// const keyToRetrieve = 'p_d';
// const value = getValueFromJSON(jsonFilePath, keyToRetrieve);
// // console.log(value);
//
// const index = 5;
//
// console.log(chooseNextNode(value, index));

//
// const normal_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
// const begin = normal_count.slice(0, 2).reduce((normal_count, val) => normal_count + val, 0);
//
// console.log(begin);
// console.log(new Set(normal_count).has(1));
// console.log(normal_count.slice(7,7+2));

import Web3 from "web3";
import fs from "fs";
import {isMainThread, parentPort, workerData} from 'worker_threads'; //使用多线程
import {delay} from "./utilities.js";

// 连接到以太坊节点
const web3 = new Web3('ws://8.130.102.188:30301');

// 获取 pending 交易
const pendingTx = await web3.eth.getPendingTransactions();
console.log(pendingTx);