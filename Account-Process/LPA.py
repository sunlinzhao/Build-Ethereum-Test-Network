import random

from networkx.algorithms.community import label_propagation_communities
import networkx as nx


def lpa(adjmat):
    # 创建无向图
    G = nx.Graph()
    # 添加节点
    num_nodes = adjmat.shape[0]
    G.add_nodes_from(range(num_nodes))

    # 添加边
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):  # 避免重复添加边
            if adjmat[i, j] != 0:
                G.add_edge(i, j)
    # 使用 LPA 算法检测社区
    lpa_result = label_propagation_communities(G)
    return list(lpa_result)


def random_partition(num_nodes, num_partitions):
    # 创建分区列表
    partitions = [set() for _ in range(num_partitions)]

    # 随机划分节点到分区
    nodes = list(range(0, num_nodes))  # 从0开始的节点
    random.shuffle(nodes)

    for i, node in enumerate(nodes):
        partition_index = i % num_partitions
        partitions[partition_index].add(node)

    return partitions
