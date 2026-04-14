---
name: new-branch
description: Create a new branch from a user-specified remote base branch and switch the local repository to the new branch. Use when the user wants to start work from an existing remote branch, create a fresh working branch from a remote base, or standardize branch creation workflow. The remote base branch must come from the user; if the user does not provide it, ask before proceeding.
---

# New Branch

## Overview

Create a new branch from a remote branch chosen by the user, create the remote branch first, then clean and switch the local repository to that new branch using a fixed Git workflow.

Treat the remote base branch as required user input. Do not choose it implicitly from `main`, `master`, or any current branch.

## Required User Input

Require these inputs before running the branch workflow:

1. The remote base branch to branch from.
2. The new branch name to create.

Rules:

1. If the remote base branch is missing, ask the user for it before doing anything else.
2. Do not choose a remote base branch on the user's behalf.
3. If the new branch name is missing or unclear, ask the user for it.
4. Confirm the exact remote base branch name and new branch name before destructive cleanup commands.

## Branch Creation Workflow

Follow this workflow in order:

1. Validate the user-provided remote base branch.
2. Create the new branch on the remote based on that remote branch.
3. Run `git reset --hard` locally to clean the worktree as requested.
4. Run `git fetch`.
5. Run `git checkout {new_branch}` to switch to the new branch locally.

Do not reorder these steps unless the user explicitly requests a different workflow.

## Safety Rules

Because `git reset --hard` is destructive:

1. Make sure the user already requested this skill or this exact workflow.
2. Make sure the remote base branch and new branch name are explicit.
3. Do not silently preserve local changes unless the user asks for that behavior.
4. Do not guess whether uncommitted work should be kept.

## Output Expectations

When finishing:

1. State which remote base branch was used.
2. State which new branch was created.
3. State whether the remote branch creation succeeded.
4. State whether the local checkout succeeded.
5. If the remote base branch was missing, ask the user for it before proceeding.
