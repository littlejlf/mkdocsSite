# DTO、Entity、BO、VO、DO 简明整理

## 1. 什么是 DTO？

**DTO（Data Transfer Object）** 是一种数据传输对象，用于系统不同层之间传递数据。

**特点：**

- 只包含字段（属性）和 Getter/Setter，不包含业务逻辑。
- 用于前后端之间的数据交互（如接收请求或返回响应）。
- 在系统的 Controller 层到 Service 层之间使用。

**示例代码：**

```java
public class RaffleAwardListRequestDTO {
    private String userId;
    private int pageNumber;
    private int pageSize;

    // Getter 和 Setter
}
```

**总结一句话：**

> DTO 是用来在系统各层传递数据的简单对象，只负责搬数据，不负责处理数据。

------

## 2. 项目分层结构中 DTO 所在位置

标准三层架构中，DTO 的使用位置如下：

| 层级                     | 主要内容                                 | DTO 所在位置                            |
| ------------------------ | ---------------------------------------- | --------------------------------------- |
| Controller 层（接口层）  | 接收前端请求、返回响应，处理参数校验     | ✅ 使用 DTO 来接收请求参数、返回响应数据 |
| Service 层（业务逻辑层） | 编写具体的业务逻辑                       | 有时也用 DTO 作为参数或返回值           |
| DAO 层（数据访问层）     | 操作数据库（Entity/DO 直接映射数据库表） | ❌ 通常用实体对象（Entity/DO），不是 DTO |

**整体数据流动简图：**

```
[前端] 
    ↓
[Controller 层] 
    - 用 RequestDTO 接收数据
    ↓
[Service 层] 
    - 处理业务逻辑（可能使用 BO）
    ↓
[DAO 层]
    - 操作数据库实体对象（DO/Entity）
```

**处理完后返回流程：**

- Service 层将结果封装为 ResponseDTO 或 VO
- Controller 层返回给前端

------

## 3. 中间常见的数据对象有哪些？

| 对象                           | 作用                                       | 典型使用层             |
| ------------------------------ | ------------------------------------------ | ---------------------- |
| **DTO (Data Transfer Object)** | 对外数据传输对象（接口请求/响应）          | Controller、Service 层 |
| **VO (View Object)**           | 面向前端展示的数据对象                     | Controller 层          |
| **BO (Business Object)**       | 业务逻辑内部使用的对象                     | Service 层             |
| **DO (Data Object)**           | 直接映射数据库表的数据对象                 | DAO 层                 |
| **Entity**                     | ORM 框架用的数据实体对象，通常对应数据库表 | DAO 层                 |

**分类口诀：**

> DTO 对外、VO 展示、BO 业务、DO 持久化（Entity 存数据库）。

------

## 4. 为什么使用 DTO？

**优点总结：**

1. **更好扩展**
   - 新增字段只需要修改 DTO 类，不必改接口方法签名，兼容老代码。
2. **减少方法参数数量**
   - 接口方法只传一个 DTO 对象，代码清爽整洁。
3. **契约清晰**
   - 明确接口需要哪些字段，前端后端一目了然。
4. **便于序列化/反序列化**
   - Spring Boot 框架等可以自动处理 JSON 与 DTO 的互转。
5. **灵活校验**
   - 可在 DTO 字段上直接使用校验注解（如 `@NotNull`、`@Size` 等）。
6. **清晰分层**
   - 不影响业务逻辑对象（BO）、持久化对象（Entity/DO），职责单一。

**一句话总结：**

> DTO 让你的代码更抗变、更好维护、更优雅！

------

## 5. 典型对象流动全流程示意图

![对象流动图](<images/DTO、Entity、BO、VO、DO 简明整理/image.png>)
**文字版说明：**

```
前端发送请求（Request）
    ↓
[Controller 层]
    - 用 RequestDTO 接收参数
    - 调用 Service 层

[Service 层]
    - 处理业务逻辑，使用 BO
    - 如果需要查询数据库
        ↓
    调用 DAO 层

[DAO 层]
    - 操作数据库，使用 DO/Entity
    - 返回 DO/Entity 给 Service

Service 返回处理结果
    - 将结果封装为 ResponseDTO 或 VO
    - Controller 返回数据给前端
```

------

# 总结

> 项目分层清晰，数据对象职责分明，代码可维护性和扩展性大大提高。熟练掌握 DTO、VO、BO、DO、Entity 的使用，是高级开发工程师必备基本功！