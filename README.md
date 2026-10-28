# NoteForge

**From messy materials to notes worth keeping.**

A lightweight, source-aware [Agent Skill](https://agentskills.io/) that turns lecture slides, PDFs, documents, images, and rough notes into clear, structured study notes.

[简体中文](README.zh-CN.md)

## Why NoteForge?

- **Adaptive notes** — Outlines, revision notes, Cornell notes, or reading notes, tailored to your learning goals.
- **Source-aware** — Preserves traceable references, separates added explanations, and flags uncertain content.
- **Details matter** — Keeps important formulas, code, tables, and diagram information.
- **Flexible output** — Markdown by default, with optional Mermaid diagrams and supported document exports.
- **Lightweight** — No additional runtime dependencies or API keys.

No rigid templates. No unnecessary setup. Just your materials and your learning goal.

## Installation

NoteForge follows the [Agent Skills specification](https://agentskills.io/specification).

For **Claude Code**, place `SKILL.md` at:

```text
.claude/skills/noteforge/SKILL.md
```

For other compatible agents, use their respective Skill directories.

## Usage

Provide your materials and describe what you need:

> Turn these lecture slides into exam revision notes, preserving key formulas and examples.

> Organize these scattered notes into a concise Markdown study guide.

> Create Cornell notes from this article, keeping its main arguments and evidence.

See [examples](examples/README.md) for sample inputs and outputs.

## Compatibility

NoteForge uses your AI agent's existing capabilities. File reading, image understanding, automatic activation, and document exports depend on the host environment. Results may vary by model.

## License

[MIT](LICENSE)
