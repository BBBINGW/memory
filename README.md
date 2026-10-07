# Research memory

用于保存研究笔记与跨会话状态。ChatGPT 通过 GitHub Notes MCP 读写本文本仓库。

## 目录

- AGENT.md：用户确认的协作与操作规则。
- RESEARCH_PHILOSOPHY.md：用户确认的研究原则。
- STATE.md：下一次会话恢复工作所需的最小状态。
- TODO.md：待办与下一步。
- inbox/：临时材料和未分类文字。
- papers/notes/：论文阅读笔记、引用和原文链接。
- findings/：发现、推导和支持证据。
- failures/：失败尝试、反例和排除原因。
- logs/：按日期记录的研究日志。

## 网页版用法

选择 GitHub Notes 插件，然后指定目标路径，例如：

- “读取 AGENT.md、RESEARCH_PHILOSOPHY.md 和 STATE.md。”
- “把这段文字保存到 inbox/2026-10-07-idea.md，提交信息 docs: save idea。”
- “把论文笔记保存到 papers/notes/author-year-topic.md。”
- “把今天的进展追加到 logs/2026-10-07.md；如果文件不存在，先创建。”

路径使用英文、数字、连字符或下划线；正文可以写中文。允许 .md 和 .txt，子目录随文件创建。单文件上限 256 KiB。当前工具不上传 PDF、图片等二进制附件；可保存其链接或提取后的文字。

已有文件应先读再做最小修改，写完重读确认；append 是原样追加，需自己包含换行。清理与初始化保留 Git 提交历史，不重写历史。
