# 2019-07-23-JDK容器源码阅读——Arrays

- MIN_ARRAY_SORT_GRAN = $2^{12}$ 。是Arrays工具类处理数组时采取并行模式的长度阈值（会将数组split成小块再并行处理）
- Arrays内置的sort方法使用的是一种组合策略：
  1. 数组长度小于47，则插入排序
  2. 数组长度小于286，则快速排序
  3. 大于286，则归并排序
  4. 如果数组是一个byte类型的数组，并且长度大于29，则使用计数排序
  5. 如果是一个长度大于3200的short或者char类型的数组，则使用计数排序

# 2019-07-23-Java容器源码阅读——ArrayList

- transient关键字：使用在实现了序列化接口的类中，修饰field，被修饰的field

在调用序列化方法的时候，不会被持久化。

- ArrayList底层用数组实现。transient Object[] elementData；这是实际存储ArrayList值的数组
  - 由于数组的大小是静态的，所以ArrayList通过grow()和trimToSize()方法来实现底层数组的伸缩
  - grow()方法每次将容量扩大为当前的**1.5倍**，当超过MAX_ARRAY_SIZE之后，再大只能到Integer.MAX_VALUE了。也就是说..最后一下只增加八个位置
  - MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8
  - IndexOf()采取顺序遍历
- 趣味问题...
  ![1563934473271](C:\Users\10421\AppData\Roaming\Typora\typora-user-images\1563934473271.png)
- modCount:通俗来讲是用来实现interator的共享锁的一个field。在对迭代器每一个方法的调用中，会在方法头尾部检查是否有非迭代器本身的方法调用改变了list的结构（增删改）。因为设计初衷是要保持迭代器和list数据完全一致。这个机制叫做fail fast机制
- fail-fast解决方案：
  1. 结构化操作时synchronize锁住对象
  2. 使用CopyOnWriteArrayList