# 📖 MyBatis 中数据库连接与 TCP 层交互总结（中文版）

[TOC]

---

## 1. 🔌 程序连接数据库 = TCP 长连接

- 程序连接数据库（如 MySQL、PostgreSQL）时，**底层是通过 TCP 建立长连接的**。
- 例如 JDBC 连接字符串：

  ```bash
  jdbc:mysql://127.0.0.1:3306/test
  ```

- 网络层动作：
  - **TCP 三次握手**建立连接：

    ```
    客户端           服务器
    SYN  -------->
         <--------  SYN+ACK
    ACK  -------->
    （连接建立）
    ```

- 握手完成后，SQL 指令通过这个**持久的 TCP 连接**发送到数据库服务器。

---

## 2. 🔌 调用 `conn.close()` 后发生了什么？

### 情况 1：没有使用连接池（原始 JDBC）

- `conn.close()` 会**真正关闭** TCP 连接。
- 触发 TCP 四次挥手断开：

  ```
  FIN -------->
     <-------- ACK
     <-------- FIN
  ACK -------->
  ```

### 情况 2：使用连接池（如 HikariCP、Druid）

- `conn.close()` **不会关闭**物理连接。
- 只是将连接**归还给连接池**，供其他线程复用。
- 只有以下情况才会真正关闭 TCP：
  - 空闲超时（idleTimeout）
  - 生命周期到期（maxLifetime）
  - 健康检查失败
  - 连接池销毁

### ✅ 小结

| 场景                     | `conn.close()` 行为         | TCP 是否关闭 |
|---------------------------|-----------------------------|--------------|
| 原生 JDBC 无连接池        | 直接关闭连接                 | ✅ 是 |
| 使用连接池（Hikari/Druid） | 归还连接池，不断 TCP         | ❌ 否 |

---

## 3. 🛠 MyBatis 中连接的生命周期管理

### 关键组件

| 组件          | 职责                         |
|--------------|------------------------------|
| DataSource   | 提供数据库连接（连接池）      |
| Transaction  | 管理事务（commit/rollback）   |
| SqlSession   | 用户操作接口，控制事务和连接  |
| Executor     | 执行实际 SQL 语句             |

### 查询时完整流程

```text
1. SqlSessionFactory.openSession()
2. Transaction.getConnection() → DataSource.getConnection()
3. Executor.query()/update()
4. StatementHandler.prepare(Connection) → 执行 SQL
5. 返回查询结果
6. SqlSession.commit()/rollback()
7. SqlSession.close() → Transaction.close() → 连接归还或关闭
```

---

## 4. 🧠 每次查询 = 新建连接？

- ✅ 每次执行数据库操作需要一个活跃的连接。
- ❌ 但是**一个 SqlSession 生命周期内复用同一个连接**。

### 示例

```java
try (SqlSession session = sqlSessionFactory.openSession()) {
    UserMapper mapper = session.getMapper(UserMapper.class);
    User user1 = mapper.selectById(1); // 使用一次连接
    User user2 = mapper.selectById(2); // 同一个连接复用
}
```

✅ 小结：**不是每条 SQL 都新建一个连接**，是复用的。

---

## 5. 🌐 TCP 建立连接时验证了什么？

- **TCP 三次握手不是验证 IP 地址本身。**
- IP 地址的有效性是由网络层（IP层）完成的。
- TCP 握手验证的是：
  - 网络连通性（SYN 能送到）
  - 通信意愿（服务器回 SYN+ACK）
  - 通信能力（双方能正常收发 ACK）

### TCP 三次握手过程

```text
1. SYN（客户端请求建立连接）
2. SYN+ACK（服务器确认并应答）
3. ACK（客户端确认）
```

✅ 握手的目的是建立可靠的通信通道，不是验证 IP 的真伪。

---

# ✨ 核心总结

> 在 MyBatis 中，每个 SqlSession 生命周期期间复用同一个数据库连接，连接通过 DataSource（连接池或裸连接）获取，本质上是 TCP 长连接，conn.close() 在连接池下只是归还连接，不直接关闭 TCP，真正的 TCP 关闭由连接池统一管理。

---

# 📦 可扩展学习方向

- TCP 四次挥手断开细节（为什么需要 4 次）
- HikariCP 如何健康检测连接（keepalive）
- MySQL wait_timeout 参数与 TCP 连接保持
- 连接池连接泄漏的检测与治理

如果需要深入这些内容，可以继续探讨！✨
