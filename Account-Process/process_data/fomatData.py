"""
- EthereumG1
    以 K-in = K-out = 3 的帐户为中心的以太坊交易网络。
    大小: 21.6 MB
- EthereumG2
    以 K-in = K-out = 4 的帐户为中心的以太坊交易网络。
    大小: 24.1 MB
- EthereumG3
    以 K-in = K-out = 5 的帐户为中心的以太坊交易网络。
    大小: 69.5 MB

addr2Idx.txt 1. (addr2Idx.txt) 节点序号是从数字1开始编号的唯一标识符。
- 行:
    每一行表示把以太坊的账户（地址）映射为一个唯一的编号（ID）
    总和：9,855行

- 列:
    1. addr : 以太坊的账户（地址）
    2.  idx : 编号（ID）
    总和: 2列

LPsubG1_df_sort.pickle
根据所有爬取的交易的交易时间进行排序。
加载这个pickle文件后得到一个DataFrame。（['From', 'To', 'Value','TimeStamp']

- 列:
    1.     Value : 交易金额
    2. Timestamp : 交易时间戳
    3.      From : 交易发送方
    4.        To : 交易接收方


LPsubG1_0.5_TransEdgelist.txt

- 行:
    每一行代表了一条边信息。
    总和: 225,714行

- 列:
    1. from_node_num : 边的起始节点序号
    2.   to_node_num : 边的到达节点序号
    3.         value : 交易额
    4.     timestamp : 时间戳
    总和: 4 列

• LPsubG1_train_test_split_0.5.pickle

数据集划分。
加载这个pickle文件后得到一个set类型。
- 元素:
1. train_test_split['train_edges_pos'] : 训练集中的正样本（边）元组
2. train_test_split['test_edges_pos'] : 测试集中的正样本（边）元组
3. train_test_split['train_edges_false'] : 训练集中的负样本（边）元组
4. train_test_split['test_edges_false'] : 测试集中的负样本（边）元组

#####
# 构造交易超边思路
    condition 1: 时间相同
    condition 2: 发送方相同
按条件分组，每一组就是一个超边
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt


def fomatEthereum():
    # ------------------读取原始数据-------------------------
    # 从 pickle 文件中读取对象
    with open(r'../dataSet/1. Ethereum Partial Transaction Dataset - ok/EthereumG1/LPsubG1_df_sort.pickle', 'rb') as file:
        # 由于Python 2和 Python 3不兼容的问题, 添加 latin1
        frame_data = pickle.load(file, encoding='latin1')

    with open(r'../dataSet/1. Ethereum Partial Transaction Dataset - ok/EthereumG1/LPsubG1_0.5_TransEdgelist.txt', 'r',
              encoding='utf-8') as file:
        edges = file.read()

    # --------------------处理数据--------------------------
    # 删除重复项
    frame_data = frame_data.drop_duplicates()

    # 按照发送和接收地址分组
    # group_by_Address_data = frame_data.groupby(['From', 'To'])

    # 按照时间戳和发送方分组
    group_by_Time_data = frame_data.groupby(['TimeStamp', 'From'])

    # 按照时间戳和接收方分组 (重复表示)
    # group_by_Time_data = frame_data.groupby(['TimeStamp', 'To'])

    # -------------------构造超边集---------------------------
    # 存储结果的列表
    hedges = {}
    for name, group in group_by_Time_data:
        group = group.to_dict(orient='records')  # 转换为字典格式，orient='records'表示每行是一个字典
        # print(group)  # [{'From': 2575.0, 'To': 957.0, 'Value': 500.0, 'TimeStamp': 14896.0}]
        v_set = set()
        v_set.add(group[0]['From'])
        for temp in group:
            v_set.add(temp['To'])
        value = tuple(v_set)
        # 将时间戳作为键，节点组成的边作为值, 节点组成的超边作为值
        hedges.update({group[0]['TimeStamp']: value})
    # 打印结果
    for result in hedges:
        print(result)
        print("\n")
    # 写入文件
    with open(r'../dataSet/Processed/ETH_hedges1.pickle', 'wb') as pkl_file:
        pickle.dump(hedges, pkl_file)

def fomatBitcoin():
    # ------------------读取原始数据-------------------------
    # 读取Excel文件
    excel_file_path = r'../dataSet/2. BitCoin on chain data - ok/100000to199999_Transaction.csv'  # 替换成你的Excel文件路径
    df = pd.read_csv(excel_file_path)

    # --------------------处理数据--------------------------
    # 选择某一列不等于某个值的数据
    filtered_df = df[(df['InputAddrs:Value[]'] != 'coinbase:None') & (df['OutputAddrs:Value[]'] != 'coinbase:None')]

    # 打印数据框的前几行
    print(filtered_df.head())

    # 截取地址，屏蔽交易额 / 使用 .loc 方法可以避免警告，并且能够在原始 DataFrame 上直接进行修改
    filtered_df.loc[:, 'InputAddrs:Value[]'] = filtered_df['InputAddrs:Value[]'].str.split(':').str[0]
    filtered_df.loc[:, 'OutputAddrs:Value[]'] = filtered_df['OutputAddrs:Value[]'].str.split(':').str[0]

    # 打印数据框的前几行
    print(filtered_df.head())

    selected_columns = ['InputAddrs:Value[]', 'OutputAddrs:Value[]', 'Timestamp']
    selected_df = filtered_df[selected_columns]

    # 打印数据框的前几行
    print(selected_df.head())

    # 按照时间戳和发送方分组
    grouped_df = selected_df.groupby(['Timestamp', 'InputAddrs:Value[]'])

    # 打印分组后的结果
    print(grouped_df.head())

    # -------------------构造超边集---------------------------
    # 将分组后的数据转换为字典
    # 存储结果的列表
    hedges = {}
    for name, group in grouped_df:
        group = group.to_dict(orient='records')  # 转换为字典格式，orient='records'表示每行是一个字典
        v_set = set()
        v_set.add(group[0]['InputAddrs:Value[]'])
        for temp in group:
            v_set.add(temp['OutputAddrs:Value[]'])

        value = tuple(v_set)
        # 将时间戳作为键，节点组成的边作为值, 节点组成的超边作为值
        hedges.update({group[0]['Timestamp']: value})

        # 打印结果
    for result in hedges:
        print(result)
        print("\n")
        # 写入文件
    with open(r'../dataSet/Processed/BTC_hedges2.pickle', 'wb') as pkl_file:
        pickle.dump(hedges, pkl_file)

def fomatEthereum2():
    # ------------------读取原始数据-------------------------
    # 读取Excel文件
    excel_file_path = r'../dataSet/3. Ethereum on chain data - ok/0to999999_BlockTransaction.csv'  # 替换成你的Excel文件路径
    df = pd.read_csv(excel_file_path)

    # --------------------处理数据--------------------------
    # 选择某一列不等于某个值的数据, 过滤掉空值与合约交易
    filtered_df = df[(df['from'] != 'None') & (df['to'] != 'None') & (df['fromIsContract'] != '1') & (df['toIsContract'] != '1')]

    # 打印数据框的前几行
    print(filtered_df.head())

    selected_columns = ['from', 'to', 'timestamp']
    selected_df = filtered_df[selected_columns]

    # 打印数据框的前几行
    print(selected_df.head())

    # 按照时间戳和发送方分组
    grouped_df = selected_df.groupby(['timestamp', 'from'])

    # 打印分组后的结果
    print(grouped_df.head())

    # -------------------构造超边集---------------------------
    # 将分组后的数据转换为字典
    # 存储结果的列表
    hedges = {}
    for name, group in grouped_df:
        group = group.to_dict(orient='records')  # 转换为字典格式，orient='records'表示每行是一个字典
        v_set = set()
        v_set.add(group[0]['from'])
        for temp in group:
            v_set.add(temp['to'])

        value = tuple(v_set)
        # 将时间戳作为键，节点组成的边作为值, 节点组成的超边作为值
        hedges.update({group[0]['timestamp']: value})

        # 打印结果
    for result in hedges:
        print(result)
        print("\n")
        # 写入文件
    with open(r'../dataSet/Processed/ETH_hedges1.pickle', 'wb') as pkl_file:
        pickle.dump(hedges, pkl_file)

def foamtEosio():
    # ------------------读取原始数据-------------------------
    # 读取Excel文件
    excel_file_path = r'../dataSet/4. EOS on chain data/eos_transfer_data/eos_transfer0.csv'  # 替换成你的Excel文件路径
    df = pd.read_csv(excel_file_path, header=None)  # header=None 不把第一行视为列名

    # --------------------处理数据--------------------------
    # 选择需要提取的列的索引
    selected_columns = [2, 6, 9]  # 替换成你想要提取的列的索引
    # 提取特定列的数据
    extracted_data = df[selected_columns]
    # 设置列名
    extracted_data.columns = ['time', 'from', 'to']  # 替换成你想要的列名
    # 删除包含空值的行
    filtered_data = extracted_data.dropna()

    # 按照时间和发送方分组
    grouped_data = filtered_data.groupby(['time', 'from'])

    # -------------------构造超边集---------------------------
    # 将分组后的数据转换为字典
    # 存储结果的列表
    hedges = {}

    for name, group in grouped_data:
        group = group.to_dict(orient='records')  # 转换为字典格式，orient='records'表示每行是一个字典
        v_set = set()
        v_set.add(group[0]['from'])
        for temp in group:
            v_set.add(temp['to'])

        value = tuple(v_set)
        # 将时间作为键，节点组成的边作为值, 节点组成的超边作为值
        hedges.update({group[0]['time']: value})

        # 打印结果
    for result in hedges:
        print(result)
        print("\n")
        # 写入文件
    with open(r'../dataSet/Processed/EOS_hedges1.pickle', 'wb') as pkl_file:
        pickle.dump(hedges, pkl_file)




if __name__ == "__main__":
    # fomatBitcoin()
    fomatEthereum2()
    # foamtEosio()
    # 构建超图 / 从字典超边集
    # with open(r'dataSet\Processed\ETH_hedges1.pickle', 'rb') as pkl_file:
    #     hedges = pickle.load(pkl_file)
    #
    # result2 = {key: value for key, value in hedges.items() if len(value) > 2}
    #
    # print(result2)