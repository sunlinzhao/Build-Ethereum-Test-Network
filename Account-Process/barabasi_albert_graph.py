import pickle
import random
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import pandas as pd
import hypernetx.algorithms.hypergraph_modularity as hmod
import numpy as np


def generate(n, m):
    """
    生成 BA 随机图模型

    Parameters:
    - n: 节点数
    - m: 每个新节点连接到现有节点的边数
    - edges: 初始图边集合

    Returns:
    - edges: 生成的 BA 随机图的边集合
    - dd[-1]: 度分布
    """
    # 初始化初始图，这里使用一个初始完全图
    edges = [(i, j) for i in range(m) for j in range(i + 1, m)]

    dd = []
    # 开始添加新节点
    for i in range(m, n):
        # 计算每个现有节点的度
        degrees = {}
        for edge in edges:
            for node in edge:
                degrees[node] = degrees.get(node, 0) + 1
        dd.append(degrees)
        # 根据度的概率分布选择连接的节点
        selected_nodes = random.choices(list(degrees.keys()), weights=degrees.values(), k=m)

        # 将新节点与选定的节点连接
        new_edges = [(i, node) for node in selected_nodes]
        edges.extend(new_edges)

    return edges, dd[-1]


def plot_graph(edges):
    """
    绘制图形

    Parameters:
    - edges: 图的边集合
    """
    G = nx.Graph(edges)
    nx.draw_networkx(G, with_labels=True, font_weight='bold')
    plt.show()


def plot_degree_distribution(degrees):
    # 绘制度分布图
    degree_sequence = sorted([d for d in degrees], reverse=True)
    plt.loglog(degree_sequence, marker='o', linestyle='-', color='b')
    plt.title("Degree distribution of BA Graph")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == "__main__":
    with open(r'dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
        hedges = pickle.load(pkl_file)
    # 过滤nan值
    hedges = {key: tuple(value for value in values if not pd.isna(value)) for key, values in hedges.items()}
    result1 = {key: value for key, value in hedges.items() if len(value) >= 4}
    edgeList = list(result1.values())[:20]

    H = hnx.Hypergraph(edgeList)
    # 生成 BA 随机图模型的边集合
    n = len(H.nodes)  # 节点数
    m = int(max(list(map(lambda x: len(x), edgeList))) / 2)  # 每个新节点连接到现有节点的边数 / 取最大边数一半
    ba_edges, degrees = generate(n, m)
    dict_ba_edges = dict(enumerate(ba_edges))
    # print(dict_ba_edges)


    print(list(degrees.values()))
    # 绘制度分布
    plot_degree_distribution(list(degrees.values()))

    h_ba_edges = dict(enumerate(ba_edges))
    h = hnx.Hypergraph(h_ba_edges)

    # 模块度和聚类的与计算参数
    ht = hmod.precompute_attributes(h)

    # 生成K个随机分区
    K = 5
    V = list(ht.nodes)
    p = np.random.choice(K, size=len(V))
    RandPart = hmod.dict2part({V[i]: p[i] for i in range(len(V))})

    print(hmod.modularity(ht, RandPart))
    # 绘制图形
    plot_graph(ba_edges)