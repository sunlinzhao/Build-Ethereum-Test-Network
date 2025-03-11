import pickle
from datetime import datetime
from itertools import combinations

import hypernetx as hnx
from communities.visualization import draw_communities

from Louvain_improved import louvain_method
from communities.algorithms import louvain_method as ml
from compute import get_info, flath, p_distribute_from_adjmat
import numpy as np

from mydraw.plot_from_hedges import plot_G, plot_HG, plot_d_d
from process_data import data2incidmat
from utilities import modularity_matrix
from generator import tx_seq
import json

if __name__ == "__main__":
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

    # incidmat = data2incidmat.convert(hedges).values.copy()
    # adjmat = data2incidmat.incidence_matrix_to_adjacency_matrix(incidmat)
    #
    # with open(r"data_txt.txt", "w") as file:
    #     for i in range(adjmat.shape[0]):
    #         for j in range(adjmat.shape[1]):
    #             if adjmat[i][j] > 0:
    #                 line = str(i) + " " + str(j) + " " + str(adjmat[i][j])
    #                 file.write(line)
    #                 file.write('\n')

    # with open(r'dataSet\Processed\BTC_hedges2.pickle', 'rb') as pkl_file:
    #     hedges1 = pickle.load(pkl_file)

    # with open(r'dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
    #     hedges2 = pickle.load(pkl_file)
    #
    # with open(r'dataSet/Processed/EOS_hedges1.pickle', 'rb') as pkl_file:
    #     hedges3 = pickle.load(pkl_file)

    # # H = hnx.Hypergraph(hedges)
    # # print(H.shape)
    # sub_hedges, T_list, N_list, T_txs, incidmat, adjmat, T = get_info(hedges, 2, 5000, None)
    # sub_hedges1, _, _, _, _, adjmat, _ = get_info(hedges1, 2, 1000, None)
    # sub_hedges2, _, _, _, _, adjmat, _ = get_info(hedges2, 2, 1000, None)
    # sub_hedges3, _, _, _, _, _, _ = get_info(hedges3, 2, 10000, None)
    #
    # print(sub_hedges)
    # print(N_list)
    # print(len(N_list))
    # print(T_list)

    # plot_G(sub_hedges)
    # plot_d_d(sub_hedges)
    # plot_HG(sub_hedges)

    # M = modularity_matrix(adjmat)
    # C = np.zeros_like(M)
    #
    # # 分割数组成小组
    # arr = [i for i in range(len(N_list))]
    # arr = np.array(arr)
    # np.random.shuffle(arr)
    # communities = [arr[i:i + 10] for i in range(0, len(arr), 10)]
    #
    # for community in communities:
    #     for i, j in combinations(community, 2):
    #         C[i, j] = 1.0
    #         C[j, i] = 1.0
    #
    # flath(C, T_list, T_txs, communities)

    # communities0, frames0 = louvain_method(adjmat, T_list=T_list, T_txs=T_txs, a=0.4, b=0.6)
    # print("frames0", frames0)
    # print("communities0", communities0)
    #
    # communities1, frames1 = ml(adjmat)
    # print("frames1", frames1)
    # print("communities1", communities1)
    # #
    # draw_communities(adjmat, communities0)
    # draw_communities(adjmat, communities1)
    #
    # pp = p_distribute_from_adjmat(adjmat)
    #
    # seqs = tx_seq(pp, 2)
    # print(seqs)
    #
    # # 将集合列表转为字符串，并替换大括号
    # data_str = str(communities1).replace('{', '[').replace('}', ']')
    # # 将字符串写入文本文件
    # with open(r'result\communities.txt', 'w') as file:
    #     file.write(data_str)
    #
    # # 将字符串写入文本文件
    # with open(r'result\tx_seq.txt', 'w') as file:
    #     file.write(str(seqs))

    # file_path = r"D:\MyProject\Python\Community_Detection\result\1704956929\info\EOS.json"
    #
    # with open(file_path) as file:
    #     data = json.load(file)
    #     accounts = data["accounts"]
    #
    # print(len(accounts))

    import matplotlib.pyplot as plt
    import numpy as np

    # 生成一些示例数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 创建子图
    fig, axes = plt.subplots(2, 1, figsize=(8, 6))

    # 在每个子图中绘制曲线
    axes[0].plot(x, y1, label='Sin(x)')
    axes[1].plot(x, y2, label='Cos(x)')

    # 在子图中添加自定义标签
    axes[0].text(5, 0.8, 'Custom Label 1', fontsize=12, color='red')
    axes[1].text(5, -0.8, 'Custom Label 2', fontsize=12, color='blue')

    # 设置标题、标签等
    axes[0].set_title('Subplot 1')
    axes[1].set_title('Subplot 2')

    axes[1].set_xlabel('X-axis')

    # 添加图例
    axes[0].legend()
    axes[1].legend()

    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()
