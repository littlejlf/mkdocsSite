# 小龙虾 AI Agent 架构解析

> 基于李宏毅老师课程笔记整理
> 
> 📅 整理时间：2026-03-15

---

## 目录

- [整体架构](#整体架构)
- [核心组件](#核心组件)
  - [Subagent 子代理](#subagent-子代理)
  - [Context Engineering 上下文工程](#context-engineering-上下文工程)
  - [Skill 技能系统](#skill-技能系统)
- [记忆机制](#记忆机制)
- [定时任务系统](#定时任务系统)

---

## 整体架构

![AI Agent 主要流程](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315142207680.png)

*图 1: AI Agent 的主要流程*

![架构图](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315142240440.png)

*图 2: 小龙虾 Agent 整体架构*

---

## 核心组件

### Subagent 子代理

![Subagent](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315140554928.png)

*图 3: Subagent 工作模式*

小龙虾采用**主从式 Agent 架构**：

- **主 Agent**：负责任务分解、协调和最终决策
- **Subagent（子代理）**：专注于执行单一、具体的子任务

这种设计的优势在于：
- 任务隔离，降低复杂度
- 可并行执行多个子任务
- 每个子代理可以独立优化

### Context Engineering 上下文工程

上下文管理是小龙虾架构的核心设计理念：

> **子 Agent 只关注当前任务，不继承主 Agent 的完整上下文**
> 
> **主 Agent 的上下文中也只保留子 Agent 的执行结果，而非完整对话历史**

这种**最小化上下文传递**的设计有以下好处：

1. **降低 Token 消耗** - 避免冗余信息占用上下文窗口
2. **提高专注度** - 子代理不受无关信息干扰
3. **清晰的职责边界** - 每个 Agent 只关心自己需要知道的内容

### Skill 技能系统

![Skill 概念](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315140408937.png)

*图 4: Skill 是工作的 SOP（标准操作流程）*

**Skill = 工作的 SOP（Standard Operating Procedure）**

每个 Skill 封装了一个特定任务的执行流程和规范，类似于人类的"工作手册"或"操作指南"。

#### Skill 按需读取机制

![Skill 读取流程](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315141311047.png)

*图 5: Skill 按需加载流程*

![Skill 详细流程](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315141732438.png)

*图 6: Skill 读取详细流程*

小龙虾采用**两阶段 Skill 加载策略**：

```
┌─────────────────────────────────────────────────────────┐
│  阶段 1: 预加载（Parser 阶段）                           │
│  - 通过关键词匹配等简单规则                              │
│  - 从本地 Skill 库中筛选可能需要的 Skill                  │
│  - 仅加载 <简介，skill.md 路径> 到上下文                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  阶段 2: 按需加载（Tool Use 阶段）                       │
│  - 当 LLM 判断需要使用某个 Skill 时                        │
│  - 输出 read 工具调用                                     │
│  - 读取完整的 skill.md 文件并嵌入上下文                    │
│  - LLM 获得完整的 Skill 指令                              │
└─────────────────────────────────────────────────────────┘
```

**设计优势：**
- ✅ 避免一次性加载所有 Skill 造成上下文膨胀
- ✅ 只在真正需要时才消耗 Token 读取完整内容
- ✅ 支持大规模 Skill 库的灵活管理

---

## 记忆机制

### 记忆存储

![记忆机制](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315142639418.png)

*图 7: 对话信息记录到本地*

小龙虾具备**持久化记忆能力**，会将对话中的关键信息记录到本地存储中。

### 记忆检索（RAG）

![记忆检索](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315142845245.png)

*图 8: 记忆检索流程*

![记忆 RAG](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315143138138.png)

*图 9: 基于 RAG 的记忆检索*

记忆检索采用 **RAG（Retrieval-Augmented Generation）** 模式：

1. **系统提示词声明** - 在 System Prompt 中明确要求检索记忆
2. **关键字生成** - 由 LLM 根据当前对话生成检索关键字
3. **语义检索** - 对 `记忆.md` 文件进行向量化检索
4. **上下文注入** - 将检索到的记忆片段注入当前对话上下文

这种设计让 Agent 能够：
- 🧠 "记住" 历史对话中的重要信息
- 🔍 主动回忆相关的过往经历
- 📚 基于累积经验做出更准确的判断

---

## 定时任务系统

### 龙虾的新特性

![定时任务特性](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315143408298.png)

*图 10: 定时任务系统*

**区别于传统 AI Agent，小龙虾支持定时触发预设任务**

传统 Agent 通常是**被动响应**模式（用户提问 → Agent 回答），而小龙虾增加了**主动触发**能力：

- 可预设定时任务
- 到点自动执行预设的 Prompt/任务
- 支持周期性任务和一次性任务

### 排程系统架构

![排程系统 1](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315143724607.png)

![排程系统 2](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315143815041.png)

![排程系统 3](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315143937451.png)

![排程系统 4](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315144024023.png)

![排程系统 5](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260315144233437.png)

*图 11-15: 排程系统详细架构*

排程系统的核心能力：

| 特性 | 说明 |
|------|------|
| **类似 Cron** | 支持定时任务调度 |
| **状态等待** | 可等待外部系统结果生成完成 |
| **任务编排** | 支持任务依赖和顺序执行 |
| **结果回调** | 任务完成后可触发后续动作 |

---

## 总结

小龙虾 Agent 架构的核心创新点：

| 组件 | 核心设计 | 解决的问题 |
|------|----------|------------|
| **Subagent** | 主从式任务分解 | 复杂任务的可管理性 |
| **Context Engineering** | 最小化上下文传递 | Token 效率与专注度 |
| **Skill 系统** | 两阶段按需加载 | 大规模技能库管理 |
| **记忆机制** | RAG 检索持久化记忆 | 长期上下文保持 |
| **排程系统** | 定时主动触发 | 从被动响应到主动执行 |

这套架构使得 AI Agent 能够：
- 🎯 更高效地处理复杂任务
- 💰 更经济地使用 Token 资源
- 🧠 拥有"记忆"能力，持续学习
- ⏰ 主动执行任务，而非仅被动响应

---

## 参考资料

- 李宏毅 AI Agent 课程视频：[YouTube 链接](https://www.youtube.com/watch?v=2rcJdFuNbZQ)
- 笔记整理：2026-03-15
