# 🧭 Python 文件路径完全指南

------

# 一、核心结论（先记住）

> 👉 `Path("xxx")` 永远是相对于 **当前工作目录（cwd）**
>  👉 ❗不是相对于当前 `.py` 文件

------

# 二、三个核心概念

------

## 1️⃣ 当前工作目录（cwd）

```
import os
os.getcwd()
```

👉 表示：

> **程序运行时所在的目录（由你在哪执行决定）**

------

### 示例

```
cd /home/user/project
python main.py
cwd = /home/user/project
```

------

## 2️⃣ 当前文件路径（`__file__`）

```
__file__
```

👉 表示：

> **当前 Python 文件的位置**

------

### 示例

```
/home/user/project/app/main.py
```

------

## 3️⃣ 相对路径（Path）

```
from pathlib import Path
Path("data/raw")
```

👉 表示：

> **相对于 cwd 的路径**

------

# 三、最容易踩的坑（重点）

------

## ❌ 常见误区

```
Path("data/raw") 是相对于当前文件
```

👉 这是错误的

------

## ✅ 实际行为

```
Path("data/raw") 是相对于当前工作目录（cwd）
```

------

# 四、经典踩坑案例（解压工具）

------

## 场景：写一个解压脚本

```
# unzip.py
from pathlib import Path

zip_path = Path("input.zip")
output_dir = Path("output")

print("zip_path:", zip_path.resolve())
print("output_dir:", output_dir.resolve())
```

------

## 目录结构

```
project/
├── unzip.py
├── input.zip
```

------

## 情况 1：在项目目录运行（正常）

```
cd project
python unzip.py
```

输出：

```
project/input.zip
project/output
```

👉 正确

------

## 情况 2：在其他目录运行（踩坑）

```
cd /
python /project/unzip.py
```

输出：

```
/input.zip
/output
```

👉 ❌ 完全错误！

------

## 问题原因

```
Path("input.zip")
```

实际等价于：

```
cwd/input.zip
```

而不是：

```
unzip.py 所在目录/input.zip
```

------

# 五、正确写法（稳定方案）

------

## ✅ 相对于当前文件

```
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

zip_path = BASE_DIR / "input.zip"
output_dir = BASE_DIR / "output"
```

------

## 无论在哪运行：

```
cd /
python /project/unzip.py
```

结果始终：

```
/project/input.zip
/project/output
```

👉 ✅ 稳定

------

# 六、什么时候应该用 cwd

------

## 场景：写通用工具

```
python unzip.py my.zip
```

------

## 正确写法

```
import sys
from pathlib import Path

zip_path = Path(sys.argv[1])
```

------

👉 这样：

```
用户在哪运行，就操作哪的文件
```

------

# 七、设计原理（理解就不会忘）

------

## Python 为什么用 cwd？

👉 因为继承操作系统设计：

```
每个进程都有当前工作目录（cwd）
```

------

## cwd 的作用

```
表示程序运行的“上下文环境”
```

------

## **file** 的作用

```
表示代码存放的位置
```

------

## 两者区别

| 概念       | 含义                     |
| ---------- | ------------------------ |
| cwd        | 程序运行位置（用户视角） |
| `__file__` | 代码位置（开发者视角）   |

------

# 八、设计哲学

------

如果只用 `__file__`：

```
所有路径都固定在代码目录 ❌
```

👉 会导致：

- CLI 工具无法处理用户文件 ❌
- 程序不灵活 ❌

------

所以必须区分：

```
cwd → 用户操作环境
__file__ → 项目资源定位
```

------

# 九、实战规则（最重要）

------

## ✅ 规则 1

```
Path("xxx") = 相对于 cwd
```

------

## ✅ 规则 2

```
项目内部文件 → 用 __file__
```

------

## ✅ 规则 3

```
用户输入路径 → 用 cwd
```

------

# 十、终极对比表

| 场景             | 写法                                  | 是否正确 |
| ---------------- | ------------------------------------- | -------- |
| 解压当前目录文件 | `Path("input.zip")`                   | ✅        |
| 读取脚本内置资源 | `Path("input.zip")`                   | ❌        |
| 读取脚本内置资源 | `Path(__file__).parent / "input.zip"` | ✅        |