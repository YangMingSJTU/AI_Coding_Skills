---
name: task-summary
description: Summarize and retrospect on the current task, including the problem, solution, implementation details, lessons learned, and follow-up notes, then save the result as a Markdown file under the current project's `doc/` directory. Use when the user asks to capture implementation experience, record a task recap, document a completed solution, or preserve lessons from the current conversation. If the user provides a destination subfolder name under `doc/`, use it; otherwise generate one automatically from the current timestamp and task topic.
---

# Task Summary

## Overview

Review the work completed in the current task, extract the important decisions and implementation details, and write a concise but useful Markdown recap for future reference.

Always save the summary under the current project root, inside `doc/<folder-name>/`.

## Folder Naming

Choose the destination folder name with this priority:

1. If the user already provided the folder name in the request, use it.
2. Otherwise generate it automatically from the current timestamp and task topic.

Recommended pattern:

`YYYYMMDD-HHMMSS-task-topic`

Keep the generated folder name short, lowercase, and hyphenated.

## Output Location

Resolve the project root from the current working repository or workspace.

Write the final file to:

`<project-root>/doc/<folder-name>/<generated-file-name>.md`

Create the `doc/` directory and the chosen subfolder if they do not already exist.

## File Naming

Generate the Markdown filename automatically from:

1. The current date in `YYYY-MM-DD` format.
2. A short slug derived from the task topic.

Recommended pattern:

`YYYY-MM-DD-task-topic.md`

Examples:

- `2026-03-26-init-ai-skill.md`
- `2026-03-26-git-auto-push-skill.md`

Keep the slug short, lowercase, and hyphenated.

## Summary Workflow

1. Inspect the current conversation and repository changes to understand what was done.
2. Identify the task goal, the chosen solution, the implementation steps, and any tradeoffs.
3. Capture the most reusable lessons, caveats, and follow-up suggestions.
4. Choose the output folder name by using the user-provided name or generating one automatically.
5. Generate the output path using the chosen folder name and auto-generated filename.
6. Write the Markdown summary file.
7. Report the saved path back to the user.

## Recommended Markdown Structure

Use a concise structure like this:

```md
# Task Summary: <task title>

## Background
Brief description of the original request and context.

## Solution
What was built or changed, and why this approach was chosen.

## Implementation
Key files, commands, workflows, or technical decisions.

## Lessons Learned
Reusable takeaways, pitfalls, or debugging insights.

## Next Steps
Optional follow-up work or maintenance notes.
```

## Writing Guidance

1. Focus on durable, reusable knowledge rather than raw chat transcript.
2. Keep the summary specific to the task that was actually completed.
3. Mention concrete file paths or commands when they help future reuse.
4. Avoid unnecessary verbosity.

## Output Expectations

When finishing:

1. State whether the summary file was created successfully.
2. Return the exact saved path.
3. Mention the generated filename.
4. Mention whether the folder name was user-provided or auto-generated.
