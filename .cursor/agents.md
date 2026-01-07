# Agent Instructions

These instructions apply to all agent actions in this repository.

## Communication Style
- Always be concise and clear.
- Prefer simple, direct explanations.
- Avoid unnecessary verbosity.

## Engineering Principles
- Do not over-engineer solutions.
- Prefer the simplest approach that satisfies the requirements.
- Minimize code changes and diff size.
- Avoid refactoring unless explicitly requested or clearly necessary.

## Assumptions and Uncertainty
- Do not make unstated assumptions.
- If a decision depends on missing, ambiguous, or uncertain information, ask a clarification question before proceeding.
- Pause execution when clarification is required rather than guessing.

## Data Analytics Constraints
- Treat all raw and source data as read-only.
- Never overwrite source tables, files, or datasets.
- Create derived tables, views, or outputs instead of modifying originals.
- Do not invent metric definitions or business logic.
- Reuse existing metrics and definitions when available.
- Explicitly state assumptions behind transformations and calculations.
- Prefer deterministic and reproducible transformations.
- Avoid randomness, sampling, or implicit ordering unless explicitly requested.
- Be mindful of query performance and cost.
- Avoid unnecessary full-table scans, joins, or materializations.

## Tooling and Dependencies
- Use existing tools, libraries, and patterns already present in the project.
- Do not introduce new dependencies, frameworks, or tools without explicit approval.

## Documentation Expectations
- Briefly document non-obvious transformations or decisions.
- Focus documentation on why a decision was made, not restating the code.

## General Behavior
- Follow existing project structure and conventions.
- Respect project scope and constraints.
- Optimize for correctness, readability, and maintainability over cleverness.
