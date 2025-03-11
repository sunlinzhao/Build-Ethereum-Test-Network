import json
import time

from process_experimental_result.process_data import get_data_json, divie_Tx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib
import warnings
from matplotlib import rcParams

# 配置中文字体为宋体，并设置字体大小为五号
rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为宋体
rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示问题
rcParams['font.size'] = 15  # 五号字体，对应大约 10.5 pt

# 忽略 Matplotlib 特定的警告
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)


# 计算实验结果
def get_compute_data(data_dir):
    # 读取数据
    results = get_data_json(data_dir)

    # 3个数据集，4个方法
    cst_ratio = [[[] for j in range(4)] for i in range(3)]  # 跨分片交易比例
    shard_num = [[[] for j in range(4)] for i in range(3)]  # 分片数量
    throughputs = [[[] for j in range(4)] for i in range(3)]  # 平均吞吐量
    latencys = [[[] for j in range(4)] for i in range(3)]  # 平均交易延迟
    max_latencys = [[[] for j in range(4)] for i in range(3)]  # 最大交易延迟
    CST_matrixs = [[[] for j in range(4)] for i in range(3)]  # CST分片间联系对比
    CST_distribute = [[[] for j in range(4)] for i in range(3)]  # CST各分片的分布
    for result in results:
        idx = 0
        if result["dataset"] == "BTC":
            idx = 0
        elif result["dataset"] == "ETH":
            idx = 1
        elif result["dataset"] == "EOS":
            idx = 2
        # if result["dataset"] == "EOS":
        #     continue

        # 跨分片交易率
        total_tx = len(result["Tx"])
        cst = sum(result["CST"])
        cst_ratio[idx][result["index"]].append(cst / total_tx)

        # CST 每个分片的分布
        CST_distribute[idx][result["index"]].append(result["CST"])

        # 分片数量
        communities = result["communities"]
        shard_num[idx][result["index"]].append(len(communities))

        # 平均吞吐量
        throughput_list = result["Throughputs"]
        throughput = sum([sum(temp) / len(temp) for temp in throughput_list if len(temp) != 0])
        if result["methods"] == "Random":
            # 随机划分的吞吐量应降低
            throughput = throughput / max([len(temp) for temp in throughput_list])
        throughputs[idx][result["index"]].append(throughput)

        # 平均交易延迟
        latency_list = result["AverageDelays"]
        latency_one = [sum(temp) / len(temp) for temp in latency_list if len(temp) != 0]
        latency_all = sum(latency_one) / len(latency_one)
        latencys[idx][result["index"]].append(latency_all / 1000)  # 毫秒转换成秒

        # 最大交易延迟
        max_latency_list = result["AverageDelays"]
        max_latency_one = [max(temp) for temp in max_latency_list if len(temp) != 0]
        max_latency_all = sum(max_latency_one) / len(max_latency_one)
        max_latencys[idx][result["index"]].append(max_latency_all / 1000)  # 毫秒转换成秒

        # CST分片间对比热力图
        Tx = result["Tx"]
        shards = result["communities"]
        shard_assignment, unassigned_combinations, shards_counts, CST_matrix = divie_Tx(shards, Tx)
        CST_matrixs[idx][result["index"]].append(CST_matrix)

    # 保存数据
    data = {
        "cst_ratio": cst_ratio,
        "shard_num": shard_num,
        "throughputs": throughputs,
        "latencys": latencys,
        "max_latencys": max_latencys,
        "CST_matrixs": [[[ttt.tolist() for ttt in tt] for tt in temp] for temp in CST_matrixs],
        "CST_distribute": CST_distribute
    }
    file_path = r'D:\MyProject\Python\Community_Detection\result\computed_result_' + str(time.time()) + ".json"
    # 将字符串写入文本文件
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=None)
    return cst_ratio, shard_num, throughputs, latencys, max_latencys, CST_matrixs, CST_distribute


def draw_result(cst_ratio, shard_num, throughputs, latencys, max_latencys, CST_matrixs, CST_distribute):
    # ["#D9958F", "#7E649E", "#31859B"]
    x = [[10, 20, 30, 40, 50], [5, 10, 20, 30, 40], [5, 10, 15, 20, 25]]
    colors = ['#D9958F', '#7E649E', '#31859B', 'black']
    linestyle = ['-', '--', '-.', ':']
    dots = ['^', 'o', 's', '+']
    labels = ["TALA", "TxAllo", "ShardCutter", "Random"]
    dataset = ["Bitcoin", "Ethereum", "Eosio"]
    dataset_num = 3
    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 5))
    for k in range(dataset_num):  # 3 个数据集
        for i, line in enumerate(cst_ratio[k]):
            plt.subplot(1, dataset_num, k + 1)
            plt.plot(x[k], line, marker=dots[i], linestyle=linestyle[i], color=colors[i], label=labels[i], linewidth=1.5)

            # 添加标题和标签
            plt.title(dataset[k], y=-0.25)
            plt.xlabel('分片数量（个）')
            plt.ylabel('跨分片交易比例')
            plt.xticks(x[k])
    # plt.suptitle("跨分片交易比例对比")

    # 显示一个图例在图片右上角外部
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # 调整子图之间的间距
    plt.tight_layout()

    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 5))
    for k in range(dataset_num):
        for i, line in enumerate(throughputs[k]):
            plt.subplot(1, dataset_num, k + 1)
            plt.plot(x[k], line, marker=dots[i], linestyle=linestyle[i], color=colors[i], label=labels[i])

            # 添加标题和标签
            plt.title(dataset[k], y=-0.25)
            plt.xlabel('分片数量（个）')
            plt.ylabel('吞吐量（tx/s）')
            plt.xticks(x[k])
    # plt.suptitle("平均交易吞吐量对比")

    # 显示一个图例在图片右上角外部
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # 调整子图之间的间距
    plt.tight_layout()

    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 5))
    for k in range(dataset_num):
        for i, line in enumerate(latencys[k]):
            plt.subplot(1, dataset_num, k + 1)
            plt.plot(x[k], line, marker=dots[i], linestyle=linestyle[i], color=colors[i], label=labels[i])

            # 添加标题和标签
            plt.title(dataset[k], y=-0.25)
            plt.xlabel('分片数量（个）')
            plt.ylabel('延迟（s）')
            plt.xticks(x[k])
    # plt.suptitle("平均交易延迟对比")
    # 显示一个图例在图片右上角外部
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # 调整子图之间的间距
    plt.tight_layout()

    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 5))
    for k in range(dataset_num):
        for i, line in enumerate(max_latencys[k]):
            plt.subplot(1, dataset_num, k + 1)
            plt.plot(x[k], line, marker=dots[i], linestyle=linestyle[i], color=colors[i], label=labels[i])

            # 添加标题和标签
            plt.title(dataset[k], y=-0.25)
            plt.xlabel('分片数量（个）')
            plt.ylabel('延迟（s）')
            plt.xticks(x[k])
    # plt.suptitle("最大交易延迟对比")
    # 显示一个图例在图片右上角外部
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # 调整子图之间的间距
    plt.tight_layout()

    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 10))
    idx = [4, 4, 4]
    for k in range(dataset_num):
        matrixs = [temp[idx[k]] for temp in CST_matrixs[k]]
        for i, mat in enumerate(matrixs):
            plt.subplot(3, 4, 4 * k + i + 1)
            # 使用 seaborn 绘制热力图
            sns.heatmap(mat, cmap='viridis', annot=False, fmt='.2f', cbar=i == 3, cbar_kws={'label': '相关度'})
            # if k == 0:
            #     plt.title(labels[i])
            # if i == 0:
            #     # 在每个 y 轴标签位置旁添加自定义标签
            #     plt.text(-17+k*3, 20, dataset[k], ha='center', va='center')  # 调整位置和对齐方式
            # 调整显示方式
            if k == 0:
                plt.title(labels[i])
            if k == 2:
                plt.xlabel('分片编号')
            if i == 0:
                plt.ylabel(dataset[k])
                plt.yticks(rotation=0) # 刻度水平显示
            if i != 0:
                plt.yticks([]) # 不显示刻度
            if k != 2:
                plt.xticks([])  # 不显示刻度

    # 调整子图之间的间距
    plt.tight_layout()

    # ------------------------------------------------------------------------
    plt.figure(figsize=(15, 10))
    for k in range(dataset_num):
        distribute = [temp[4] for temp in CST_distribute[k]]
        for i, dis in enumerate(distribute):
            plt.subplot(3, 4, 4 * k + i + 1)
            # 绘制直方图分布
            plt.bar(x=[i for i in range(len(dis))], height=dis, color=colors[k])
            # plt.title(labels[i])
            # plt.xlabel('分片编号')
            # 设置y轴刻度
            plt.yticks([i for i in range(0, 60, 10)])
            if k == 0:
                plt.title(labels[i])
            if k == 2:
                plt.xlabel('分片编号')
            if i == 0:
                plt.ylabel(dataset[k] + '\nCST数量')
                # plt.ylabel('CST数量')
                plt.yticks(rotation=0) # 刻度水平显示
            if i != 0:
                plt.yticks([]) # 不显示刻度
            # print(dis)
    # 调整子图之间的间距
    plt.tight_layout()


    # 显示图形
    plt.show()


if __name__ == '__main__':
    # dict_data = {
    #     "CST": CST,
    #     "transactionTimestamps": transactionTimestamps,
    #     "Delays": Delays,
    #     "blockTimestamps": blockTimestamps,
    #     "blockTimes": blockTimes,
    #     "Throughputs": Throughputs,
    #     "AverageDelays": AverageDelays,
    #     "Tx": Tx,
    #     "communities": communities,
    #     "data_file": data_file,
    #     "dataset": dataset,
    #     "methods": methods,
    #     "index": index,
    #     "accounts_count": accounts_count
    # }

    data_dir = r'D:\MyProject\JS\resource\result'
    cst_ratio, shard_num, throughputs, latencys, max_latencys, CST_matrixs, CST_distribute = get_compute_data(data_dir)
    draw_result(cst_ratio, shard_num, throughputs, latencys, max_latencys, CST_matrixs, CST_distribute)
    for i in cst_ratio:
        print(i)

# ["#D9958F", "#7E649E", "#31859B"]