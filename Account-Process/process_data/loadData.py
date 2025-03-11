import pickle

import scipy.sparse as sp
import numpy as np


def loadEtherFromNPZ(dataset_dir):
    adj = sp.load_npz(dataset_dir + "ether_adj.npz")
    data = np.load(dataset_dir + "ether_features.npz")
    np.nan_to_num(data['feats'])

    return adj, data['feats'], data['y_train'], data['y_val'], data['y_test'], data['train_index'], data['val_index'], \
           data['test_index'], data['train_target']


if __name__=="__main__":
    # with open(r'dataSet\Processed\ETH_hedges_part.pickle', 'rb') as pkl_file:
    #     hedges = pickle.load(pkl_file)
    # # 找到元组元素数量大于2的项
    # result = {key: value for key, value in hedges.items() if len(value) > 2}



    dataset_dir = "dataSet\\ethereum_dataset\\"

    adj, feats, y_train, y_val, y_test, train_index, val_index, test_index, train_target = loadEtherFromNPZ(dataset_dir)

    print(adj)

    # print(feats)
    # print(y_train)
    # print(y_val)
    # print(y_test)
    # print(train_index)
    # print(val_index)

    # 提取稀疏矩阵的元素值
    elements = adj.data

    # 使用 Counter 统计元素的频次
    from collections import Counter

    element_counts = Counter(elements)

    # 打印结果
    for element, count in element_counts.items():
        print(f"Element {element} has frequency: {count}")
