from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import numpy as np
import seaborn as sns

from hypernetx.drawing.util import get_collapsed_size


def plot_HG(hedges):
    # 找到元组元素数量大于2的项
    result2 = {key: value for key, value in hedges.items() if len(value) >= 2}
    result2 = dict(list(result2.items())[:100])
    H = hnx.Hypergraph(result2)

    plt.subplots(figsize=(10, 10))
    kwargs = {'with_node_counts': True}
    # kwargs = {}
    cmap = plt.cm.Blues
    alpha = .8

    sizes = np.array([H.size(e) for e in H.edges()])
    norm = plt.Normalize(sizes.min(), sizes.max())

    edges_kwargs = {
        'facecolors': cmap(norm(sizes)) * (1, 1, 1, alpha),
        'edgecolors': 'black',
        'linewidths': 2
    }
    H_collapsed = H.collapse_nodes()
    colors = [
        'red' if get_collapsed_size(v) > 1 else 'black'
        for v in H_collapsed
    ]
    nodes_kwargs = {
        'facecolors': colors
    }
    hnx.draw(H.collapse_nodes(), with_edge_labels=False, with_node_labels=False, edges_kwargs=edges_kwargs,
             nodes_kwargs=nodes_kwargs, **kwargs, layout=nx.kamada_kawai_layout)
    plt.show()


def plot_G(hedges):
    result1 = {key: value for key, value in hedges.items() if len(value) == 2}
    edgeList = [tuple(value) for value in result1.values()]

    print(edgeList)

    # 从边集构造图
    G = nx.Graph()
    G.add_edges_from(edgeList)

    # 统计边频次
    edge_weights = Counter(edgeList)
    # 提取元组中的所有元素
    nodes = [item for sublist in edgeList for item in sublist]
    node_activity = Counter(nodes)

    # 为节点的大小和边的宽度设置映射
    node_size = [node_activity[node] for node in G.nodes]  # 除以100控制一下画面大小
    edge_width = [edge_weights[edge] for edge in G.edges]

    # 绘制图
    pos = nx.kamada_kawai_layout(G)  # 指定节点位置

    # # 绘制图形
    # nx.draw_networkx(G, pos, with_labels=True, font_weight='bold', node_size=node_size, width=edge_width, node_color='skyblue',
    #         font_color='black', font_size=8, edge_color='gray', linewidths=0.5, alpha=0.7)
    # width=0 不设置连线
    nx.draw_networkx(G, pos, with_labels=False, node_size=node_size, node_color='skyblue', alpha=0.7, width=0)
    # nx.draw_networkx(G, pos, with_labels=False, node_size=20, node_color='red', alpha=0.7, width=1)

    # 显示图形
    plt.show()


def get_d_d(hedges):
    degrees = {}
    for edge in hedges.values():
        for node in edge:
            degrees[node] = degrees.get(node, 0) + 1
    degree_sequence = sorted([d for d in list(degrees.values())], reverse=True)
    return list(degrees.values()), degree_sequence


def plot_d_d(hedges):
    degrees = {}
    for edge in hedges.values():
        for node in edge:
            degrees[node] = degrees.get(node, 0) + 1
    # 绘制度分布图
    degree_sequence = sorted([d for d in list(degrees.values())], reverse=True)
    plt.loglog(degree_sequence, marker='o', linestyle='-', color='b')
    plt.title("Degree distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.show()

    return list(degrees.values()), degree_sequence


def plot_degree_probability(*data_items, labels=None, colors=None):
    """
    绘制账户度分布概率密度图

    Parameters:
        *data_items (list): 输入的数据项列表
        labels (list, optional): 每个数据项对应的标签列表
        colors (list, optional): 每个数据项对应的颜色列表

    Returns:
        None
    """
    # 设置绘图参数
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # 绘制每个数据项的概率密度图
    for i, data in enumerate(data_items):
        label = labels[i] if labels else f'Data {i + 1}'
        color = colors[i] if colors else None

        # sns.kdeplot(data, fill=True, label=label, color=color, alpha=0.7, linewidth=2, edgecolor='black')
        sns.histplot(data, label=label, color=color, alpha=0.7, edgecolor='black')

    # 添加标题和标签
    plt.title('Account Degree Distribution Probability Density')
    plt.xlabel('Degree')
    plt.ylabel('Density')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.show()
