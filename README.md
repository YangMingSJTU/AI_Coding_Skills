# AI_Coding_Skills

Reusable Codex skills stored in Git for backup, sharing, and cross-machine setup.

## Included Skills

### `init-ai`

Initialize a workspace from a skill-local `Init.md` guide. The skill reads `Init.md` from its own folder and creates a default one automatically if it does not exist.

Repo path:

`skills/init-ai`

### `auto-push`

Commit and push the current task's Git changes safely. The skill summarizes the staged diff into a commit message, syncs with the remote branch before pushing, preserves remote changes during straightforward additive conflict resolution, and stops to ask for guidance when overlap or ambiguity exists.

Repo path:

`skills/auto-push`

### `task-summary`

Summarize the current task into a reusable Markdown recap saved under the current project's `doc/` directory. The filename is generated from the date and task topic, and the destination subfolder must come from the user rather than being guessed automatically.

Repo path:

`skills/task-summary`

### `continue-task`

Resume an in-progress task by reading prior Markdown notes from the current project's `doc/` directory. The skill requires the user to provide the subfolder name under `doc/`, then reads the relevant summaries and implementation notes to recover context and continue the work.

Repo path:

`skills/continue-task`

## Install To Codex

Codex loads user skills from the current user's `.codex/skills` directory.

- Windows: `C:\Users\<username>\.codex\skills`
- macOS: `~/.codex/skills`
- Linux: `~/.codex/skills`

Copy the `init-ai` skill folder from this repository into your local Codex skills directory so the result looks like:

- Windows: `C:\Users\<username>\.codex\skills\init-ai`
- macOS: `~/.codex/skills/init-ai`
- Linux: `~/.codex/skills/init-ai`

## Suggested Repo Layout

Store each reusable skill under `skills/<skill-name>/` so the repository can hold multiple skills over time without mixing them into the repo root.
