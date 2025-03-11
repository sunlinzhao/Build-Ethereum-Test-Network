import pickle

import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import numpy as np

with open(r'../dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
    hedges = pickle.load(pkl_file)

# with open(r'../dataSet\Processed\BTC_hedges2.pickle', 'rb') as pkl_file:
#     hedges = pickle.load(pkl_file)
#
# with open(r'../dataSet/Processed/EOS_hedges1.pickle', 'rb') as pkl_file:
#     hedges = pickle.load(pkl_file)

result1 = {key: value for key, value in hedges.items() if len(value) == 2}
edgeList = [tuple(value) for value in result1.values()]

print(edgeList)
# 从边集构造图
G = nx.Graph()
# 设置随机数生成器的种子
# seed_value = 42
# np.random.seed(seed_value)

G.add_edges_from(edgeList[:5000])

# 统计边频次
edge_weights = Counter(edgeList)
print(edge_weights)
# 提取元组中的所有元素
nodes = [item for sublist in edgeList for item in sublist]
node_activity = Counter(nodes)
print(node_activity)

# 为节点的大小和边的宽度设置映射
node_size = [node_activity[node] / 100 for node in G.nodes]  # 除以100控制一下画面大小
edge_width = [edge_weights[edge] for edge in G.edges]

# 绘制图
pos = nx.kamada_kawai_layout(G)  # 指定节点位置
# pos = nx.spring_layout(G, k=0.6, iterations=100)  # 指定节点位置

# # 绘制图形
# nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_size, width=edge_width, node_color='skyblue',
#         font_color='black', font_size=8, edge_color='gray', linewidths=0.5, alpha=0.7)
# width=0 不设置连线
nx.draw_networkx(G, pos, with_labels=False, node_size=node_size, node_color='skyblue', alpha=0.7, width=0)
# nx.draw(G, pos, with_labels=False, node_size=8, node_color='red', alpha=0.7, width=1)

# 显示图形
plt.show()

# 考虑要不要去除合约账户
# 1000000to1999999_BlockTransaction.csv 有转给或者接收合约账户的交易，要过滤掉
