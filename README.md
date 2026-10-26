# Research memory

用于保存研究笔记与跨会话状态。ChatGPT 通过 GitHub Notes MCP 读写本文本仓库。

## 目录

- AGENT.md：用户确认的协作与操作规则。
- RESEARCH_PHILOSOPHY.md：用户确认的研究原则。
- [科研质量执行指南](findings/RESEARCH_QUALITY_EXECUTION_2026-10-26.md)：七个科研问题的修复、P0–P2、完整贡献门槛与可复现证据等级。
- STATE.md：历史及当前状态入口，可能包含可执行的 NEXT_ACTION；若落后于可信的最新研究线快照，必须先核验和对账，不能凭旧标题改变当前方向。
- TODO.md：待办与下一步。
- inbox/：临时材料和未分类文字。
- papers/notes/：论文阅读笔记、引用和原文链接。
- findings/：发现、推导和支持证据。
- failures/：失败尝试、反例和排除原因。
- logs/：按日期记录的研究日志。

## 网页版用法

选择 GitHub Notes 插件，然后指定目标路径，例如：

- “先按 START_RESEARCH_SESSION.md 识别 PI 最近明确选择的目标，读取科研质量执行指南，核对最新可靠的研究线快照。”
- “把这段文字保存到 inbox/2026-10-07-idea.md，提交信息 docs: save idea。”
- “把论文笔记保存到 papers/notes/author-year-topic.md。”
- “把今天的进展追加到 logs/2026-10-07.md；如果文件不存在，先创建。”

路径使用英文、数字、连字符或下划线；正文可以写中文。允许 .md 和 .txt，子目录随文件创建。单文件上限 256 KiB。当前工具不上传 PDF、图片等二进制附件；人工提供的 PDF 可放在 papers/supplied/，通过 read_repo_pdf 分页读取文本。

已有文件应先读再做最小修改，写完重读确认；append 是原样追加，需自己包含换行。清理与初始化保留 Git 提交历史，不重写历史。

## 研究基础设施

新会话从 [START_RESEARCH_SESSION.md](START_RESEARCH_SESSION.md) 开始。
本地/长期存储规则见 [LOCAL_WORKSPACE.md](LOCAL_WORKSPACE.md)；论文获取规则见
[papers/README.md](papers/README.md)，重要证据缺口记录在
[MISSING_SOURCES.md](MISSING_SOURCES.md)。如果当前 checkout 确实包含 `scripts/research_health.py`，可运行该脚本检查基础文件与凭证风险；执行前应先验证脚本存在。当前仓库目录清单未显示 `scripts/`，因此不应将该命令写成必需的启动步骤。

当前 MCP 支持 `papers/supplied/` 下 PDF 的只读分页文本提取，不支持本机文件、
PDF 写入、OCR 或图像解读。使用方法与质量限制见 `papers/supplied/README.md`。
服务端已放行上述研究文档和 `papers/`。MCP 生产 HTTPS 测试已通过；
ChatGPT 中可能需要刷新工具列表
以发现新增的 `read_repo_pdf`。


## 当前科研指南和研究状态（2026-10-26）

研究会话优先按 [START_RESEARCH_SESSION.md](START_RESEARCH_SESSION.md)、[科研质量执行指南](findings/RESEARCH_QUALITY_EXECUTION_2026-10-26.md)、[AGENT.md](AGENT.md) 和 [RESEARCH_PHILOSOPHY.md](RESEARCH_PHILOSOPHY.md) 工作。

- **P0：**先确定重要的、原文可查的实际瓶颈和基线，避免不断换论文拼 technique。
- **P1：**在深入推导或 Codex 前完成原文接口、原创机制、先前技术、乐观端到端收益四项检查；缺关键原文时标记 `SOURCE_BLOCKED`。
- **P2：**复用旧的失败和完整修复经验；保留一个最小可证伪假设、一个决定性测试，以及正确性、安全、精度和完整成本的渐进验证。
- 研究线由 PI 最近的明确选择确定；`继续`不得擅自切换或重启 `PAUSED` 项目。若根 `STATE.md` 与晚近独立审计/交接冲突，应显式标记 `STATE_STALE/RECONCILE_REQUIRED`，先核验再更新。
- 原 [研究线索引](findings/RESEARCH_TRACK_INDEX.md)、[隔离规则](findings/TRACK_ISOLATION_POLICY.md) 和 [MCP 隔离设计](findings/MCP_TRACK_GUARD_CODEX_SPEC.md) 是历史文件，不是要求额外部署服务端隔离的当前规范；这不取消 PI 对研究目标和写入范围的授权要求。
- 历史 GitHub 累计记录可能滞后。例如 SHIP-I407、BOOT-B123 的较新交接证据曾独立保存；引用轮次、原生性能和新颖性结论前应逐项核对证据等级，不能默默把 prescout 记成正式完成。

此方法文档更新不改变任何历史研究结论、暂停状态、正式编号或实验授权。
