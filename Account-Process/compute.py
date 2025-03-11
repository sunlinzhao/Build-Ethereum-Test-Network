# 计算交易平稳度
import math
import random
import re
from collections import defaultdict
from datetime import datetime
from itertools import combinations

from process_data import data2incidmat
import numpy as np


# 计算交易平稳度
# def flath(T_list, T_txs, communities):
#     # 使用 where 函数获取值为1的元素的行和列索引
#     # rows, cols = np.where(C == 1.0)
#     # txs = list(zip(rows, cols))
#     # print(txs)
#
#     T = (max(T_list) - min(T_list)) / 60
#
#     # 计算每个社区在时间跨度t内的平均交易量 Si_t_mean, 和时间跨度T内的平均交易量 Si_T_mean
#     tx_sum_list = []  # 每个社区的交易总量
#     Si_t_means = []
#     Si_T_means = []
#     Cumulative = 0.0
#     for community in communities:
#         tx_sum = 0
#         t_list = []
#         for node in community:
#             t_index = idx_T_txs(node, T_txs)
#             if len(t_index) != 0:
#                 t_list.extend([T_list[i] for i in t_index])
#                 # if tuple([i, j]) in txs:
#                 tx_sum += len(t_index)
#         tx_sum_list.append(tx_sum)
#
#         if (len(t_list) == 0):
#             t = 0.0
#         else:
#             t = (max(t_list) - min(t_list)) / 60
#         if t == 0.0:
#             return 0.1
#         Si_t_mean = tx_sum / t
#         Si_t_means.append(Si_t_mean)
#         Si_T_mean = tx_sum / T
#         Si_T_means.append(Si_T_mean)
#         Cumulative += (Si_t_mean - Si_T_mean) ** 2
#         print(t, T, tx_sum)
#     delta = math.sqrt(Cumulative / (T * len(communities)))
#     # if delta == 0.0:
#     #     return 0.0
#     fh = 1 / (1 + math.exp(-0.5 / delta))
#     # print(fh)
#     return fh

# 计算交易平稳度
# 使用区块间隔作为交易平稳度
def flath(T_list, T_txs, communities):
    T = len(set(T_list))

    # 计算每个社区在时间跨度t内的平均交易量 Si_t_mean, 和时间跨度T内的平均交易量 Si_T_mean
    tx_sum_list = []  # 每个社区的交易总量
    Si_t_means = []
    Si_T_means = []
    Cumulative = 0.0
    for community in communities:
        tx_sum = 0
        t_list = []
        for node in community:
            t_index = idx_T_txs(node, T_txs)
            if len(t_index) != 0:
                t_list.extend([T_list[i] for i in t_index])
                tx_sum += len(t_index)
        tx_sum_list.append(tx_sum)

        t = len(set(t_list))
        if t == 0:
            t = 1.0

        Si_t_mean = tx_sum / t
        Si_t_means.append(Si_t_mean)
        Si_T_mean = tx_sum / T
        Si_T_means.append(Si_T_mean)
        Cumulative += (Si_t_mean - Si_T_mean) ** 2
        # print(t, T, tx_sum)
    delta = math.sqrt(Cumulative / (T * len(communities)))
    if delta == 0.0:
        return 0.0
    fh = 1 / (1 + math.exp(-0.5 / delta))
    # print(fh)
    return fh


# 获得交易时间索引
def idx_T_txs(node, T_txs):
    t_index = []
    for i, temp in enumerate(T_txs):
        if len(temp) != 0:
            if node in temp:
                t_index.append(i)
    return t_index


'''
params:
    dict_data: raw data
    d: hedges contain d vertex at least
    b: use n hedges from dict_data
    n: limit the number of nodes by degree of node, if None then anyway
return:
    T_list: time list
    N_list: node list
    T_txs: tx's nods are ranked by time
    incidmat: incidence_matrix
    adjmat: adjacency_matrix
    T: [min_time, max_time]
    hedges: processed certainly hedges
'''


# 从字典超边数据计算得到相关信息
def get_info(dict_data, d, b=None, n=None):
    hedges = {key: value for key, value in dict_data.items() if len(value) >= d}

    if n is not None:
        sub_nodes = get_sub_nodes(hedges, n)
        hedges = get_sub_hedges(hedges, sub_nodes)
    else:
        if b is not None:
            sorted_items = dict(sorted(hedges.items(), key=lambda item: item[0]))
            # 随机生成起始索引
            subset_length = b
            start_index = random.randint(0, len(sorted_items) - subset_length)
            # 获取连续固定长度的子集
            hedges = dict(list(sorted_items.items())[start_index: start_index + subset_length])

            # hedges = dict(list(hedges.items())[:b])

    df_incidmat = data2incidmat.convert(hedges)

    T_list = list(df_incidmat.columns)

    if is_time_string(T_list[0]):
        # 转为时间戳
        T_list = list(map(lambda x: int(datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timestamp()), T_list))

    N_list = list(df_incidmat.index)

    incidmat = df_incidmat.values.copy()
    adjmat = data2incidmat.incidence_matrix_to_adjacency_matrix(incidmat)

    T_txs = []

    # 遍历每一列
    for col in df_incidmat.columns:
        # 找到不为 0 的元素所在的行号
        indices = df_incidmat[df_incidmat[col] != 0].index.to_list()
        if len(indices) != 0:
            for i, temp in enumerate(indices):
                indices[i] = N_list.index(temp)
        # 将行号组成列表并添加到结果列表中
        T_txs.append(list(indices))

    T = [min(T_list), max(T_list)]

    return hedges, T_list, N_list, T_txs, incidmat, adjmat, T


def is_time_string(s):
    # 使用正则表达式来检查是否为时间字符串的可能格式
    time_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    return isinstance(s, str) and re.match(time_pattern, s) is not None


def timestamp_to_time_string(timestamp):
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 使用 strftime 方法将 datetime 对象格式化为字符串
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')


# 从邻接矩阵_计算节点发起交易的概率分布矩阵
def p_distribute_from_adjmat(adjmat: np.array):
    # 计算每一行的和
    row_sums = adjmat.sum(axis=1)
    # 按每一行进行归一化
    p_distribute = adjmat / row_sums[:, np.newaxis]
    return p_distribute


# 依据概率分布矩阵，随机选择下一次交易的节点(行列索引)
def choose_next_node(p_distribute, index):
    return np.random.choice(len(p_distribute[index]), p=p_distribute[index])


# 从超边集 hedges 返回节点度数前 n 的节点子集
def get_sub_nodes(hedges: dict, n: int):
    # 获取超边集中的所有节点
    all_nodes = set(node for hedge in hedges.values() for node in hedge)

    # 检查指定的节点数量是否合法
    if n > len(all_nodes):
        raise ValueError("指定的节点数量超过了超边集中的实际节点数量。")

    # 随机选择指定数量的节点
    # selected_nodes = random.sample(all_nodes, n)

    # 计算超边集中所有节点的度数
    degree_count = defaultdict(int)
    for nodes in hedges.values():
        for node in nodes:
            degree_count[node] += 1

    # 根据度数对节点进行排序，并选取度数最大的 n 个节点
    sorted_nodes = sorted(degree_count.keys(), key=lambda x: degree_count[x], reverse=True)
    sub_nodes = sorted_nodes[:n]

    return sub_nodes


# 返回仅仅包含节点子集的超边子集
def get_sub_hedges(hedges: dict, sub_nodes: list):
    # 从超边集中提取出包含这些节点的超边子集
    sub_hedges = {}
    for timestamp, nodes in hedges.items():
        if len(set(nodes).intersection(set(sub_nodes))) > 1:  # 判断两个集合是否有交集且大于1
            sub_hedges[timestamp] = set(nodes).intersection(set(sub_nodes))  # 保存两个集合的交集

    return sub_hedges


if __name__ == "__main__":
    hedges = {
        0: ('FN', 'TH'),
        1: ('TH', 'JV'),
        2: ('BM', 'FN', 'JA'),
        3: ('JV', 'JU', 'CH', 'BM'),
        4: ('JU', 'CH', 'BR', 'CN', 'CC', 'JV', 'BM'),
        5: ('TH', 'GP'),
        6: ('GP', 'MP'),
        7: ('MA', 'GP')
    }
    sub_hedges, T_list, N_list, T_txs, incidmat, adjmat, T = get_info(hedges, 1, 8)
    p_distribute = p_distribute_from_adjmat(adjmat)
    print(p_distribute)
    print(choose_next_node(p_distribute, 2))
