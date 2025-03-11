import pickle
import hypernetx as hnx
import pandas as pd
import numpy as np
from collections import Counter

'''
input [data] format like:
scenes = {
    0: ('FN', 'TH'),
    1: ('TH', 'JV'),
    2: ('BM', 'FN', 'JA'),
    3: ('JV', 'JU', 'CH', 'BM'),
    4: ('JU', 'CH', 'BR', 'CN', 'CC', 'JV', 'BM'),
    5: ('TH', 'GP'),
    6: ('GP', 'MP'),
    7: ('MA', 'GP')
}
output [incidence_matrix] 关联矩阵
'''


def convert(data):
    # 过滤nan值
    data = {key: tuple(value for value in values if not pd.isna(value)) for key, values in data.items()}
    # 互换键和值
    flipped_data = {value: key for key, value in data.items()}

    # 创建超图
    H = hnx.Hypergraph(data)

    # 获取节点和边的列表
    nodes = list(H.nodes)
    edges = list(H.edges)

    # 创建一个零矩阵，行是节点，列是边
    incidence_matrix = np.zeros((len(nodes), len(edges)))
    # print("关联矩阵大小（顶点数x超边数）: ", incidence_matrix.shape)
    # 将关联矩阵转换为DataFrame以显示
    df = pd.DataFrame(incidence_matrix, index=nodes, columns=edges, dtype=float)
    # print(df)

    # 统计边频次
    # result1 = {key: value for key, value in scenes.items() if len(value) == 2}
    edgeList = [value for value in data.values()]
    edge_weights = Counter(edgeList)
    # print("频次作为超边权重: ", edge_weights)

    # 填充关联矩阵 : 超边权重作为超边中节点总权重，然后节点均分权重
    for edge, weight in zip(edge_weights.keys(), edge_weights.values()):
        for vertex in edge:
            df.at[vertex, flipped_data[edge]] += (weight / len(edge))
            # print(edge, weight)
    return df


# 将关联矩阵转化为邻接矩阵
def incidence_matrix_to_adjacency_matrix(incidence_matrix):
    # 获取节点数和边数
    num_nodes, num_edges = incidence_matrix.shape

    # 初始化邻接矩阵
    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    # 遍历关联矩阵的列
    for edge_idx in range(num_edges):
        # 找到关联矩阵中 不为0 的节点
        connected_nodes = np.where(incidence_matrix[:, edge_idx] > 0)[0]

        # 对于无向图，将对称位置累加 权重
        if len(connected_nodes) >= 2:
            for i in range(1, len(connected_nodes)):
                adjacency_matrix[connected_nodes[0], connected_nodes[i]] += incidence_matrix[connected_nodes[0]][
                    edge_idx]
                adjacency_matrix[connected_nodes[i], connected_nodes[0]] += incidence_matrix[connected_nodes[0]][
                    edge_idx]

    return adjacency_matrix


if __name__ == "__main__":
    # 用 incidence_dataframe() 库实现
    # with open(r'../dataSet/Processed/EOS_hedges1.pickle', 'rb') as pkl_file:
    #     hedges = pickle.load(pkl_file)

    # result2 = {key: value for key, value in hedges.items() if len(value) >= 2}
    # hedges = dict(list(result2.items())[:1000])

    scenes = {
        0: ('FN', 'TH'),
        1: ('TH', 'JV'),
        2: ('BM', 'FN', 'JA'),
        3: ('JV', 'JU', 'CH', 'BM'),
        4: ('JU', 'CH', 'BR', 'CN', 'CC', 'JV', 'BM'),
        5: ('TH', 'GP'),
        6: ('GP', 'MP'),
        7: ('MA', 'GP')
    }

    h = hnx.Hypergraph(scenes)
    # I, verMap, edgeMap = h.incidence_matrix(weights=True, index=True)
    I = h.incidence_dataframe()
    # print(I)

    # print(convert(scenes))
    print(convert(scenes).values.copy())

    change = incidence_matrix_to_adjacency_matrix(convert(scenes).values.copy())

    print(change)
