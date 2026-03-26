---
name: auto-push
description: Safely commit and push all files changed for the current task to the active Git remote branch. Use when the user asks to submit the work from the current conversation, generate a commit message from the actual modifications, sync with the remote branch before pushing, and resolve straightforward conflicts by preserving remote changes while adding local new features. If remote and local changes overlap semantically or the correct merge is unclear, stop and ask the user how to proceed.
---

# Auto Push

## Overview

Review the current repository changes, stage the files that belong to the current task, write a concise commit message based on the diff, and push the result to the current branch on the configured remote.

Keep the workflow conservative. Prefer pausing for user confirmation over guessing on ambiguous merge conflicts.

## Safety Rules

1. Work only inside the repository that is relevant to the current conversation.
2. Include only files that were modified for the current task. If unrelated local changes are present and cannot be separated confidently, stop and ask the user.
3. Never rewrite history with `git push --force` unless the user explicitly asks for it.
4. Never discard remote changes.
5. If a merge or rebase conflict is not obviously additive, stop and ask the user.

## Standard Workflow

1. Inspect the worktree with non-destructive Git commands such as `git status --short`, `git diff --stat`, `git diff`, and `git branch --show-current`.
2. Identify the active branch and its upstream remote. If no upstream exists, stop and ask the user what remote branch to use.
3. Determine which modified files belong to the current task.
4. Stage only those files.
5. Summarize the staged diff and write a commit message that reflects the actual change.
6. Commit with a non-interactive Git command.
7. Fetch and integrate the latest remote changes before pushing. Prefer `git pull --rebase` when the branch has a clean linear history and no merge commit is required by the repo workflow.
8. If integration succeeds without conflict, push to the upstream branch.
9. Report the commit summary, branch, and push result.

## Commit Message Rules

Generate the commit message from the staged diff:

1. Use one concise subject line.
2. Prefer imperative phrasing such as `Add`, `Update`, `Fix`, `Refactor`, or `Document`.
3. Mention the main feature or file group, not every file.
4. Do not use placeholder text.

## Conflict Handling

When remote changes arrive during pull, rebase, or merge:

1. Compare the remote and local edits at the conflicting files.
2. If the remote change and the local change affect clearly different logic, preserve the remote change and re-apply the local new feature on top.
3. If both sides changed the same lines, same behavior, same API shape, or the intent might overlap, stop and ask the user how to resolve it.
4. If the correct result depends on product intent, coding style preference, or hidden business rules, stop and ask the user.
5. After manual conflict resolution, re-run the relevant status and diff checks before continuing.

Examples of conflicts that require asking the user:

- Both remote and local rename the same method differently.
- Both remote and local edit the same prompt or user-facing copy.
- Both remote and local change dependency versions or config defaults.
- It is unclear whether the remote edit already implements the local feature.

## Decision To Ask The User

Pause and ask the user instead of proceeding when any of these are true:

1. The current task files cannot be separated from unrelated local changes.
2. The upstream branch is missing or unclear.
3. The push would require force-push.
4. A conflict involves overlapping or similar changes.
5. The final merged behavior is uncertain.

## Output Expectations

When finishing the task:

1. State which files were included in the commit.
2. Show the final commit message.
3. State which branch and remote were used.
4. If the push stopped for a conflict or uncertainty, explain exactly what needs user input.
