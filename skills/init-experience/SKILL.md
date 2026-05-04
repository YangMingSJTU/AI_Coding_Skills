---
name: init-experience
description: Load experience notes and reusable preferences from an `Experience.md` file in the current working directory root. Use when the user wants to initialize the current workspace from project-local experience notes, coding conventions, lessons learned, or operating guidance stored in `Experience.md`. This skill creates `Experience.md` in the current project root if it is missing, then reads and applies the information in that file.
---

# Init Experience

## Overview

Locate `Experience.md` in the current project root, create it if missing, then read and apply its contents as the workspace-local experience and guidance source.

Do not read from the skill directory. This skill works from the current working directory root so it can travel with the project across Windows, macOS, and Linux.

## Locate The File

Resolve the project root from the current working directory.

Use this file path:

`<project-root>/Experience.md`

This works cross-platform because the resolved project root may be:

- Windows: `C:\path\to\project\Experience.md`
- macOS: `/Users/<user>/path/to/project/Experience.md`
- Linux: `/home/<user>/path/to/project/Experience.md`

## Load Workflow

1. Set `experience_file` to `<project-root>/Experience.md`.
2. If `Experience.md` does not exist, create it with the default template shown below.
3. Read the full contents of `Experience.md`.
4. Load and apply the instructions, conventions, lessons, and preferences written in `Experience.md`.
5. If `Experience.md` is ambiguous, ask the user instead of expanding the scope on your own.

## Default `Experience.md` Template

Create this file when it is missing:

```md
# Experience

Use this file as the project-local experience and guidance source for the current workspace.

By default, when this file is loaded:

1. Read and apply the information in this file.
2. Treat this file as the source of truth for project-local lessons, conventions, and preferences.
3. Ask the user for clarification whenever the scope is ambiguous.
```

## Output Expectations

When using this skill:

1. Mention which `Experience.md` path was used.
2. Say whether the file already existed or was created from the default template.
3. Summarize what information was loaded from `Experience.md` concisely.
