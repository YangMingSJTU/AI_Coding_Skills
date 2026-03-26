---
name: continue-task
description: Continue an in-progress task by reading previously written task experience and implementation notes from Markdown files stored under the current project's `doc/` directory. Use when the user wants to resume work from prior summaries, reload the task context, continue an unfinished implementation, or reuse earlier lessons and plans. The destination subfolder name under `doc/` must be provided by the user; if it is missing, ask before reading files.
---

# Continue Task

## Overview

Load the task notes that were written during earlier work, extract the current status, decisions, and next steps, and use that information to continue the task without rebuilding context from scratch.

Treat the Markdown files in the selected `doc/` subfolder as the primary historical context for the ongoing task.

## Required User Input

The `doc/` subfolder name is required from the user.

1. If the user already provided the folder name, use it.
2. If the user did not provide the folder name, stop and ask for it before scanning any task notes.
3. Do not guess or invent the folder name.

## Input Location

Resolve the current project root from the active repository or workspace.

Read task notes from:

`<project-root>/doc/<user-folder-name>/`

Look for Markdown files such as:

- `*.md`
- dated summaries like `YYYY-MM-DD-task-topic.md`
- retrospectives, plans, or implementation notes created by earlier tasks

If the folder does not exist or contains no relevant Markdown files, say so clearly and ask whether to proceed with a fresh context build.

## Continuation Workflow

1. Ask for the `doc/` subfolder name if the user did not provide it.
2. Resolve the folder path under the current project root.
3. Read the relevant Markdown files in that folder.
4. Extract the task goal, work already completed, key decisions, unresolved issues, and suggested next steps.
5. Summarize the recovered context back to the user.
6. Continue the task using that recovered context plus the current repository state.

## What To Extract

When reading task notes, identify:

1. The original objective.
2. The chosen solution or architecture.
3. Files already touched or planned.
4. Important commands or workflows.
5. Risks, blockers, or unresolved decisions.
6. The best next action to continue the task.

## Reading Guidance

1. Prefer the most recent and most task-relevant Markdown files first.
2. If multiple files describe the same task, merge them into one coherent understanding.
3. If two notes conflict, surface the conflict to the user instead of guessing.
4. Use repository inspection to verify details when the notes may be outdated.

## Output Expectations

When finishing the context recovery step:

1. State which folder was used.
2. Mention which Markdown files were read.
3. Summarize the current task status and recommended next step.
4. If the folder name is missing, ask the user for it before proceeding.
