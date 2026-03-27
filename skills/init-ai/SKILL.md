---
name: init-ai
description: Load instructions and preferences from a skill-local `Init.md` file. Use when the user asks to load reusable setup rules, personal preferences, or initialization guidance from `Init.md`. This skill reads `Init.md` from the `init-ai` skill folder, creates a default file if it is missing, and limits itself to loading and applying the information in that file unless the user explicitly asks for additional project analysis or initialization work.
---

# Init AI

## Overview

Locate the `init-ai` skill directory, ensure `Init.md` exists in that directory, read it fully, and use it as the loaded instruction set for the current workspace.

Treat `Init.md` as the editable source of truth. Do not add extra project understanding, repo inspection, or initialization steps unless they are explicitly written in `Init.md` or explicitly requested by the user.

## Locate The Skill Directory

Resolve the skill directory with this priority order:

1. Use the explicit skill path from the user's prompt when one is provided.
2. Otherwise use the directory that contains this `SKILL.md`.
3. Do not hardcode a username.

Default install locations are:

- Windows: `%USERPROFILE%\.codex\skills\init-ai`
- macOS: `~/.codex/skills/init-ai`
- Linux: `~/.codex/skills/init-ai`

Always read and write `Init.md` inside the resolved skill directory.

## Load Workflow

1. Set `init_file` to `<skill-dir>/Init.md`.
2. If `Init.md` does not exist, create it with the default template shown below.
3. Read the full contents of `Init.md`.
4. Load and apply the instructions, constraints, and preferences written in `Init.md`.
5. If `Init.md` is ambiguous, ask the user instead of expanding the scope on your own.

## Default `Init.md` Template

Create this file when it is missing:

```md
# Init

Use this file as the initialization guide for the current workspace.

By default, when this skill is invoked:

1. Read and apply the information in this file.
2. Treat this file as the source of truth for preferences and constraints.
3. Ask the user for clarification whenever the scope is ambiguous.
```

## Output Expectations

When using this skill:

1. Mention which `Init.md` path was used.
2. Say whether the file already existed or was created from the default template.
3. Summarize what information was loaded from `Init.md` concisely.
