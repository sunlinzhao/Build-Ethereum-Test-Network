# Build-Ethereum-Test-Network

**题目**：《Cross Shard Transaction Optimization Based on Community Detection in Sharded Blockchain Systems》

**摘要**：由于分片区块链系统中跨分片交易处理机制复杂且代 价昂贵以及跨分片交易比例过高，使得分片区块链系统难以达到理想的理论性能 上限。所以本文旨在通过将频繁交易的账户划分到同一分片来降低跨分片交易比 例，从而提高系统吞吐量。本文根据历史交易数据构建账户交易超图，将区块链 的账户划分问题表述为图结构上的社区发现问题。

同时提出一种时间感知的社区 发现算法，考虑交易在时间上的分布均匀程度对账户进行划分，解决了社区发现 算法倾向于划分更大分片的问题。此外，本文搭建了本地以太坊测试网络，并在 真实的交易数据集上实现所提出的算法。实验表明，本文所提出的算法能够将跨 分片交易比例从 95%左右降低至约 10%，同时在交易吞吐量和交易延迟的表现 上优于其它基于社区发现的账户划分算法。



1. **网络架构图**

<img src="https://s2.loli.net/2025/03/11/tiBadZ9yfrD1PEq.png" alt="POA实现架构图" style="zoom:5%;" />

2. **数据集可视化**

![数据集图结构](https://s2.loli.net/2025/03/11/FCBOk3HApSGujyR.png)

3. **账户划分示意图**

<img src="https://s2.loli.net/2025/03/11/3XBdOcCqGDKhyN9.png" alt="社区发现算法的账户划分" style="zoom:5%;" />

4. **测试结果热力图**

<img src="https://s2.loli.net/2025/03/11/uYKb1eJXPdImvzr.png" alt="image-20250311161305224" style="zoom: 67%;" />

5. **测试数据可视化**

<img src="https://s2.loli.net/2025/03/11/nFsmrJx43lLupb6.png" alt="image-20250311161627406" style="zoom:80%;" />

<img src="https://s2.loli.net/2025/03/11/e1nwTE7tVxZPUMf.png" alt="image-20250311161642426" style="zoom:80%;" />

6. **系统流程图**

<img src="https://s2.loli.net/2025/03/11/vxlpa61Tub9JXAq.png" alt="image-20250311161800650" style="zoom:67%;" />
