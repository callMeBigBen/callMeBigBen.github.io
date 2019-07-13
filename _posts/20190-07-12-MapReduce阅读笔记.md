# MapReduce

- 什么是MapReduce？

  - 是一个分布式系统的计算模型
  - 由谷歌于2004年在OSDI发布，由Jeff Dean领导

- 有一个问题是：为什么我们需要分布式系统？论文中和6.824的讲义里给的答案是(xjb回忆)：

  > - easy to scale up
  > - achieve security via isolation among physic machines
  > - achieve fault-tolerance via replication
  > - associate isolated machines

- 四个点回答的很全面，但是直接原因肯定还是单个machine的处理能力增速赶不上待处理数据规模的增速， 不采用这种物理分布，逻辑统一的架构形式压根处理不了这些数据了。“穷则思变”

- Why "Map" and "reduce"?
  - come from Lisp functions "map" and "reduce"
- 名字拆分，**map和reduce分别对应的函数，就是整个系统思想中的两个核心，外加上一个控制中心master**
- MapReduce模型中，计算采取
  1. 将大文件split成small trunk
  2. 由若干个worker节点并行处理这些trunk.每个worker一次接受一个trunk，执行计算过程
  3. 所有trunk计算完之后，我们需要把这些一点一点的计算结果合起来返回给client，实现逻辑上的封闭性（外界看不出你用了分布式）（以上的说法实际略去了很多操作，后面会讲）
- Map函数：worker节点处理trunk时执行的函数，就是map函数。这样的worker节点我们也称为mapper。
  - 往细了一点来讲：mapper接收一小份数据，执行定义好的map函数，然后会将结果输出为一个<K,V>对（为什么是键值对？是为了方便reducer的工作，提高性能）。这里我们假设大数据被切分成M个trunk，产生了M个键值对
- Reduce函数: worker节点执行合并计算结果的函数，就是reduce函数。这样的worker节点我们称为reducer。
  - reducer会处理中间的键值对结果，将这些结果合并。reducer的数量一般会显著小于M（废话..不然还叫什么合并）
- Master：控制中心
  - 负责大文件的切分和转发到mapper的过程
  - 负责中间键值对的分配（分配给N个reducer）
  - 负责处理异常

- :) （此处是一张架构图，大家一起来想象)



## MapReduce的差错控制

有这么几种不好的情况：

1. **节点down了**，由于节点的类型，又可分为mapper挂了和reducer挂了
2. 节点没down，但是处理速度慢导致进度落后成为吞吐率短板了，变成**落后节点**
3. **master节点挂了**

这里插一嘴系统怎么判断节点是不是挂了：**master会周期性的ping worker节点**，如果收不到回复，就认为这些节点挂了

我们分别来讲

- 对于mapper挂了的情况，master记录其处理的trunk的信息，将其转发给其他空闲的mapper。**同时，告诉挂掉的mapper对应的reducer，不要到原来那个mapper去等中间键值对结果了，换成现在这个**
- 对应reducer挂了的情况，master将这个reducer的任务**分配给其他的reduce**r。鉴于 Google MapReduce 的结果是存储在 Google File System 上的，已完成的 Reduce 任务的结果的可用性由 Google File System 提供，因此 MapReduce Master 只需要处理未完成的 Reduce 任务即可。
- 节点落后了：master把这个/些节点处理的数据同时**分配给空闲节点，**然后“让他们比赛”，谁**最先算完就取谁的**
- master节点挂了：这个情况出现的比较少，一般会有checkpoint机制，即保留系统snapshot来帮助恢复



## 优化机制

- **数据本地性**：尽量将map任务分配到该任务所处理文件所在地机器上，如果不行，就分配到尽量近的机器上；这么做，因为MapReduce提出来的时候，网络速度是系统的瓶颈，所以系统的设计要尽量避免使用网络交换数据；然而其实到了今天，数据中心的机器间数据交换速度非常块，瓶颈成了磁盘的写入速度。
- 所及今天**新的分布式架构会尽量避开磁盘I/O的缺点，更多的利用内存和网络**（Spark的设计理念）
- 顺着上面这点，还能推测，reducer的位置选取，也是尽量离对应mapper近的好

- **Combiner**：在某些情况下，用户定义的Map任务可能会产生大量重复地中间结果键，同时用户所定义的Reduce函数本身也是满足交换律和结合律的（好难懂啊）
- 在这种情况下，Google MapReduce 系统允许用户声明在 Mapper 上执行的 Combiner 函数：Mapper 会使用由自己输出的R个中间结果 Partition 调用 **Combiner 函数以对中间结果进行局部合并**，减少 Mapper 和 Reducer 间需要传输的数据量。

