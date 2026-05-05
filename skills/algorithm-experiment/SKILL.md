---
name: algorithm-experiment
description: Summarize the key data, design intent, core findings, and follow-up directions from the current algorithm training or evaluation task, then record them into `Algorithm_Experiment.md` in the current working directory root. Use when the user wants to preserve experiment context from conversation history, logs, screenshots, charts, or other image data related to an algorithm run. This skill is optimized for downstream AI analysis accuracy. It creates `Algorithm_Experiment.md` in the current project root if it is missing, then appends a short, high-signal, fixed-format experiment entry instead of a broad narrative summary.
---

# Algorithm Experiment

## Overview

Collect only the highest-signal information from the current algorithm experiment, including design rationale, key metrics, critical evidence, and next exploration directions, then organize it into a short fixed-format Markdown entry.

This skill works from the current working directory root so it can travel with the project across Windows, macOS, and Linux.

## Locate The File

Resolve the project root from the current working directory.

Use this file path:

`<project-root>/Algorithm_Experiment.md`

This works cross-platform because the resolved project root may be:

- Windows: `C:\path\to\project\Algorithm_Experiment.md`
- macOS: `/Users/<user>/path/to/project/Algorithm_Experiment.md`
- Linux: `/home/<user>/path/to/project/Algorithm_Experiment.md`

## Record Workflow

1. Set `experiment_file` to `<project-root>/Algorithm_Experiment.md`.
2. If `Algorithm_Experiment.md` does not exist, create it with the default template shown below.
3. Review the current conversation, user-provided logs, and user-provided image data related to the algorithm run.
4. Extract only the experiment title, record time, design goal, core data, key result, key failure or risk, and next direction.
5. Append one short fixed-format entry to `Algorithm_Experiment.md`.

If the available logs or images are incomplete or ambiguous, say so explicitly and record only what can be defended from the evidence.

## What To Extract

Prefer content such as:

1. Experiment title
2. Record time
3. Design goal
4. Core metrics and the few most decision-relevant data points
5. Main conclusion from logs, charts, screenshots, or visual evidence
6. Key failure or risk
7. Next exploration direction

Do not record unsupported guesses as facts.
Do not paste raw logs.
Do not describe images in detail when one conclusion sentence is enough.
Do not repeat background already known from prior entries.

## Compression Rules

Use a strict short-entry policy:

1. Default target is 5-8 lines per experiment entry.
2. Each field should be one short sentence or one compact clause.
3. Keep only the most decision-relevant metrics.
4. Collapse logs and images into evidence summaries instead of copying source material.
5. Omit low-signal observations and redundant context.

Allow one optional `Supplement:` line only when:

1. A critical metric needs one extra clarification.
2. A log anomaly cannot be represented cleanly in the main fields.
3. An image-derived conclusion needs one extra sentence for context.

## Default `Algorithm_Experiment.md` Template

Create this file when it is missing:

```md
## Experiment Entry: <timestamp> | <title>
Design Goal: <short design goal and purpose>
Core Data: <few key metrics or highest-signal evidence>
Key Result: <main conclusion from this run>
Key Failure Or Risk: <main failure, anomaly, or risk>
Next Direction: <next exploration direction>
Supplement: <optional one-line clarification only when needed>
```

Use headings equivalent to the user's preferred format. If the user wants Chinese headings in the final `Algorithm_Experiment.md`, write the final file in Chinese.

## Writing Guidance

1. Prioritize downstream AI parsing accuracy over narrative completeness.
2. Separate observed facts from interpretation when needed.
3. Keep each entry self-contained but minimal.
4. Use the user's logs and images as primary evidence when available.
5. Do not expand beyond the fixed block unless the single optional supplement is necessary.

## Multi-Entry Behavior

1. Keep appending entries to the same `Algorithm_Experiment.md`.
2. Use the same fixed block template for every entry.
3. Let later AI identify the latest entry by the block header and timestamp.
4. Keep each entry short enough that multiple historical entries do not overwhelm later analysis.

## Output Expectations

When finishing:

1. Mention which `Algorithm_Experiment.md` path was used.
2. Say whether the file already existed or was created from the default template.
3. Summarize which categories of information were added or updated.
