# ThreadLocal知识总结



## threadlocal与内存泄露



通常情况下，我们创建的变量可以被任何一个线程访问和修改。这在多线程环境中可能导致数据竞争和线程安全问题。那么，**如果想让每个线程都有自己的专属本地变量，该如何实现呢？**

JDK 中提供的 `ThreadLocal` 类正是为了解决这个问题。**`ThreadLocal` 类允许每个线程绑定自己的值**，可以将其形象地比喻为一个“存放数据的盒子”。每个线程都有自己独立的盒子，用于存储私有数据，确保不同线程之间的数据互不干扰。每个线程都会绑定一个threadlocalMap,这是threadlocal只是key，设置的值为value,这时尽管key相同，获得的value也是线程私有map中获得的独立的value。



```java
public class ThreadLocalExample {
    //withInitial()中的方法是延迟执行的，在线程首次调用get时再执行，所以其生成的值对象也是线程间独立的，每个线程首次调用get时都会调用
    private static ThreadLocal<Integer> threadLocal = ThreadLocal.withInitial(() -> 0);

    public static void main(String[] args) {
        Runnable task = () -> {
            int value = threadLocal.get();
            value += 1;
            threadLocal.set(value);
            System.out.println(Thread.currentThread().getName() + " Value: " + threadLocal.get());
        };

        Thread thread1 = new Thread(task, "Thread-1");
        Thread thread2 = new Thread(task, "Thread-2");

        thread1.start(); // 输出: Thread-1 Value: 1
        thread2.start(); // 输出: Thread-2 Value: 1
    }
}
```


   threadlocal为什么会和线程内存泄露问题联系在一起，由于在实际使用中，线程常常以线程池的方法被使用；线程池

中的线程的run方法内，是以循环的方法去获取任务队列的任务去执行，同时获取不到的时候阻塞等待任务，所以线程会长时间停留在内存中。从而存在到threadlocal以及对应value的强引用链；

  `ThreadLocalMap` 的 `key` 和 `value` 引用机制：

- **key 是弱引用**：`ThreadLocalMap` 中的 key 是 `ThreadLocal` 的弱引用 (`WeakReference<ThreadLocal<?>>`)。 这意味着，如果 `ThreadLocal` 实例不再被任何强引用指向(如把类型为threadlocal的变量设置为null)，垃圾回收器会在下次 GC 时回收该实例，导致 `ThreadLocalMap` 中对应的 key 变为 `null`。
- **value 是强引用**：即使 `key` 被 GC 回收，`value` 仍然被 `ThreadLocalMap.Entry` 强引用存在，无法被 GC 回收。

 

<img src="D:\vscode-res\mkdocsSite\docs\images\image-20250625110038292.png" alt="image-20250625110038292" style="zoom:50%;" />

<img src="D:\vscode-res\mkdocsSite\docs\images\image-20250625110753869.png" alt="image-20250625110753869" style="zoom:50%;" />

## 解决内存泄露的方法

 `ThreadLocalMap` 在 `get()`, `set()` 和 `remove()` 操作时会尝试清理 key 为 null 的 entry，但这种清理机制是被动的，并不完全可靠。

在使用完 `ThreadLocal` 后，务必调用 `remove()` 方法。 这是最安全和最推荐的做法。 `remove()` 方法会从 `ThreadLocalMap` 中显式地移除对应的 entry，彻底解决内存泄漏的风险。 即使将 `ThreadLocal` 定义为 `static final`，也强烈建议在每次使用后调用 `remove()`。

在线程池等线程复用的场景下，使用 `try-finally` 块可以确保即使发生异常，`remove()` 方法也一定会被执行。

## 问题 为什么要使用threadlocal 不是直接用方法内的临时变量代替，也没有gc问题

临时变量（局部变量）**只能在当前方法中访问**，**无法跨方法、跨类共享**；而 `ThreadLocal` 是**让同一个线程内的多个方法共享变量的唯一干净方式**。

### 案例

#### 🧠 场景背景：

你在开发一个微服务系统，用户请求进来后，经过如下调用路径：

​	网关 → 服务A（Controller → Service → DAO → 调用服务B（HTTP/RPC）

为了能全链路追踪请求、排查问题，你希望每条日志都打印该请求的 traceId

```bash
[traceId=abc123] 用户下单成功
[traceId=abc123] 库存扣减成功
[traceId=abc123] 支付处理中
```

#### ❌ 如果不用 `ThreadLocal`：

你必须手动在每个方法中传递 traceId：

```java


public void controller(String traceId) {
    log.info("traceId={}, 控制层开始", traceId);
    service(traceId);
}

public void service(String traceId) {
    log.info("traceId={}, 业务处理", traceId);
    dao(traceId);
}


```

每一层都要加 `traceId` 参数；

非常 **冗余**；

第三方库（比如日志框架）也**无法自动拿到 traceId**。

#### ✅ 正确生产级做法：使用 ThreadLocal 传递 traceId

### 第一步：定义上下文类

```java
public class TraceContext {
    //通常都设为静态的，方便共享，方便任何方法内去引用到ThreadLocal
    private static final ThreadLocal<String> traceIdHolder = new ThreadLocal<>();

    public static void set(String traceId) {
        traceIdHolder.set(traceId);
        //MDC 配合日志框架用的，也可以不用
        MDC.put("traceId", traceId); // 日志上下文也设置
    }

    public static String get() {
        return traceIdHolder.get();
    }

    public static void clear() {
        traceIdHolder.remove();
        MDC.remove("traceId");
    }
}
```

------

### 第二步：在请求入口统一设置 traceId

例如：Spring Boot 中用 `OncePerRequestFilter`

```java
public class TraceIdFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
        throws ServletException, IOException {
        String traceId = request.getHeader("X-Trace-Id");
        if (traceId == null) {
            traceId = UUID.randomUUID().toString();
        }

        try {
            TraceContext.set(traceId); // 设置上下文
            chain.doFilter(request, response);
        } finally {
            TraceContext.clear(); // 请求结束清理
        }
    }
}
```

------

### 第三步：在任何业务层中直接使用

```java
public class OrderService {
    public void createOrder() {
        String traceId = TraceContext.get(); // 不需要传参
        log.info("开始处理订单，traceId={}", traceId);
    }
}
```