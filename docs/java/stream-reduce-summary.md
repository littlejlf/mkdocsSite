# Java Stream API — `reduce(identity, accumulator)` 使用总结

## 📌 方法定义

```java
T reduce(T identity, BinaryOperator<T> accumulator)
```

该方法对流中的元素执行归约操作，使用指定的 **恒等值** `identity` 和一个 **结合型累加函数** `accumulator`，返回归约后的结果。

其逻辑等价于：

```java
T result = identity;
for (T element : stream)
    result = accumulator.apply(result, element);
return result;
```

---

## ⚙️ 并行执行说明

### ✅ 用户无需关心的并行实现细节：
- 数据的分片策略
- 并行任务的线程调度
- 中间结果的合并过程
- 所使用的线程池或底层机制（如 ForkJoinPool）

这些由 Java 流的实现自动处理，特别是在调用 `.parallel()` 时。

### ⚠️ 但必须满足的前提条件：

| 要求 | 说明 |
|------|------|
| **结合性** (Associativity) | `a ⊕ (b ⊕ c) == (a ⊕ b) ⊕ c`，如加法、乘法、字符串拼接 |
| **无副作用** (Stateless & Non-interfering) | 累加函数不能访问或修改外部状态或共享变量 |
| **恒等值 identity** | 对所有 `t` 满足：`accumulator.apply(identity, t) == t` |

---

## 💡 使用示例

### 示例 1：整数求和

```java
List<Integer> integers = List.of(1, 2, 3, 4);
Integer sum = integers.reduce(0, Integer::sum);
System.out.println(sum); // 输出 10
```

### 示例 2：字符串拼接

```java
List<String> words = List.of("Hello", "World");
String sentence = words.reduce("", (a, b) -> a + " " + b);
System.out.println(sentence); // 输出 " Hello World"
```

---

## ✅ 优点总结

- 提供函数式风格的聚合操作
- 可自动并行执行，适合大数据量处理
- 避免线程安全问题，简化同步逻辑

---

## ⚠️ 错误示例：含副作用的累加器

```java
List<Integer> list = Arrays.asList(1, 2, 3);

// 不推荐：累加器包含副作用操作（打印），并行执行可能导致混乱
Integer sum = list.parallelStream().reduce(0, (a, b) -> {
    System.out.println(Thread.currentThread().getName());
    return a + b;
});
```

输出结果可能无序，性能不稳定，并可能出现竞态条件。

---

## 🔚 总结

> `reduce(identity, accumulator)` 是一种强大而安全的终端归约操作。  
> 只要满足函数式约束（结合性、无副作用、恒等值），你就可以放心地使用它进行顺序或并行的聚合处理，而无需操心底层并发细节。
