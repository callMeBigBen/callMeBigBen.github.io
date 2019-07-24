# 2019-07-23-Java容器源码阅读——ArrayList

- transient关键字：使用在实现了序列化接口的类中，修饰field，被修饰的field

在调用序列化方法的时候，不会被持久化。

- ArrayList底层用数组实现。transient Object[] elementData；这是实际存储ArrayList值的数组
  - 由于数组的大小是静态的，所以ArrayList通过扩容和trimToSize()方法来实现底层数组的伸缩
  - IndexOf()采取顺序遍历

- 趣味问题...
  ![1563933395550](127.0.0.1/C:/Users/10421/AppData/Roaming/Typora/typora-user-images/1563933395550.png)

  ![1563933488366](127.0.0.1/C:/Users/10421/AppData/Roaming/Typora/typora-user-images/1563933488366.png)

