# 2019-07-24-JDK容器源码阅读——Hashmap

- 2 major initial paramters:

  1. capacity
  2. load factor: 当hashmap当前size>capacity*load factor时，整个hashmap会rehash，扩容成现在的**两倍**
     - 默认0.75会比较好
- 非同步，多线程访问下当至少有一个线程结构化修改hashmap时，需要自行确保一致性。

  - 结构化修改是指：有改变size的操作，如增删。
  - 如果并不需要异步，那么初始化的时候最好是用Collections.synchronizedMap()方法作为包装方法
- 迭代器是fail-fast
- 冲突项的插入，是头插法，插在链表首部
- 容器的扩容都是需要在内存上重新复制的
- 相对比与Hashtable：
  1. **Hashtable线程安全**
  2. Hashmap允许null key和null value，线程不安全，所以效率上高一点
  3. Hashmap是fail-fast

- 复习一下**堆**：
  - 定义：一颗完全二叉树
  - 最大堆：树中每个节点的值都大于或等于左右子节点的值
  - 最小堆：书中每个节点的值都小于或等于左右子节点的值
- 优先权队列：
  - 定义：零或多个元素的集合，每个元素都有一个优先值属性。我们会对优先权队列执行 1.查找 2.插入 3. 删除的操作
  - 堆是一种能够有效实现优先权队列的数据结构。这时插入和删除直接对**堆顶元素**进行操作