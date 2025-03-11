import numpy as np
import pickle
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd

from compute import get_info
from mydraw.plot_from_hedges import plot_d_d, get_d_d

with open(r'..\dataSet\Processed\BTC_hedges2.pickle', 'rb') as pkl_file:
    hedges1 = pickle.load(pkl_file)

with open(r'..\dataSet\Processed\ETH_hedges2.pickle', 'rb') as pkl_file:
    hedges2 = pickle.load(pkl_file)

with open(r'..\dataSet/Processed/EOS_hedges1.pickle', 'rb') as pkl_file:
    hedges3 = pickle.load(pkl_file)

sub_hedges1, _, _, _, _, _, _ = get_info(hedges1, 2, 20000, None)
sub_hedges2, _, _, _, _, _, _ = get_info(hedges2, 2, 20000, None)
sub_hedges3, _, _, _, _, _, _ = get_info(hedges3, 2, 20000, None)

# 生成正态分布和幂律分布的数据集
d1, x1 = get_d_d(sub_hedges1)
d1 = list(Counter(d1))
d1 = [x / max(d1) for x in d1]
print(d1)

d2, x2 = get_d_d(sub_hedges2)
d2 = [x / max(d2) for x in d2]
d2 = list(Counter(d2))
print(d2)

d3, x3 = get_d_d(sub_hedges3)
d3 = [x / max(d3) for x in d3]
d3 = list(Counter(d3))
print(d3)

# 将数据组合成一个列表
data = [d1, d2, d3]

plt.figure()
# 绘制垂直箱线图，突出显示异常值为红色
plt.boxplot(data, vert=True, showfliers=True, notch=False, patch_artist=False,
            boxprops=dict(color='black'),
            capprops=dict(color='black'),
            whiskerprops=dict(color='black'),
            flierprops=dict(markeredgecolor='red', marker='o', markersize=5),
            medianprops=dict(color='black'))

# 设置坐标轴标签
plt.xticks([1, 2, 3], ['BTC', 'ETH', 'EOS'], fontsize=18)
plt.ylabel('Probability', fontsize=18)

# 显示图形
# plt.title('Boxplots with Outliers Highlighted')
plt.show()

plt.figure()
plt.loglog(x1, linestyle='-', color='r', linewidth=3)
plt.loglog(x2, linestyle='--', color='g', linewidth=3)
plt.loglog(x3, linestyle=':', color='b', linewidth=3)
# plt.title("Degree distribution")
plt.xlabel("Degree", fontsize=18)
plt.ylabel("Frequency", fontsize=18)
plt.legend(['BTC', 'ETH', 'EOS'])
plt.show()

# 将两个列表转换为 DataFrame
df = pd.DataFrame(list(zip(d1, d2, d3)), columns=['BTC', 'ETH', 'EOS'])

plt.figure()
# 创建同时包含平滑小提琴图和箱线图的图表，使用不同的配色方案
plt.figure()
# sns.catplot(kind="violin", bw_method=0.2, palette=["red", "green", "blue"], data=df)
sns.violinplot(data=df, bw_method=0.2, palette=["red", "green", "blue"])
# 绘制箱线图
# 设置异常点的颜色和大小
flierprops = dict(marker='o', markersize=5, markerfacecolor='black', markeredgecolor='black')
sns.boxplot(data=df, color="white", width=0.15, flierprops=flierprops)

plt.ylabel("Probability", fontsize=18)
# plt.xticks(fontsize=18)  # 调整横坐标轴标签的大小

plt.xlabel("DataSet", fontsize=18)
# plt.legend(['BTC', 'ETH', 'EOS'])
plt.show()
