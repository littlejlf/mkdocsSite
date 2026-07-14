# Git 合并机制、冲突模型与协作实践完整总结

------

# 一、Git 的三棵树模型（理解一切的基础）

Git 的核心不是“文件系统”，而是三棵树模型：

1. **HEAD**
2. **Index（Stage / 暂存区）**
3. **Working Tree（工作区）**

------

## 1️⃣ HEAD 是什么？

HEAD 指向：

> 当前分支的最新一次提交（最近 commit）

它代表：

- 已经进入历史的版本
- 上一次 commit 的完整快照

```
A → B → C (HEAD)
```

------

## 2️⃣ Index（暂存区）是什么？

Index 表示：

> 下一次 commit 将要保存的内容

流程：

```
Working Tree --git add--> Index --git commit--> HEAD
```

注意：

- `git add` 只是进入 Index
- 只有 `git commit` 才进入历史

------

## 3️⃣ 三棵树关系图

```
HEAD        上一次提交
Index       准备提交
Working     正在修改
```

理解三棵树，是理解 merge、rebase、stash、冲突的基础。

------

# 二、三方合并（Three-way Merge）机制

当 Git 需要“合并历史”时，会进行三方比较。

三方是：

1. 共同祖先（merge base）
2. 当前分支（HEAD）
3. 目标分支（如 origin/main）

示例：

```
        C   (远程)
       /
A — B
       \
        D   (本地)
```

三方为：

- 祖先：B
- 本地：D
- 远程：C

Git 比较：

- B → D 的修改
- B → C 的修改

如果修改区域重叠 → 冲突。

------

# 三、什么时候会触发合并？

| 操作          | 是否涉及三方合并   |
| ------------- | ------------------ |
| git merge     | ✅                  |
| git pull      | ✅（fetch + merge） |
| git rebase    | ✅                  |
| git stash pop | ✅                  |
| git push      | ❌                  |
| git fetch     | ❌                  |

------

# 四、三种完全不同的“问题类型”（最容易混淆）

Git 中常见的“报错”其实分三类。

------

## ① 工作区保护（Working Tree Protection）

触发条件：

- 工作区有未提交修改
- pull 会修改同一个文件

报错：

```
Your local changes would be overwritten by merge.
```

⚠ 注意：

这不是冲突。

这是：

> Git 拒绝开始 merge

它发生在：

- merge 之前
- 甚至还没进入三方比较

目的：

> 防止你未提交的修改被覆盖

解决方式：

```
git commit
git stash
```

------

## ② 三方合并冲突（真正的冲突）

触发条件：

- 同一段代码在两个分支都被修改

发生阶段：

- 已进入 merge 或 rebase

表现：

```
CONFLICT (content)
```

文件出现：

```
<<<<<<< HEAD
...
=======
...
>>>>>>> branch
```

这是三方对比失败的结果。

------

## ③ push 被拒绝（Non-fast-forward）

示例：

```
远程: A → B → C
本地: A → B → D
```

执行 push：

```
rejected (non-fast-forward)
```

这不是冲突。

这是：

> 历史分叉，不能直接移动远端指针

必须先：

```
git pull
```

再合并后 push。

------

# 五、Fast-forward vs Non-fast-forward

## 1️⃣ Fast-forward

```
远程: A → B → C
本地: A → B → C → D
```

push 只是：

> 移动远程指针

没有新 commit
 没有分叉
 没有冲突

------

## 2️⃣ Non-fast-forward

```
远程: A → B → C
本地: A → B → D
```

不能简单移动指针。

必须合并或 rebase。

------

# 六、Merge 与 Rebase 的本质区别

## 1️⃣ Merge

```
git merge main
```

特点：

- 三方合并一次完成
- 产生一个 merge commit
- 保留真实分叉

结构：

```
A → B → C
     ↘   ↘
       D → M
```

优点：

- 不改历史
- 协作安全

缺点：

- 历史变复杂

------

## 2️⃣ Rebase

```
git rebase main
```

本质：

> 把每个 commit 重新在新基底上执行一次

原结构：

```
      C
     /
A — B
     \
      D → E
```

变成：

```
A → B → C → D' → E'
```

特点：

- 重写 commit
- 不产生 merge commit
- 历史线性

优点：

- 更干净

缺点：

- 改写历史
- 公共分支危险

------

# 七、为什么 Rebase 更容易冲突？

因为：

merge 是：

> 一次三方比较

rebase 是：

> 每个 commit 都重新执行一次三方比较

commit 越多
 冲突概率越高

------

# 八、stash 的本质与冲突机制

## 1️⃣ stash 做了什么？

```
git stash
```

本质：

- 把 Working Tree 和 Index 的改动
- 保存成一个临时 commit
- 然后回到 HEAD 状态

默认：

- 保存已跟踪文件的修改
- 不保存未跟踪文件（除非 `-u`）

------

## 2️⃣ stash 为什么能绕过工作区保护？

因为 stash 后：

```
Working Tree 变干净
```

所以：

```
git pull
```

不会触发保护机制。

------

## 3️⃣ stash pop 为什么会冲突？

```
git stash pop
```

本质是：

> 把 stash 那个 commit 再 merge 回当前分支

三方是：

1. 当前 HEAD
2. stash 保存时的基底
3. stash 的修改

如果 pull 之后代码变化：

> 当前 HEAD 与 stash 的修改冲突

就会产生冲突。

------

# 九、Index 在冲突时的内部结构

当 merge 冲突发生时：

Index 会存储三份内容：

| Stage | 内容     |
| ----- | -------- |
| 1     | 祖先版本 |
| 2     | 当前分支 |
| 3     | 目标分支 |

这就是三方合并的底层实现。

------

# 十、协作开发最佳实践

### 1️⃣ 公共分支不要 rebase

避免：

```
git push --force
```

------

### 2️⃣ feature 分支可以 rebase

```
git pull --rebase
```

保持历史干净。

------

### 3️⃣ 经常 pull

减少分叉时间。

------

### 4️⃣ 小步提交

降低冲突范围。

------

### 5️⃣ 使用分支保护（如在 GitHub 上）

- 禁止 force push
- 强制 PR
- 强制 CI

------

# 最终核心理解

Git 中其实存在三类完全不同的现象：

1. 工作区保护（merge 之前拒绝）
2. 三方合并冲突（merge / rebase 过程中）
3. non-fast-forward 拒绝（push 阶段）

它们：

- 发生阶段不同
- 原理不同
- 解决方式不同

一旦分清这三种问题，你就不会再混淆。