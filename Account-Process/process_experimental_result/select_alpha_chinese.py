# 参数 alpha 的选取
import json
import os
import matplotlib.pyplot as plt
import matplotlib
import warnings
import numpy as np
from matplotlib import rcParams

# 配置中文字体为宋体，并设置字体大小为五号
rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为宋体
rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示问题
rcParams['font.size'] = 18  # 五号字体，对应大约 10.5 pt

# 忽略 Matplotlib 特定的警告
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)


# 获取路径下目录
def get_all_folders(path):
    folders = [f.path for f in os.scandir(path) if f.is_dir()]
    return folders


# 获取路径下文件
def get_all_files(path):
    files = [f.path for f in os.scandir(path) if f.is_file()]
    return files


def compute_std(communities):
    shard_num = len(communities)
    all_account = 0
    for shard in communities:
        all_account += len(shard)
    mean_a = all_account / shard_num
    acc = 0
    for shard in communities:
        acc += pow(len(shard) - mean_a, 2)
    std = pow(acc / shard_num, 0.5)
    return std


# 读取文件
def read_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        a = data["a"]
        b = data["b"]
        communities = data["communities0"]
        q = data["q0"]
        f = data["f0"]
        len_c = len(communities)
        std = compute_std(communities)
    return a, b, communities, q, f, len_c, std


def process_data(dir_path):
    # 待返回数据
    A = [[] for i in range(3)]  # 顺序 BTC ETH EOS
    B = [[] for i in range(3)]
    Communities = [[] for i in range(3)]
    Q = [[] for i in range(3)]
    F = [[] for i in range(3)]
    Len_C = [[] for i in range(3)]
    STD = [[] for i in range(3)]

    # 处理数据
    alpha_folders = get_all_folders(dir_path)
    for alpha_folder in alpha_folders:
        dataset_folders = get_all_folders(alpha_folder)
        for dataset_folder in dataset_folders:
            shard_folders = get_all_folders(dataset_folder)
            for shard_folder in shard_folders:
                files = get_all_files(shard_folder)
                file = files[0]
                a, b, communities, q, f, len_c, std = read_file(file)
                index = 0
                if "BTC" in file:  # 判断属于哪个数据集
                    index = 0
                elif "ETH" in file:
                    index = 1
                elif "EOS" in file:
                    index = 2
                A[index].append(a)
                B[index].append(b)
                Communities[index].append(communities)
                Q[index].append(q)
                F[index].append(f)
                Len_C[index].append(len_c)
                STD[index].append(std)
    return A, B, Communities, Q, F, Len_C, STD


def get_info_Std_mean(A, B, Communities, Q, F, Len_C, STD):  # 标准差，不同超边数量均值
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    Std_collect = [[0 for i in range(7)] for j in range(3)]
    count = [[0 for i in range(7)] for j in range(3)]
    i = 0
    for a_set, std_set in zip(A, STD):  # 不同数据集
        for a, std in zip(a_set, std_set):  # 不同a值
            j = a_index.index(a)
            Std_collect[i][j] += std
            count[i][j] += 1
        k = 0
        for std_acc, num in zip(Std_collect[i], count[i]):
            Std_collect[i][k] = std_acc / num
            k += 1
        i += 1

    return Std_collect


def get_info_Std(A, STD):  # 标准差，不同超边数量
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    Std_collect = [[[] for i in range(7)] for j in range(3)]
    i = 0
    for a_set, std_set in zip(A, STD):  # 不同数据集
        for a, std in zip(a_set, std_set):  # 不同a值
            j = a_index.index(a)
            Std_collect[i][j].append(std)
        i += 1
    return Std_collect


# ---------------------- 绘图 ------------------------

# 绘制标准差
def show_std(Std_collect):
    datasets = ["BTC", "ETH", "EOS"]
    # 定义标签
    labels = ["α=0.2", "α=0.3", "α=0.4", "α=0.5", "α=0.6", "α=0.7", "α=0.8"]
    x = [i for i in range(1, 13)]
    x_labels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]  # 超边数量

    # 创建图形和子图
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 创建3个子图

    # 确保axs总是可迭代的，即使只有单个子图
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    # 遍历子图
    for i, ax in enumerate(axs):
        # 绘制每条折线
        for j, line in enumerate(Std_collect[i]):
            ax.plot(line, label=labels[j])

        # 添加图例
        ax.legend()
        # 添加横轴和纵轴的标签
        ax.set_xlabel('Number of Hyperedges')  # 横轴标签
        ax.set_ylabel('Standard Deviation')  # 纵轴标签
        # 设置横坐标刻度
        ax.set_xticks(x)  # 设置横坐标刻度的位置
        ax.set_xticklabels(x_labels)  # 设置横坐标刻度的标签
        # 为每个子图添加标题
        # ax.set_title(datasets[i])

    # 添加一个主标题
    fig.suptitle('Comparison of Standard Deviations at Different Values of α')
    # 调整子图布局
    fig.tight_layout()

    # 显示图形
    plt.show()


# 绘制标准差均值
def show_std_mean(Std_collect):
    # 图例标签
    labels = ['BTC', 'ETH', 'EOS']

    # α值
    alpha_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制每条折线
    for i, line in enumerate(Std_collect):
        ax.plot(alpha_values, line, label=labels[i])

    # 添加图例
    ax.legend()

    # 添加横轴和纵轴的标签
    ax.set_xlabel('Alpha Value (α)')
    ax.set_ylabel('Standard Deviation')

    # 设置横坐标刻度
    ax.set_xticks(alpha_values)

    # 为图表添加标题
    ax.set_title('Standard Deviation of BTC, ETH, and EOS vs Alpha Value')

    # 显示图形
    plt.show()


# 绘制q均值
def show_q_mean(Q_collect):
    # 图例标签
    labels = ['BTC', 'ETH', 'EOS']

    # α值
    alpha_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制每条折线
    for i, line in enumerate(Q_collect):
        ax.plot(alpha_values, line, label=labels[i])

    # 添加图例
    ax.legend()

    # 添加横轴和纵轴的标签
    ax.set_xlabel('Alpha Value (α)')
    ax.set_ylabel('q')

    # 设置横坐标刻度
    ax.set_xticks(alpha_values)

    # 为图表添加标题
    ax.set_title('q of BTC, ETH, and EOS vs Alpha Value')

    # 显示图形
    plt.show()


# 绘制f均值
def show_f_mean(F_collect):
    # 图例标签
    labels = ['BTC', 'ETH', 'EOS']

    # α值
    alpha_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制每条折线
    for i, line in enumerate(F_collect):
        ax.plot(alpha_values, line, label=labels[i])

    # 添加图例
    ax.legend()

    # 添加横轴和纵轴的标签
    ax.set_xlabel('Alpha Value (α)')
    ax.set_ylabel('f')

    # 设置横坐标刻度
    ax.set_xticks(alpha_values)

    # 为图表添加标题
    ax.set_title('f of BTC, ETH, and EOS vs Alpha Value')

    # 显示图形
    plt.show()


# 绘制q
def show_q(Q_collect):
    datasets = ["BTC", "ETH", "EOS"]
    # 定义标签
    labels = ["α=0.2", "α=0.3", "α=0.4", "α=0.5", "α=0.6", "α=0.7", "α=0.8"]
    x = [i for i in range(1, 13)]
    x_labels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]  # 超边数量

    # 创建图形和子图
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 创建3个子图

    # 确保axs总是可迭代的，即使只有单个子图
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    # 遍历子图
    for i, ax in enumerate(axs):
        # 绘制每条折线
        for j, line in enumerate(Q_collect[i]):
            ax.plot(line, label=labels[j])

        # 添加图例
        ax.legend()
        # 添加横轴和纵轴的标签
        ax.set_xlabel('Number of Hyperedges')  # 横轴标签
        ax.set_ylabel('q')  # 纵轴标签
        # 设置横坐标刻度
        ax.set_xticks(x)  # 设置横坐标刻度的位置
        ax.set_xticklabels(x_labels)  # 设置横坐标刻度的标签
        # 为每个子图添加标题
        # ax.set_title(datasets[i])

    # 添加一个主标题
    fig.suptitle('Comparison of q Deviations at Different Values of α')
    # 调整子图布局
    fig.tight_layout()

    # 显示图形
    plt.show()


# 绘制f
def show_f(F_collect):
    datasets = ["BTC", "ETH", "EOS"]
    # 定义标签
    labels = ["α=0.2", "α=0.3", "α=0.4", "α=0.5", "α=0.6", "α=0.7", "α=0.8"]
    x = [i for i in range(1, 13)]
    x_labels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]  # 超边数量

    # 创建图形和子图
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 创建3个子图

    # 确保axs总是可迭代的，即使只有单个子图
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    # 遍历子图
    for i, ax in enumerate(axs):
        # 绘制每条折线
        for j, line in enumerate(F_collect[i]):
            ax.plot(line, label=labels[j])

        # 添加图例
        ax.legend()
        # 添加横轴和纵轴的标签
        ax.set_xlabel('Number of Hyperedges')  # 横轴标签
        ax.set_ylabel('f')  # 纵轴标签
        # 设置横坐标刻度
        ax.set_xticks(x)  # 设置横坐标刻度的位置
        ax.set_xticklabels(x_labels)  # 设置横坐标刻度的标签
        # 为每个子图添加标题
        # ax.set_title(datasets[i])

    # 添加一个主标题
    fig.suptitle('Comparison of f Deviations at Different Values of α')
    # 调整子图布局
    fig.tight_layout()

    # 显示图形
    plt.show()


# ---------------------- 绘图 ------------------------

def get_info_q(A, Q):
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    Q_collect = [[[] for i in range(7)] for j in range(3)]
    i = 0
    for a_set, q_set in zip(A, Q):  # 不同数据集
        for a, q in zip(a_set, q_set):  # 不同a值
            j = a_index.index(a)
            Q_collect[i][j].append(q)
        i += 1
    return Q_collect


def get_info_f(A, F):
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    F_collect = [[[] for i in range(7)] for j in range(3)]
    i = 0
    for a_set, f_set in zip(A, F):  # 不同数据集
        for a, f in zip(a_set, f_set):  # 不同a值
            j = a_index.index(a)
            F_collect[i][j].append(f)
        i += 1
    return F_collect


def get_info_q_mean(A, Q):
    datasets = ["BTC", "ETH", "EOS"]
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    Q_collect = [[0 for i in range(7)] for j in range(3)]
    count = [[0 for i in range(7)] for j in range(3)]
    i = 0
    for a_set, q_set in zip(A, Q):  # 不同数据集
        for a, q in zip(a_set, q_set):  # 不同a值
            j = a_index.index(a)
            Q_collect[i][j] += q
            count[i][j] += 1
        k = 0
        for q_acc, num in zip(Q_collect[i], count[i]):
            Q_collect[i][k] = q_acc / num
            k += 1
        i += 1
    return Q_collect


def get_info_f_mean(A, F):
    datasets = ["BTC", "ETH", "EOS"]
    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    F_collect = [[0 for i in range(7)] for j in range(3)]
    count = [[0 for i in range(7)] for j in range(3)]
    i = 0
    for a_set, f_set in zip(A, F):  # 不同数据集
        for a, f in zip(a_set, f_set):  # 不同a值
            j = a_index.index(a)
            F_collect[i][j] += f
            count[i][j] += 1
        k = 0
        for f_acc, num in zip(F_collect[i], count[i]):
            F_collect[i][k] = f_acc / num
            k += 1
        i += 1
    return F_collect


def get_std_q_f_only_BTC(A, Q, F, STD):
    result = []
    # 只取 BTC 数据
    a_set = A[0]
    q_set = Q[0]
    f_set = F[0]
    std_set = STD[0]

    a_index = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    # 标准差均值
    Std_mean_collect = [0 for i in range(7)]
    Std_mean_count = [0 for i in range(7)]

    for a, std in zip(a_set, std_set):  # 不同a值
        j = a_index.index(a)
        Std_mean_collect[j] += std
        Std_mean_count[j] += 1
    k = 0
    for std_acc, num in zip(Std_mean_collect, Std_mean_count):
        Std_mean_collect[k] = std_acc / num
        k += 1

    # q_均值
    Q_mean_collect = [0 for i in range(7)]
    Q_mean_count = [0 for i in range(7)]

    for a, q in zip(a_set, q_set):  # 不同a值
        j = a_index.index(a)
        Q_mean_collect[j] += q
        Q_mean_count[j] += 1
    k = 0
    for q_acc, num in zip(Q_mean_collect, Q_mean_count):
        Q_mean_collect[k] = q_acc / num
        k += 1

    # f_均值
    F_mean_collect = [0 for i in range(7)]
    F_mean_count = [0 for i in range(7)]

    for a, f in zip(a_set, f_set):  # 不同a值
        j = a_index.index(a)
        F_mean_collect[j] += f
        F_mean_count[j] += 1
    k = 0
    for f_acc, num in zip(F_mean_collect, F_mean_count):
        F_mean_collect[k] = f_acc / num
        k += 1
    # 标准差，非均值
    Std_collect = [[] for i in range(7)]
    for a, std in zip(a_set, std_set):  # 不同a值
        j = a_index.index(a)
        Std_collect[j].append(std)

    # q，非均值
    Q_collect = [[] for i in range(7)]
    for a, q in zip(a_set, q_set):  # 不同a值
        j = a_index.index(a)
        Q_collect[j].append(q)

    # f，非均值
    F_collect = [[] for i in range(7)]
    for a, f in zip(a_set, f_set):  # 不同a值
        j = a_index.index(a)
        F_collect[j].append(f)

    result.append(Std_mean_collect)
    result.append(Q_mean_collect)
    result.append(F_mean_collect)
    result.append(Std_collect)
    result.append(Q_collect)
    result.append(F_collect)

    return result


# 只绘制BTC的std、q、f，均值
def show_only_btc_mean(data):
    # 图例标签
    labels = ['标准差均值', '模块度均值（q）', '平稳度均值（f）']
    # 设置线条颜色
    colors = ["#D9958F", "#7E649E", "#31859B"]
    # 设置点标记
    markers = ['o', 's', '^']
    # 设置线型
    linestyles = ['-', '--', '-.']

    # α值
    alpha_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    # 创建图形和子图
    fig, ax = plt.subplots(figsize=(15, 5))

    # 绘制每条折线
    for i, line in enumerate(data):
        # 计算最小值和最大值
        min_value = min(line)
        max_value = max(line)
        # 归一化数据
        normalized_data = [(x - min_value) / (max_value - min_value) for x in line]

        ax.plot(alpha_values, normalized_data, label=labels[i], color=colors[i], marker=markers[i],
                linestyle=linestyles[i], markersize=8, linewidth=2)

    # 添加图例
    ax.legend()

    # 添加横轴和纵轴的标签
    ax.set_xlabel('α')
    ax.set_ylabel('归一化值')

    # 设置横坐标刻度
    ax.set_xticks(alpha_values)

    # 为图表添加标题
    ax.set_title('分片结果平均指标的归一化比较')

    # 开启网格
    # plt.grid(True)
    # 显示图形
    plt.show()


def show_only_btc(data):
    # 子图标题
    titles = ["", "", ""]
    # 设置线条颜色
    colors = ["#D9958F", "r", "#31859B", '#7F7F7F', '#BF9000', '#EA700D', '#7E649E']
    # 设置点标记
    markers = ['o', 's', '^', 'v', '*', '+', 'x']
    # 设置线型
    linestyles = ['--', '-', '--', '--', '--', '--', '--']
    # 设置线宽
    linewidths = [1.5, 3, 1.5, 1.5, 1.5, 1.5, 1.5]
    # y轴标签
    y_labels = ["标准差", "模块度（q）", "平稳度（f）"]
    # 定义标签
    labels = ["α=0.2", "α=0.3", "α=0.4", "α=0.5", "α=0.6", "α=0.7", "α=0.8"]
    x = [i for i in range(20, 160, 10)]
    x_labels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150]  # 超边数量

    # 创建图形和子图i
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))  # 创建3个子图

    # 确保axs总是可迭代的，即使只有单个子图
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    # 遍历子图
    for i, ax in enumerate(axs):
        # 绘制每条折线
        for j, line in enumerate(data[i]):
            ax.plot(x_labels, line, label=labels[j], color=colors[j], linewidth=linewidths[j], marker=markers[j],
                    linestyle=linestyles[j])

        # 添加图例
        ax.legend()
        # 添加横轴和纵轴的标签
        ax.set_xlabel('超边数量（个）')  # 横轴标签
        ax.set_ylabel(y_labels[i])  # 纵轴标签
        # 设置横坐标刻度
        ax.set_xticks(x_labels)  # 设置横坐标刻度的位置
        ax.set_xticklabels(x_labels)  # 设置横坐标刻度的标签

        # 为每个子图添加标题
        # ax.set_title(titles[i])

        # 设置x轴范围，从10开始
        ax.set_xlim(left=10)  # 使用Axes对象的方法设置x轴范围
        # 开启网格
        # ax.grid(True)

    # 添加一个主标题
    # Comparison of the standard deviation, modularity value, and stability value of the shard partitioning results for different values of \(\alpha\).
    fig.suptitle('不同超边数量下分片结果比较')
    # 调整子图布局
    fig.tight_layout()

    # 显示图形
    plt.show()


if __name__ == "__main__":
    dir_path = r"D:\MyProject\Python\Community_Detection\result-alpha"
    A, B, Communities, Q, F, Len_C, STD = process_data(dir_path)

    # 绘制标准差均值
    # Std_collect_mean = get_info_Std_mean(A, B, Communities, Q, F, Len_C, STD)
    # show_std_mean(Std_collect_mean)

    # 绘制标准差
    # Std_collect = get_info_Std(A, STD)
    # show_std(Std_collect)
    #
    # # 绘制Q-F值-均值
    # Q_collect = get_info_q_mean(A, Q)
    # # print(Q_collect)
    # show_q_mean(Q_collect)
    # F_collect = get_info_q_mean(A, F)
    # # print(F_collect)
    # show_f_mean(F_collect)
    #
    # # 绘制Q-F值
    # Q_collect = get_info_q(A, Q)
    # show_q(Q_collect)
    # # print(Q_collect)
    # F_collect = get_info_q(A, F)
    # show_f(F_collect)
    # # print(F_collect)

    # 只要BTC的数据
    result = Std_collect = get_std_q_f_only_BTC(A, Q, F, STD)
    data1 = result[:3]
    show_only_btc_mean(data1)
    data2 = result[3:]
    show_only_btc(data2)
# ["#D9958F", "#7E649E", "#31859B"]