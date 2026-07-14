###### 几个命令

mkdocs build

mkdocs gh-deploy

mkdocs serve
###### 网址
https://littlejlf.github.io/mkdocsSite/

---

### AI 对话样式开关

`mkdocs.yml` 中：

```yaml
extra:
  conversation_formatting: true   # true=开启AI对话美化 false=原始markdown样式
```

### 触发关键词

Hook 自动检测以下格式的 .md 文件并应用对话样式：

| 匹配条件 | 说明 |
|---------|------|
| 文件首行为 `> From: ...` | 标记为 AI 对话页，来源 URL 显示为灰色引用 |
| `# you asked` | 用户提问，显示 `[问]` 标签 |
| `# chatgpt response` | AI 回复，显示 `[答]` 标签 |
| `message time: ...` | 提问时间戳，自动提取显示 |

满足首行格式即可，其他关键词自动匹配，无需手动配置。