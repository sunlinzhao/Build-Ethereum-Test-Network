import Web3 from "web3";
// import {parentPort, workerData} from 'worker_threads';  //使用多线程

// workerData 主线程传来的参数
// let params = workerData;


// 定义获取账户的函数
const getAccounts = (web3) => {
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
// 定义获取账户余额的函数
const getAccountBalance = (web3, account) => {
    return new Promise(async (resolve, reject) => {
        await web3.eth.getBalance(account, (error, balance) => {
            if (error) {
                reject(error);
            } else {
                // 将余额从 Wei 转换为 Ether
                const balanceInEther = web3.utils.fromWei(balance, 'ether');
                resolve(balanceInEther);
            }
        });
    });
};


async function getNodeInfo(httpUrls) {
    let Accounts = [];
    let Balances = [];
    let Count = []; // 统计每个实际节点账户个数
    for (let i = 0; i < httpUrls.length; i++) {

        let web3 = new Web3(new Web3.providers.HttpProvider(httpUrls[i]));
        // 获取账户
        const accounts = await getAccounts(web3);
        let acc = 0;
        // 由于 getAccountBalance 是异步的，需要使用 async/await 或者处理 Promise
        for (const account of accounts) {
            const balance = await getAccountBalance(web3, account);
            Accounts.push(account);
            Balances.push(balance);
            acc++;
        }
        Count.push(acc);
        // 关闭连接
        web3.currentProvider.disconnect();
    }
    return [Accounts, Balances, Count];
}

// 导出默认值
export default getNodeInfo;

// params[0]: http address list
// getNodeInfo(params[0]).then((res) => {
//     // console.log('Accounts:', Accounts);
//     parentPort.postMessage(res)
// }).catch((error) => {
//     console.error('Error getting Accounts:', error);
// })