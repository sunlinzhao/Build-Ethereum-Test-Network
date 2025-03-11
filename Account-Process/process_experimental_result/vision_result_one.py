import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

from process_experimental_result.process_data import get_data_json, divie_Tx, get_adj_Tx
import matplotlib
import warnings
# 忽略 Matplotlib 特定的警告
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)

# 读取 JSON 文件
data_dir = r'D:\MyProject\JS\resource\result'
result = get_data_json(data_dir)

data = result[1]

CST = data["CST"]
Delays = data["Delays"]
Throughputs = data["Throughputs"]
# 计算每个子列表的元素和和平均值
averages_Throughputs = [sum(filter(None, sublist)) / len(list(filter(None, sublist))) for sublist in Throughputs]

AverageDelays = data["AverageDelays"]
# 计算每个子列表的元素和和平均值
averages_AverageDelays = [sum(filter(None, sublist)) / len(list(filter(None, sublist))) for sublist in AverageDelays]

Tx = data["Tx"]
Communities = data["communities"]
community_assignment, unassigned_combinations, community_counts, CST_matrix = divie_Tx(Communities, Tx)
community_Tx = community_assignment + [unassigned_combinations]

adj = get_adj_Tx(Tx)


def show():
    # ----------------------------------------------------------
    plt.figure()
    # 绘制条形图
    plt.bar(range(len(CST)), CST, color='blue')
    # 设置横轴标签
    plt.xlabel('Number of Shard')
    # 设置纵轴标签
    plt.ylabel('Num of CSTs')
    # 设置标题
    plt.title('Distribution of CSTs')

    # ----------------------------------------------------------
    plt.figure()
    # 将每个子列表的数据分别绘制为折线
    for i, line_data in enumerate(Delays):
        plt.plot(line_data, label=f'Line {i + 1}')

    # 设置横轴标签
    plt.xlabel('Transactions')
    # 设置纵轴标签
    plt.ylabel('Latency/ms')
    # 设置标题
    plt.title('Latency of Transactions')
    # 添加图例
    plt.legend()

    # ----------------------------------------------------------
    plt.figure()
    # 绘制条形图
    plt.bar(range(len(averages_Throughputs)), averages_Throughputs, color='green')
    # 设置横轴标签
    plt.xlabel('Number of Shard')
    # 设置纵轴标签
    plt.ylabel('Throughput/tps')
    # 设置标题
    plt.title('Throughput of Shard')

    # ----------------------------------------------------------
    plt.figure()
    # 绘制条形图
    plt.bar(range(len(averages_AverageDelays)), averages_AverageDelays, color='red')
    # 设置横轴标签
    plt.xlabel('Number of Shard')
    # 设置纵轴标签
    plt.ylabel('Average Latency/ms')
    # 设置标题
    plt.title('Average Latency of Shard')

    # ----------------------------------------------------------
    plt.figure()
    # 绘制散点图
    for i, color_data in enumerate(community_Tx):
        x, y = zip(*color_data)
        plt.scatter(x, y, label=f'Color {i}')
    # 设置横轴标签
    plt.xlabel('X-axis')
    # 设置纵轴标签
    plt.ylabel('Y-axis')
    # 设置标题
    plt.title('Scatter Plot with Multiple Colors')

    # ----------------------------------------------------------
    plt.figure()
    # 绘制条形图
    plt.bar(range(len(community_counts)), community_counts, color='black')
    # 设置横轴标签
    plt.xlabel('Number of Shard')
    # 设置纵轴标签
    plt.ylabel('Num of Transactions')
    # 设置标题
    plt.title('Num of Transactions by Shard')

    # ----------------------------------------------------------
    plt.figure()
    # 使用 seaborn 绘制热力图
    sns.heatmap(adj, cmap='viridis', annot=False, fmt='g', cbar=True)

    # ----------------------------------------------------------
    plt.figure()
    # 使用 seaborn 绘制热力图
    sns.heatmap(CST_matrix, cmap='viridis', annot=True, fmt='.2f', cbar=True)

    # 显示图形
    plt.show()


if __name__ == "__main__":
    show()
