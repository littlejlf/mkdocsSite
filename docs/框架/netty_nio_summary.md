
# ✅ Java NIO 与 Netty 中非阻塞 IO 机制整理

## 一、什么是 Java NIO 的非阻塞？

Java NIO 使用 Channel、Selector、Buffer 模型实现非阻塞 IO，即：

- `read()` / `write()` / `connect()` **不会阻塞线程**
- 使用 `Selector` 注册事件，统一轮询处理
- 适合高并发、多连接的场景

---

## 二、Netty 是如何使用 NIO 的？

Netty 默认使用 NIO：

- 封装了 `SocketChannel`、`Selector` 等底层组件
- 提供 `NioEventLoopGroup`、`NioServerSocketChannel`
- 实现了“事件驱动 + 回调 + 多路复用”的高性能 IO 处理框架

---

## 三、Boss 线程 和 Worker 线程的职责对比

| 内容        | Boss 线程（连接监听）             | Worker 线程（IO 读写处理）             |
|-------------|------------------------------------|------------------------------------------|
| 使用 NIO？  | ✅ ServerSocketChannel              | ✅ SocketChannel                          |
| 非阻塞表现  | ✅ 非阻塞 accept                    | ✅ 非阻塞 read/write                      |
| 工作职责    | 接收连接请求并分配给 Worker        | 处理读/写/断开等事件                     |
| 并发能力    | ❌ 单连接入口                      | ✅ 一个线程处理多个连接（多路复用）       |
| Selector 数 | 通常 1 个（accept）                | 多个（每个 Worker 一个 Selector）        |

---

## 四、Netty 非阻塞 IO 流程（以连接为例）

```
Client 发起连接请求
       ↓
Boss 线程（NioEventLoop）使用 Selector 监听 accept 事件
       ↓
ServerSocketChannel 非阻塞返回连接
       ↓
将连接封装为 NioSocketChannel，分配给某个 Worker
       ↓
Worker 的 Selector 开始监听连接上的读写事件
       ↓
事件到来时通过 ChannelHandler 回调处理
```

---

## 五、总结句（推荐背诵）

> Java NIO 的非阻塞模型在 Netty 中通过 Selector 和 Channel 得到完整实现。Boss 线程负责非阻塞接收连接，Worker 线程负责非阻塞读写和事件处理。非阻塞、高并发的核心体现主要在 Worker 的 IO 多路复用机制中。
