
# Netty 通信处理流程：物联网场景（JSON 报文/二进制传输）

## ✅ 场景背景

智能温湿度传感器每隔 30 秒通过 TCP 上报一次数据，报文内容为 UTF-8 编码的 JSON 格式，例如：

```json
{"deviceId":"abc123","temp":23.5,"hum":48.2,"timestamp":1718721523}
```

- 协议结构：`[2字节长度][JSON数据]`
- 通过 TCP 传输，本质是 **二进制字节流**

---

## ✅ 协议示意

| 字节偏移 | 字段     | 类型    | 描述                      |
|----------|----------|---------|---------------------------|
| 0~1      | length   | short   | JSON 字符长度（单位：字节）|
| 2~N      | payload  | byte[]  | UTF-8 编码 JSON 字节序列  |

---

## ✅ Netty Server 通信处理流程

1. 使用 `LengthFieldBasedFrameDecoder` 处理粘包/半包
2. 自定义 `ByteToMessageDecoder` 解码 ByteBuf → JSON 字符串 → Java 对象
3. 使用业务 Handler 处理上报数据

---

## ✅ ChannelPipeline 示例

```java
pipeline.addLast(new LengthFieldBasedFrameDecoder(
    1024,  // 最大帧长度
    0,     // 长度字段偏移
    2      // 长度字段长度（short）
));
pipeline.addLast(new JsonReportDecoder());
pipeline.addLast(new JsonBusinessHandler());
```

---

## ✅ 解码器示例（JsonReportDecoder）

```java
public class JsonReportDecoder extends ByteToMessageDecoder {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    protected void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) throws Exception {
        // 从 ByteBuf 中读取 UTF-8 编码字符串
        String jsonStr = in.toString(CharsetUtil.UTF_8);

        // 解析 JSON 为 Java 对象
        JsonNode node = objectMapper.readTree(jsonStr);
        SensorData data = new SensorData(
            node.get("deviceId").asText(),
            node.get("temp").asDouble(),
            node.get("hum").asDouble(),
            node.get("timestamp").asLong()
        );

        out.add(data); // 传递给下一个 handler
    }
}
```

---

## ✅ SensorData 实体类

```java
public record SensorData(String deviceId, double temp, double hum, long timestamp) {}
```

---

## ✅ 业务处理 Handler 示例

```java
public class JsonBusinessHandler extends SimpleChannelInboundHandler<SensorData> {

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, SensorData data) {
        System.out.println("📥 上报数据: " + data);
        // 1. 数据入库
        // 2. 超温超湿告警判断
        // 3. 推送前端可视化
    }
}
```

---

## ✅ ByteBuf 与字符串解码说明

- `ByteBuf` 是 Netty 的字节容器
- 调用 `in.toString(CharsetUtil.UTF_8)`：
  - 从 `readerIndex` 开始读取
  - 读取 `readableBytes()` 个字节
  - 不会修改指针
- 如果要“消耗掉字节”，可以用：
  ```java
  in.readCharSequence(in.readableBytes(), CharsetUtil.UTF_8).toString();
  ```

---

## ✅ 总结

- TCP 一定是**字节流**，即使内容是 JSON，Netty 也是收到的字节数组
- 你需要通过：
  1. **解包器**保帧
  2. **ByteBuf → String**（指定编码）
  3. **JSON → Java 对象**
- 常用于设备上报、自定义协议、业务事件推送等物联网高频场景

## 代码使用（包括init）

  ```java
  public class NettyServer {

    private final int port;

    public NettyServer(int port) {
        this.port = port;
    }

    public void run() throws InterruptedException {
        // boss：处理连接请求
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        // worker：处理 IO 读写事件
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap bootstrap = new ServerBootstrap();

            bootstrap.group(bossGroup, workerGroup)
                     .channel(NioServerSocketChannel.class)
                     .childHandler(new ChannelInitializer<SocketChannel>() {
                         @Override
                         protected void initChannel(SocketChannel ch) {
                             ChannelPipeline pipeline = ch.pipeline();

                             // 1. 粘包/拆包处理器（2字节长度前缀）
                             pipeline.addLast(new LengthFieldBasedFrameDecoder(
                                     1024, // maxFrameLength
                                     0,    // lengthFieldOffset
                                     2,    // lengthFieldLength
                                     0,    // lengthAdjustment
                                     2     // initialBytesToStrip（strip掉长度字段）
                             ));

                             // 2. 自定义解码器（ByteBuf → Java 对象）
                             pipeline.addLast(new MyDeviceDecoder());

                             // 3. 自定义业务处理器
                             pipeline.addLast(new MyBusinessHandler());
                         }
                     });

            // 绑定端口，启动服务
            ChannelFuture future = bootstrap.bind(port).sync();
            System.out.println("✅ Netty Server started on port " + port);

            // 等待关闭
            future.channel().closeFuture().sync();

        } finally {
            // 优雅关闭线程池
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        new NettyServer(9000).run();
    }
}

  ```
