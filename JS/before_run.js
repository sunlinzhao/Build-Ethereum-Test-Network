import {getValueFromJSON} from "./utilities.js";
import readTxtFileToArray from "./readFromTxt.js";

const data_file_which = "D:\\MyProject\\JS\\resource\\data_file.txt";
const data_file = await readTxtFileToArray(data_file_which);
console.log(data_file[0])

const accounts = getValueFromJSON(data_file[0], "accounts");
const communities0 = getValueFromJSON(data_file[1], "communities0");
const communities1 = getValueFromJSON(data_file[1], "communities1");
const communities2 = getValueFromJSON(data_file[1], "communities2");
const communities3 = getValueFromJSON(data_file[1], "communities3");
console.log("accounts num is:", accounts.length);
console.log("communities0: ", communities0);
console.log("communities1: ", communities1);
console.log("communities2: ", communities2);
console.log("communities3: ", communities3);

console.log("need: ", Math.ceil(accounts.length / 4));