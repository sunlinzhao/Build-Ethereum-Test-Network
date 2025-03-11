# 数值对比分析
import json

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        cst_ratio = data["cst_ratio"]
        throughputs = data["throughputs"]
        latencys = data["latencys"]
        max_latencys = data["max_latencys"]
    return cst_ratio, throughputs, latencys, max_latencys

def show_non_percent(cst_ratio, throughputs, latencys, max_latencys):
    dataset = ["BTC", "ETH", "EOS"]
    method = ["TALA", "TxAllo", "ShardCutter", "Random"]
    for i, tmp in enumerate(cst_ratio):
        print("【{}】".format(dataset[i]))
        for i, cst in enumerate(tmp):
            print(method[i], end=": ")
            print(sum(cst) / len(cst))
def show_result(cst_results, thr_results, lat_results, m_lat_results):
    dataset = ["BTC", "ETH", "EOS"]
    method = ["TALA", "TxAllo", "ShardCutter"]
    # Cross-Shard Transaction Ratio Reduction (%)
    print(">>>>> Cross-Shard Transaction Ratio Reduction (%) <<<<<")
    for i, tmp in enumerate(cst_results):
        print("【{}】".format(dataset[i]))
        for i, cst in enumerate(tmp):
            print(method[i], end=": ")
            print(cst)
    print("---------------------")

    # Average Throughput Improvement (%)
    print(">>>>> Average Throughput Improvement (%) <<<<<")
    for i, tmp in enumerate(thr_results):
        print("【{}】".format(dataset[i]))
        for i, thr in enumerate(tmp):
            print(method[i], end=": ")
            print(thr)
    print("---------------------")

    # Average Transaction Latency Reduction (%)
    print(">>>>> Average Transaction Latency Reduction (%) <<<<<")
    for i, tmp in enumerate(lat_results):
        print("【{}】".format(dataset[i]))
        for i, lat in enumerate(tmp):
            print(method[i], end=": ")
            print(lat)
    print("---------------------")

    # Maximum Transaction Latency Reduction (%)
    print(">>>>> Maximum Transaction Latency Reduction (%) <<<<<")
    for i, tmp in enumerate(m_lat_results):
        print("【{}】".format(dataset[i]))
        for i, m_lat in enumerate(tmp):
            print(method[i], end=": ")
            print(m_lat)
    print("---------------------")

if __name__ == "__main__":
    # BTC ETH EOS
    # TALA TxAllo ShardCutter / Random
    # 每一项代表不同负载下的指标
    file_path = r"D:\MyProject\Python\Community_Detection\result\computed_result_1721568771.5436833.json"
    cst_ratio, throughputs, latencys, max_latencys = read_file(file_path)

    # 计算与随机划分相比跨分片交易率下降百分比
    cst_results = []
    for temp in cst_ratio:
        cst = temp[:3]
        r_cst = temp[-1]
        cst_result = []
        for t in cst:
            result = [(b_i - a_i) / b_i for a_i, b_i in zip(t, r_cst)]
            cst_result.append(sum(result) / len(result))
        cst_results.append(cst_result)
    # print(cst_results)
    # 计算与随机划分相比平均吞吐量提升
    thr_results = []
    for temp in throughputs:
        thr = temp[:3]
        r_thr = temp[-1]
        thr_result = []
        for t in thr:
            result = [(b_i - a_i) / b_i for a_i, b_i in zip(r_thr, t)]
            thr_result.append(sum(result) / len(result))
        thr_results.append(thr_result)
    # print(thr_results)
    # 计算与随机划分相比平均交易延迟下降
    lat_results = []
    for temp in latencys:
        lat = temp[:3]
        r_lat = temp[-1]
        lat_result = []
        for t in lat:
            result = [(b_i - a_i) / b_i for a_i, b_i in zip(t, r_lat)]
            lat_result.append(sum(result) / len(result))
        lat_results.append(lat_result)
    # print(lat_results)
    # 计算与随机划分相比最大交易延迟下降
    m_lat_results = []
    for temp in max_latencys:
        m_lat = temp[:3]
        r_m_lat = temp[-1]
        m_lat_result = []
        for t in m_lat:
            result = [(b_i - a_i) / b_i for a_i, b_i in zip(t, r_m_lat)]
            m_lat_result.append(sum(result) / len(result))
        m_lat_results.append(m_lat_result)
    # print(m_lat_results)
    show_result(cst_results, thr_results, lat_results, m_lat_results)
    # show_non_percent(cst_ratio, throughputs, latencys, max_latencys)

