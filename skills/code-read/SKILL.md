---
name: code-read
description: Read and explain a user-specified code scope in beginner-friendly language, describe the core architecture and behavior in detail, expand technical terms with simple definitions, and generate a Markdown walkthrough plus SVG diagrams under the current project's `doc/code_read/` directory. Use when the user asks to understand, summarize, walk through, explain, or diagram files, folders, modules, or features. The user must provide both the code scope and the destination subfolder name under `doc/code_read/`; if either is missing or too vague, ask before proceeding.
---

# Code Read

## Overview

Read a clearly defined part of the codebase, explain how it works as if teaching a technical beginner, and save the explanation as a Markdown report with one or more supporting SVG diagrams.

Prefer clarity over completeness. The goal is not to dump every line of code, but to help a newcomer quickly understand the important structure, flow, and vocabulary.

## Required User Input

Require these inputs before doing the write-up:

1. The code scope to analyze, such as a file, folder, module, service, or feature.
2. The destination folder name under `doc/code_read/`.

Rules:

1. If the user did not provide the folder name, ask for it before creating files.
2. If the user did not provide a clear code scope, ask the user to narrow it.
3. Never guess the folder name.
4. Never pretend the scope is precise when it is still ambiguous.

## Output Location

Resolve the current project root from the active workspace or repository.

Save outputs to:

`<project-root>/doc/code_read/<user-folder-name>/`

Create the folder if it does not already exist.

## File Naming

Generate filenames from the current date plus a short topic slug derived from the analyzed scope.

Use this pattern:

- Markdown report: `YYYY-MM-DD-<topic>-code-read.md`
- Required overview SVG: `YYYY-MM-DD-<topic>-overview.svg`
- Optional flow SVG: `YYYY-MM-DD-<topic>-flow.svg`
- Optional module SVG: `YYYY-MM-DD-<topic>-modules.svg`

Keep the topic slug short, lowercase, and hyphenated.

## Reading Workflow

1. Confirm the scope and output folder name.
2. Read the relevant code files and surrounding context needed to understand them.
3. Identify the big-picture architecture, major modules, execution flow, and important dependencies.
4. Translate technical ideas into plain language suitable for a beginner.
5. Expand jargon with short explanations when a term first appears.
6. Produce a Markdown explanation and at least one SVG overview diagram.
7. Add one or two more SVG diagrams only when they add real clarity.
8. Save the files under `doc/code_read/<user-folder-name>/`.

## Writing Style

Write for a technical beginner:

1. Use simple language first.
2. Explain unfamiliar terms in one short sentence.
3. Prefer analogies and concrete examples when helpful.
4. Avoid assuming the reader already understands framework jargon.
5. Focus on helping the reader build a mental model of the system.

## Recommended Markdown Structure

Use this structure by default:

```md
# Code Read: <scope title>

## Background
What was analyzed and why.

## Big-Picture Architecture
The main building blocks and how they relate.

## Main Modules And Responsibilities
What each important file, module, or layer is responsible for.

## Key Flow
How control, requests, or data move through the system.

## Important Concepts
Beginner-friendly explanations of key technical terms.

## How It Works Together
How the pieces combine to deliver the feature or behavior.

## Risks Or Confusing Areas
Places that may be easy to misunderstand or fragile to change.

## Suggested Next Reading
Useful follow-up files or concepts to study next.
```

Link the generated SVG files from the report and embed them when appropriate.

## Diagram Rules

Always generate at least one SVG overview diagram.

Optional additional diagrams:

1. A flow diagram when execution order matters.
2. A module diagram when relationships between components need extra clarity.

Guidelines:

1. Keep diagrams simple and readable.
2. Use beginner-friendly labels.
3. Prefer grouped components over line-by-line detail.
4. Skip extra diagrams when they would be redundant or low-signal.

## Output Expectations

When finishing:

1. State which scope was analyzed.
2. State which folder was used under `doc/code_read/`.
3. Return the saved Markdown path.
4. Return the saved SVG paths.
5. If the scope or folder name is missing, ask the user before continuing.
