import * as fs from 'fs';
import * as readline from 'readline';

// 逐行读取txt文件的内容并存储在数组中
function readTxtFile(filePath) {
    return new Promise((resolve, reject) => {
        const fileStream = fs.createReadStream(filePath);
        const rl = readline.createInterface({
            input: fileStream, crlfDelay: Infinity,
        });
        const lines = []; // 用于存储每一行的数组
        rl.on('line', (line) => {
            // console.log(line)
            lines.push(line)
        });
        rl.on('close', () => {
            resolve(lines);
        });
        rl.on('error', (error) => {
            reject(error);
        });
    });
}

async function readTxtFileToArray(filePath) {
    try {
        const fileContent = await readTxtFile(filePath);
        let fileArray = []; // 定义一个空数组用于存储文件内容
        for (let line of fileContent) { // 使用of关键字遍历文件内容
            // 将 JSON 字符串解析为 JavaScript 对象
            // const nestedArrays = JSON.parse(line);
            fileArray.push(line);
        }
        return fileArray;
    } catch (error) {
        throw new Error(error);
    }
}


// 导出默认值
export default readTxtFileToArray;

// params[0]: filePath
// readTxtFileToArray(params[0])
//     .then((lines) => {
//         console.log('Lines:', lines);
//     })
//     .catch((error) => {
//         console.error('Error reading the file:', error);
//     }); 改为js类