---
name: experience-summary
description: Summarize reusable experience, common mistakes, and durable lessons from the current task, then record them into an experience record file. Use when the user wants to preserve generally useful经验, recurring pitfalls, or typical implementation mistakes discovered while completing a task. If the user provides a target file path, use that path. Otherwise use `Experience.md` in the current working directory root. If the target file does not exist, do not create it automatically; tell the user the file is missing and ask what to do next. If the user already provides specific experience items to record, ask whether the assistant should also summarize additional experience from the current task before writing.
---

# Experience Summary

## Overview

Collect the parts of the current task that are broadly reusable, especially common mistakes and generally useful lessons, and append or organize them into the chosen experience record file.

This skill supports both an explicit user-provided file path and a default project-root path. The default path works across Windows, macOS, and Linux.

## Locate The File

Choose the experience file path with this priority:

1. If the user explicitly provides a file path, use that file path.
2. Otherwise resolve the project root from the current working directory and use the default file path below.

Default file path:

`<project-root>/Experience.md`

This works cross-platform because the resolved project root may be:

- Windows: `C:\path\to\project\Experience.md`
- macOS: `/Users/<user>/path/to/project/Experience.md`
- Linux: `/home/<user>/path/to/project/Experience.md`

## Missing File Rule

If the chosen experience file does not exist:

1. Do not create the file automatically.
2. Tell the user that the target experience file is missing.
3. Ask the user what to do next.

## Input Handling

When the user already provides specific experience items to record:

1. Ask whether those provided items are the only things to record.
2. Ask whether the assistant should also summarize additional reusable experience from the current task.
3. Do not assume the user wants automatic extra summarization if they already provided curated content.

## Summary Workflow

1. Locate the user-provided experience file path when available, otherwise `<project-root>/Experience.md`.
2. If the file is missing, stop and ask the user what to do next.
3. Review the current conversation and repository context to identify reusable experience and common mistakes.
4. If the user already provided experience items, ask whether to record only those items or also summarize more from the current task.
5. Extract durable lessons rather than one-off transcript details.
6. Organize the new content so it fits cleanly into `Experience.md`.
7. Write the updated `Experience.md`.

## What To Record

Prefer content such as:

1. Reusable implementation经验
2. Common error patterns
3. Fragile steps that are easy to get wrong
4. Better default practices discovered during the task
5. Constraints or caveats that are likely to matter again

Do not record noise such as transient chat wording or purely task-specific trivia unless it has future reuse value.

## Writing Guidance

1. Write concise, reusable notes.
2. Prefer generalized lessons over raw task transcript.
3. Separate typical mistakes from recommended practices when possible.
4. Keep the file easy to scan for future tasks.

## Output Expectations

When finishing:

1. Mention which experience record file path was used.
2. State whether the file existed or the workflow stopped because it was missing.
3. State what categories of experience were added or updated.
4. If the user supplied explicit experience items, say whether the result included only those items or also task-derived additions.
