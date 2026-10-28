# NoteForge

**让零散资料成为值得留下的笔记。**

NoteForge 是一个轻量级、注重来源可核对的 [Agent Skill](https://agentskills.io/)，能够将课件、PDF、文档、图片和零散记录整理成清晰、有条理的学习笔记。

[English](README.md)

## 为什么选择 NoteForge？

- **智能自适应** — 根据学习目的选择大纲式、复习式、康奈尔式或阅读式笔记。
- **来源可核对** — 保留可追溯的来源信息，区分补充解释，标注存疑内容。
- **保留重要细节** — 尽可能保留公式、代码、表格和图示中的关键信息。
- **灵活输出** — 默认 Markdown，按需使用 Mermaid 图或环境支持的文档格式。
- **轻量设计** — 无额外运行依赖，无需 API Key。

无需固定模板或复杂配置，只需提供资料和学习目标。

## 安装

NoteForge 遵循 [Agent Skills 开放规范](https://agentskills.io/specification)。

使用 **Claude Code** 时，将 `SKILL.md` 放入：

```text
.claude/skills/noteforge/SKILL.md
```

其他兼容 Agent 请使用对应的 Skill 目录。

## 使用

提供资料，直接说明需求即可：

> 把这份 PPT 整理成期末复习笔记，保留重要公式和例题。

> 将这些零散课堂记录整理成简洁的 Markdown 笔记。

> 把这篇文章整理成康奈尔笔记，保留主要观点和论据。

更多示例见 [examples](examples/README.md)。

## 兼容性

NoteForge 使用 AI Agent 已有的能力。文件读取、图片理解、自动触发与格式导出取决于运行环境，不同模型的表现可能有所差异。

## 许可证

[MIT](LICENSE)
