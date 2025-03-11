import os
import json
import numpy as np

# 获取路径下目录
def get_all_folders(path):
    folders = [f.path for f in os.scandir(path) if f.is_dir()]
    return folders

# 获取路径下文件
def get_all_files(path):
    files = [f.path for f in os.scandir(path) if f.is_file()]
    return files

# 从json文件解析获取数据
def get_data_json(data_dir):
    paths = get_all_folders(data_dir)

    result = []
    for path in paths:
        files = get_all_files(path)
        # 读取 JSON 文件
        with open(files[0], 'r') as file:
            data = json.load(file)
        communities = data["communities"]
        data_file = data["data_file"]
        methods = data["methods"]
        index = data["index"]
        accounts_count = data["accounts_count"]
        dataset = data["dataset"]

        subpaths = get_all_folders(path)

        # ------------------CST---------------------
        cst_path = subpaths[0]
        cst_files = get_all_files(cst_path)

        CST = []  # 跨分片交易

        for cst_file in cst_files:
            # 读取 JSON 文件
            with open(cst_file, 'r') as file:
                data = json.load(file)
            if len(CST) == 0:
                CST = [0 for i in range(0, len(data))]
            CST = [x + y for x, y in zip(CST, data)]

        # ------------------index---------------------
        index_path = subpaths[1]
        index_files = get_all_files(index_path)

        transactionTimestamps = []  # 交易时间戳
        Delays = []
        blockTimestamps = []
        blockTimes = []
        Throughputs = []
        AverageDelays = []

        for index_file in index_files:
            # 读取 JSON 文件
            with open(index_file, 'r') as file:
                data = json.load(file)

            transactionTimestamps.append(data["transactionTimestamps"])
            Delays.append(data["Delays"])
            blockTimestamps.append(data["blockTimestamps"])
            blockTimes.append(data["blockTimes"])
            Throughputs.append(data["Throughputs"])
            AverageDelays.append(data["AverageDelays"])

        # ------------------Tx---------------------
        tx_path = subpaths[2]
        tx_files = get_all_files(tx_path)

        Tx = []

        for tx_file in tx_files:
            # 读取 JSON 文件
            with open(tx_file, 'r') as file:
                data = json.load(file)
            Tx.extend(data)

        dict_data = {
            "CST": CST,
            "transactionTimestamps": transactionTimestamps,
            "Delays": Delays,
            "blockTimestamps": blockTimestamps,
            "blockTimes": blockTimes,
            "Throughputs": Throughputs,
            "AverageDelays": AverageDelays,
            "Tx": Tx,
            "communities": communities,
            "data_file": data_file,
            "dataset": dataset,
            "methods": methods,
            "index": index,
            "accounts_count": accounts_count
        }

        result.append(dict_data)
    return result

def divie_Tx(communities, Tx):
    # 初始化社区分配字典
    community_assignment = [[] for i in range(len(communities))]
    unassigned_combinations = []

    # 遍历组合列表
    for combination in Tx:
        assigned = False

        # 遍历社区列表
        for i, community in enumerate(communities):
            # 检查组合是否完全包含在社区中
            if all(node in community for node in combination):
                community_assignment[i].append(combination)
                assigned = True
                break

        # 如果组合不属于任何社区，则将其列为未分配
        if not assigned:
            unassigned_combinations.append(combination)

    # 统计每个社区的组个数
    community_counts = [len(assignments) for assignments in community_assignment]

    # 创建全零矩阵, 跨分片交易矩阵
    CST_matrix = np.zeros((len(communities), len(communities)))

    for temp in unassigned_combinations:
        index1 = [i for i, sublist in enumerate(communities) if temp[0] in sublist][0]
        index2 = [i for i, sublist in enumerate(communities) if temp[1] in sublist][0]
        community_counts[index1] += 1
        community_counts[index2] += 1
        CST_matrix[index1][index2] += 1
        CST_matrix[index2][index1] += 1

    CST_matrix = (CST_matrix-np.min(CST_matrix)) / (np.max(CST_matrix)-np.min(CST_matrix)) # 最大最小归一化
    return community_assignment, unassigned_combinations, community_counts, CST_matrix

def get_adj_Tx(Tx): # 节点的邻接矩阵
    # 计算节点数，假设节点编号从0开始
    num_nodes = max(max(tx) for tx in Tx) + 1
    # 初始化邻接矩阵
    adj_matrix = np.zeros((num_nodes, num_nodes))

    # 增加权重
    for tx in Tx:
        node1, node2 = tx
        adj_matrix[node1, node2] += 1
        adj_matrix[node2, node1] += 1  # 如果是无向图，需要考虑对称性
    # 计算每列的和
    # column_sums = adj_matrix.sum(axis=0)
    # 使用列和进行归一化
    # normalized_adj_matrix = adj_matrix / column_sums

    # 使用总和归一化
    normalized_adj_matrix = adj_matrix / np.sum(adj_matrix)

    return normalized_adj_matrix

if __name__ == '__main__':
    data_dir = r'D:\MyProject\JS\resource\result'
    result = get_data_json(data_dir)

    C = result[3]["communities"]
    Tx = result[3]["Tx"]

    community_assignment, unassigned_combinations, community_counts, CST_matrix = divie_Tx(C, Tx)

    print(CST_matrix)



    # print(get_adj_Tx(result[0]["Tx"]))


