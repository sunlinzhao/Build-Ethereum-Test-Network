import pickle

def count_entries_from_pickle_file(file_path):
    # 从文件中加载 pickle 数据
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    # 计算数据条数
    if isinstance(data, (list, dict, set, tuple)):
        return len(data)
    else:
        return 1  # 如果是单个对象，则返回 1

# 示例
file_path = r'D:\MyProject\Python\Community_Detection\dataSet\Processed\ETH_hedges2.pickle'  # 替换为你的 pickle 文件路径
print("数据条数:", count_entries_from_pickle_file(file_path))
