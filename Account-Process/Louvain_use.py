import pickle

import numpy as np
from communities.algorithms import louvain_method
# from Louvain_improved import louvain_method
from compute import get_info

from process_data import data2incidmat
from communities.visualization import draw_communities

# hedges = {
#     0: ('FN', 'TH'),
#     1: ('TH', 'JV'),
#     2: ('BM', 'FN', 'JA'),
#     3: ('JV', 'JU', 'CH', 'BM'),
#     4: ('JU', 'CH', 'BR', 'CN', 'CC', 'JV', 'BM'),
#     5: ('TH', 'GP'),
#     6: ('GP', 'MP'),
#     7: ('MA', 'GP')
# }

with open(r'dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
    hedges = pickle.load(pkl_file)

sub_hedges, T_list, N_list, T_txs, incidmat, adjmat, T = get_info(hedges, 6, 25)

'''
- adj_matrix (numpy.ndarray): Adjacency matrix representation of your graph
- n (int or None, optional (default=None)): Terminates the search once this number of communities is detected; 
    if None, then the algorithm will behave normally and terminate once modularity is maximized
'''
communities, frames = louvain_method(adjmat)
print(frames)
print(communities)

for temp in frames:
    print(temp['Q'])

draw_communities(adjmat, communities)
