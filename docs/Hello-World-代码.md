> From: https://chatgpt.com/c/6a55b074-bef8-83e8-a8bb-2254d50babaa

# you asked

message time: 2026-07-14 11:43:48

写一个hello word的代码

---

# chatgpt response

你没有指定语言，下面给几个常见版本：

### Java
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

运行：
```bash
javac HelloWorld.java
java HelloWorld
```

---

### Python
```python
print("Hello World")
```

运行：
```bash
python hello.py
```

---

### C
```c
#include <stdio.h>

int main() {
    printf("Hello World\n");
    return 0;
}
```

---

### JavaScript (Node.js)
```javascript
console.log("Hello World");
```

运行：
```bash
node hello.js
```

---

### Go
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello World")
}
```

---

如果是学习后端开发，最常见的第一个 Hello World 一般是 **Java + Spring Boot**：

```java
@RestController
@SpringBootApplication
public class HelloApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloApplication.class, args);
    }

    @GetMapping("/hello")
    public String hello() {
        return "Hello World";
    }
}
```

启动后访问：

```
http://localhost:8080/hello
```

返回：

```
Hello World
```