import ast
import os
import time

import pandas as pd
import numpy as np
import pickle
import random

import igraph as ig
import hypernetx as hnx
import hypernetx.algorithms.hypergraph_modularity as hmod
import hypernetx.algorithms.generative_models as gm

import warnings

from Louvain_improved import louvain_method
from communities.algorithms import louvain_method as ML
from LPA import lpa, random_partition
from networkx.algorithms.community import label_propagation_communities

from compute import get_info, p_distribute_from_adjmat, flath
import json

# warnings.simplefilter('ignore')
from utilities import modularity_matrix, modularity


def start(index, n):
    time_str = str(int(time.time()))

    # 导入数据
    data_path = [r'dataSet\Processed\BTC_hedges2.pickle', r'dataSet\Processed\ETH_hedges2.pickle',
                 r'dataSet\Processed\EOS_hedges1.pickle']
    name = ["BTC", "ETH", "EOS"]
    data_list = []
    for path in data_path:
        with open(path, 'rb') as file:
            hedges = pickle.load(file)
            data_list.append(hedges)

    degree = 2  # 超边大小上限
    num = n  # 选择超边数量
    a = 0.3
    b = 0.7
    for i, hedges in enumerate(data_list):
        if i != index:
            continue

        # 获取相关信息
        sub_hedges, T_list, N_list, T_txs, incidmat, adjmat, T = get_info(hedges, degree, num, None)

        communities0, frames0 = louvain_method(adjmat, T_list=T_list, T_txs=T_txs, a=a, b=b)
        communities1, frames1 = louvain_method(adjmat, T_list=T_list, T_txs=T_txs, a=1.0, b=0.0)
        communities2 = lpa(adjmat)
        communities3 = random_partition(len(N_list), len(communities1))

        if (len(communities0) < min([len(communities1), len(communities2), len(communities3)])) or (len(
                communities0) < len(communities1)):
            print('break')
            return False
        if communities0 == communities1:
            # or any([len(list(temp)) == 1 for temp in communities0])
            # or (len(communities0) == len(communities1))
            print('break')
            return False

        # communities1, frames1 = ML(adjmat)

        print(communities0)
        print(communities1)
        print(communities2)
        print(communities3)

        q0 = modularity(modularity_matrix(adjmat), communities0)
        f0 = flath(T_list, T_txs, communities0)
        print(q0, f0)

        q1 = modularity(modularity_matrix(adjmat), communities1)
        f1 = flath(T_list, T_txs, communities1)
        print(q1, f1)

        # 将字典元素转为列表
        communities0_list = [list(s) for s in communities0]
        communities1_list = [list(s) for s in communities1]
        communities2_list = [list(s) for s in communities2]
        communities3_list = [list(s) for s in communities3]

        communities_json = {
            "a": a,
            "b": b,
            "communities0": communities0_list,
            "communities1": communities1_list,
            "communities2": communities2_list,
            "communities3": communities3_list,
            "q0": q0,
            "f0": f0,
            "q1": q1,
            "f1": f1,
        }

        info_json = {
            "accounts": N_list,
            "times": T_list,
            "Tx": T_txs,
            "hedges": sub_hedges
        }

        # 概率转移矩阵
        pp = p_distribute_from_adjmat(adjmat)

        mat_json = {
            "p_d": pp.tolist(),
            "adj": adjmat.tolist()
        }

        shard_num = len(communities0)

        # 确保目录存在，如果不存在则创建
        directory = r'result\{}\{}'.format(name[i], time_str + "_" + str(len(communities0)))
        # 创建目录
        os.makedirs(directory, exist_ok=True)

        # 创建文件
        file_path1 = os.path.join(directory, '{}.json'.format("communities"))
        file_path2 = os.path.join(directory, '{}.json'.format("info"))
        file_path3 = os.path.join(directory, '{}.json'.format("mat"))

        # 将字符串写入文本文件
        with open(file_path1, 'w') as json_file:
            json.dump(communities_json, json_file, indent=None)

        with open(file_path2, 'w') as json_file:
            json.dump(info_json, json_file, indent=None)

        with open(file_path3, 'w') as json_file:
            json.dump(mat_json, json_file, indent=None)

        return True


if __name__ == "__main__":
    num_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]
    for i in range(3):
        for n in num_list:
            while not start(i, n):
                continue

