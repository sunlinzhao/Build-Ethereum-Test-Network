import pickle

import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
from collections import Counter
from hypernetx.drawing.util import get_collapsed_size
import hypernetx.algorithms.hypergraph_modularity as hmod
import hypernetx.algorithms.generative_models as gm
import numpy as np

# 构建超图 / 从字典超边集
# with open(r'../dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
#     hedges = pickle.load(pkl_file)

# with open(r'../dataSet\Processed\BTC_hedges2.pickle', 'rb') as pkl_file:
#     hedges = pickle.load(pkl_file)

with open(r'../dataSet/Processed/EOS_hedges1.pickle', 'rb') as pkl_file:
    hedges = pickle.load(pkl_file)

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

# 从二部图构造超图
# B = nx.Graph()
# B.add_nodes_from([1, 2, 3, 4], bipartite=0)  # 添加边
# B.add_nodes_from(['a', 'b', 'c', 'd'], bipartite=1)  # 添加节点
# # Add edges only between nodes of opposite node sets
# B.add_edges_from([(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (2, 'c'), (3, 'c'), (4, 'a'), (4, 'd')])  # 边和节点的对应关系
# HB = hnx.Hypergraph.from_bipartite(B)
# plt.subplots(figsize=(5, 5))
# hnx.draw(HB)
# plt.show()