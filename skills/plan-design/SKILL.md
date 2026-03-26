---
name: plan-design
description: Compare multiple implementation approaches for a user requirement and recommend the best solution before coding. Use when the user asks for solution design, architecture choices, tradeoff analysis, feasibility evaluation, implementation options, or a recommended approach. This skill proposes 2-5 reasonable options, compares them across feasibility, implementation efficiency, compatibility, architectural fit, and change risk, and then gives a clear recommendation with rationale.
---

# Plan Design

## Overview

Take a concrete requirement or design problem, generate a small set of realistic implementation options, and help the user choose by comparing tradeoffs in a balanced, decision-friendly format.

Default to chat-first output. The goal is to help the user make a decision, not to write a full RFC unless the user asks for more depth.

## Required Input Quality

Require a concrete problem, requirement, or design decision to evaluate.

If the request is too vague, ask for the missing context before proposing options. Examples of missing context:

1. The feature or problem being solved.
2. Important constraints such as performance, compatibility, deadlines, or platform limits.
3. Whether the user is optimizing for speed, maintainability, minimal change, or long-term architecture.

Do not fake precision when the real constraints are missing.

## Option Count Rules

Generate between 2 and 5 options:

1. Use 2 or 3 options for narrow or tightly constrained problems.
2. Use 4 or 5 options only when the solution space is genuinely broad enough to justify it.
3. Do not pad the list with weak or unrealistic options just to reach a number.

## Comparison Framework

Evaluate each option against the same default dimensions:

1. Feasibility
2. Implementation efficiency
3. Compatibility with the current system or constraints
4. Architectural reasonableness
5. Change risk

Add more dimensions only when the problem clearly requires them, such as:

- Performance impact
- Rollout complexity
- Testing burden
- Migration cost
- Operational risk

## Output Structure

Use this structure by default:

1. Problem summary
2. Assumptions or constraints used
3. Option 1
4. Option 2
5. Additional options when justified
6. Recommended option
7. Why this recommendation wins
8. Optional next step or validation suggestion

For each option, include:

- A short implementation summary
- Main advantages
- Main disadvantages
- Best-fit scenario or when to choose it

## Recommendation Rules

Always recommend one option when the available information is sufficient.

The recommendation should:

1. Be explicit and decisive.
2. Explain why it wins against the alternatives.
3. Match the user's likely priorities and constraints.
4. Still surface important tradeoffs the user should know.

If no option is clearly safe because key constraints are unknown, say that directly and list what must be clarified before choosing.

## Writing Style

Default to a balanced comparison:

1. Give enough detail to support a decision.
2. Avoid turning the answer into a long architecture document unless requested.
3. Prefer concise tradeoff analysis over generic theory.
4. Keep options realistic for the current context.

## Output Expectations

When finishing:

1. State how many options were compared.
2. Show the recommendation clearly.
3. Explain the top tradeoffs in plain language.
4. If the request was too vague, ask targeted follow-up questions instead of inventing assumptions.
