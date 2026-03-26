---
name: init-ai
description: Initialize a Codex workspace from a skill-local `Init.md` file. Use when the user asks to bootstrap a repo, run an onboarding pass, load reusable setup instructions, or standardize how a new project is initialized. This skill reads `Init.md` from the `init-ai` skill folder, creates a default file if it is missing, and then follows the instructions in that file.
---

# Init AI

## Overview

Locate the `init-ai` skill directory, ensure `Init.md` exists in that directory, read it fully, and use it as the initialization guide for the current workspace.

Treat `Init.md` as the editable source of truth. Keep the workflow in this file stable and keep project-specific initialization preferences in `Init.md`.

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

## Initialization Workflow

1. Set `init_file` to `<skill-dir>/Init.md`.
2. If `Init.md` does not exist, create it with the default template shown below.
3. Read the full contents of `Init.md`.
4. Follow the instructions in `Init.md` to initialize the current workspace.
5. Keep initialization safe by default: inspect, summarize, and prepare unless `Init.md` explicitly requests file edits or commands.
6. If `Init.md` is ambiguous, make the smallest reasonable assumption and state it in the response.

## Default `Init.md` Template

Create this file when it is missing:

```md
# Init

Use this file as the initialization guide for the current workspace.

During initialization:

1. Inspect the repository structure and key configuration files.
2. Detect the main languages, frameworks, package managers, and test commands.
3. Summarize important entry points, development commands, and project conventions.
4. Call out obvious risks, missing dependencies, or setup blockers.
5. Do not edit files during initialization unless the user explicitly asks for changes.
6. End with a short "next steps" list for the user.
```

## Output Expectations

When using this skill:

1. Mention which `Init.md` path was used.
2. Say whether the file already existed or was created from the default template.
3. Summarize the initialization result concisely.
