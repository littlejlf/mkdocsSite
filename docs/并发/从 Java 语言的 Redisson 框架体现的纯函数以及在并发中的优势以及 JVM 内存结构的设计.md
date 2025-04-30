# 从 Java 语言的 Redisson 框架体现的纯函数以及在并发中的优势以及 JVM 内存结构的设计

## 1. 引入：一个简单的 Redisson 示例

```java
public void incrementCounter(String key, int v) {
    RAtomicLong counter = redissonClient.getAtomicLong(key);
    long newValue = counter.addAndGet(v);
}
for (int i = 0; i < 100; i++) {
    new Thread(() -> {
        incrementCounter("stock",-1);
    }).start();
}
```

这段代码实现了在分布式环境下对远程计数器的线程安全原子自增，这里体现了 **纯函数思想** 、 **并发优势** ，并且设计背后依赖于 **JVM 内存结构的分区原则**。

------

## 2. 纯函数的体现

### 2.1 什么是纯函数？

- **确定性**：相同输入必然得到相同输出
- **无副作用**：执行过程不影响外部任何状态
- 在标准的纯函数语言中，如Haskell直接取消变量的概念，从而取消状态来达到纯函数的性质；在Java中也常常用fianl等修饰变量，但是存在不同，当final修饰的是一个对象时，只是锁定了其引用，仍然可以修改其状态，只是取消了部分的状态（及引用值本身）

### 2.2 Redisson 中纯函数特性

在源码实现中：

```java
public RAtomicLong getAtomicLong(String name) {
    return new RedissonAtomicLong(this.commandExecutor, name);
}

public long addAndGet(long delta) {
    return (Long)this.get(this.addAndGetAsync(delta));
}
```

**体现无状态特性：**

- `getAtomicLong` 每次调用都 new 一个新对象，不保存历史状态，也不改变 RedissonClient 本身的状态
- 输入是 `name`，输出是根据 `name`和 `commandExecutor` 生成的新对象，真正做到了 **输入决定输出，无任何副作用**。

**体现纯函数特性：**

- `addAndGet(delta)` 根据输入 `delta`，进行原子操作，没有依赖本地历史状态
- 没有修改本地对象（如本地统计器）
- 结果只取决于输入发送给 Redis 并返回

------

## 3. 并发中的优势

### 3.1 避免共享可变状态

- RedissonClient 无状态设计，多线程无需加锁

### 3.2 Redis 单线程原子性保证

- Redis 命令在服务端单线程一次一条执行

### 3.3 应用场景

多线程实例，每次 `addAndGet(1)` 最终加和精确，无需本地同步。

------

## 4. JVM 内存结构与并发模型

### 4.1 JVM运行时内存区域

| 区域         | 说明                                     | 是否线程共享 |
| ------------ | ---------------------------------------- | ------------ |
| 程序计数器   | 指向当前字节码指令                       | 不共享       |
| Java虚拟机栈 | 存放局部变量、调用链信息                 | 不共享       |
| 堆内存       | 存放 new 对象实例                        | 共享         |
| 方法区       | 存放类元数据（字段、方法、常量、类结构） | 共享         |
| 本地方法栈   | 执行 Native 方法                         | 不共享       |

### 4.2 调用过程

- PC计数器：指向 `addAndGet`
- Java堆栈：新建栈帧，存放局部变量（key）
- 堆：分配 RAtomicLong 和其他对象
- 方法区：全线程共用方法定义

### 4.3 JVM设计在并发中的意义

方法内的本地变量依靠 JVM 堆栈，是线程私有的；同时，`new` 语句每次执行都会在堆内存重新分配对象。这样设计保证了，即使在高并发环境下，方法的本地变量也不会存在共享状态，从而避免带来并发错误。

```java
public void createUser() {
    User user = new User(); // new 对象，分配在堆
    user.setName(Thread.currentThread().getName());
    System.out.println(user);
}

for (int i = 0; i < 100; i++) {
    new Thread(() -> {
        createUser();
    }).start();
}
```

- 每个线程调用 `createUser`，都在堆内新建独立对象 `User`，不共享。
- 本地变量 `user` 依靠堆栈，线程安全，没有并发冲突；不同线程间的user属于不同对象，不涉及共享状态。

------

## 5. 结论

Redisson 框架显示了：

- 纯函数思维有助于并发算法设计
- 无状态设计优化多线程调用
- JVM 内存分区保证了执行独立性与资源共享

**函数式思想 + JVM设计，是现代高并发程序不可或缺的基石！**