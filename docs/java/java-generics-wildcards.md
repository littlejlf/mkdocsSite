
# Java 泛型中的通配符详解：`? extends T` 与 `? super T`

本文整理自腾讯云开发者社区文章，主要讲解 Java 泛型通配符的使用方式与适用场景。

## 为什么需要通配符？

在 Java 中，泛型是不具备协变性的。即使 `Apple` 是 `Fruit` 的子类，`Plate<Apple>` 也不是 `Plate<Fruit>` 的子类。为了表达泛型类型间的灵活关系，引入了通配符：

- `? extends T`：上界通配符
- `? super T`：下界通配符

## `? extends T` 上界通配符

表示该泛型类型是 `T` 或其子类。

```java
Plate<? extends Fruit> plate = new Plate<Apple>();
```

这种通配符主要用于**读取数据**。不能写入数据（除了 `null`），因为编译器无法确认具体类型。

### 适用场景：
- 泛型对象是数据的“生产者”（Producer）
- 只能安全读取，不保证写入安全

## `? super T` 下界通配符

表示该泛型类型是 `T` 或其父类。

```java
Plate<? super Fruit> plate = new Plate<Object>();
```

这种通配符主要用于**写入数据**（只能addT以及其子类；但是List<? super Dog> list = new ArrayList<Object>(Arrays.asList("a", "b", "c"));是可以的）。读取时由于具体类型不确定，只能当作 `Object` 处理。

### 适用场景：
- 泛型对象是数据的“消费者”（Consumer）
- 可安全写入，但读取时类型信息丢失

## PECS 原则

Java 泛型使用中的经典原则：

- **Producer Extends**：需要从中读取数据时，使用 `? extends T`
- **Consumer Super**：需要向其中写入数据时，使用 `? super T`

## 注意事项

- 上界通配符 `? extends T`：**可读不可写**
- 下界通配符 `? super T`：**可写但读类型不确定**

## 总结

| 通配符         | 表示范围             | 适合操作 | 可写入 | 可读取 |
|----------------|----------------------|----------|--------|--------|
| `? extends T`  | T 及其子类           | 读取     | ❌     | ✅     |
| `? super T`    | T 及其父类           | 写入     | ✅     | 仅作 Object |

通过通配符的灵活运用，可以使 Java 泛型在保持类型安全的同时，增强代码的通用性与可复用性。
