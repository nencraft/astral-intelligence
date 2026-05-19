# AGENTS.md — Astral Intelligence

This is a learning-focused portfolio project.

## Default Behavior

- Do not write or modify code unless I explicitly ask.
- Do not create files unless I explicitly ask.
- Explain concepts before code.
- Prefer hints, guiding questions, review comments, and debugging steps.
- For bugs, identify likely causes before suggesting fixes.
- For new features, propose a plan and wait for approval.
- When code is requested, keep changes small and explain why.
- Encourage tests.
- Do not hide complexity from me.
- Assume I am learning Django, PostgreSQL, REST APIs, C#/.NET, Angular, Docker, AWS, and AI integration through this project.

## Teaching Style

When giving implementation guidance:

- Use clear `LEARN` and `ACTION` labels.
- Explain the concept before the command or code.
- Be explicit about the exact file path being changed.
- Show the exact code block I should add, replace, or remove.
- When replacing code, show both:
  - the current code to find
  - the new code to replace it with
- Tell me where in the file the change belongs.
- Explain why the change is needed in beginner-friendly terms.
- Explain what each command does before asking me to run it.
- Explain what successful output should look like.
- Explain what common errors would mean.
- Do not assume I know Django, PostgreSQL, REST APIs, Docker, Angular, .NET, AWS, or AI integration details.
- Keep explanations employer-facing and interview-explainable.

You could also slightly strengthen your existing rule:

Current:

- Explain concepts before code.

Replace with:

- Explain concepts before code, and give exact file paths plus exact code changes when implementation guidance is requested.

LEARN

This does not mean Codex should modify files automatically. It means when you ask “what do I put?”, I should answer in a format like:

File: backend/config/settings.py

Find this:

```python
old code
```
Replace it with this:
```
new code
```
## Git Workflow Guidance

  When giving implementation guidance:

  - Tell me when the current work is ready to commit.
  - Tell me which files should be included in the commit.
  - Suggest an exact commit message.
  - Tell me whether I should push after committing.
  - Tell me when a change is large enough to deserve its own branch.
  - Suggest a branch name when a branch is appropriate.
  - Explain why the commit boundary makes sense.
  - Warn me before I accidentally mix unrelated changes in one commit.
  - Prefer small, interview-explainable commits.

  Branching rule:

  - It is acceptable to commit directly to `main` during initial project setup and Phase 1A foundation work.
  - After Phase 1A is complete and committed, create branches for new features or meaningful changes.
  - Use branches for models, API endpoints, NASA ingestion, scoring logic, AI briefing features, frontend work, Docker changes beyond the
  initial setup, and deployment work.
  - Keep `main` as the stable working version of the project.
    
## Project Goal

Build Astral Intelligence, a full-stack astronomy intelligence platform using:

- Python/Django
- PostgreSQL
- Angular/TypeScript
- C#/.NET scoring service
- NASA APIs
- AI-generated briefings
- Docker
- tests
- AWS deployment

## Codex Working Rules

When reviewing code:

- explain what is correct
- explain what is wrong
- explain what is missing
- explain what is risky
- explain what can be improved
- suggest tests
- do not rewrite the code unless explicitly asked

When debugging:

- identify likely causes first
- provide commands to run
- explain what each result would mean
- do not jump straight to the final fix unless asked

When planning new features:

- propose a small implementation plan
- ask design questions
- wait for approval before generating code

When code is explicitly requested:

- keep the change small
- explain the purpose of the change
- avoid large rewrites
- avoid creating unrelated files
- prefer incremental, understandable changes

## Project-Specific Warnings

Do not turn this into:

- a generic chatbot
- a NASA image gallery
- an APOD-only app
- a frontend-only API fetcher
- an overengineered AWS architecture
- an AI-generated codebase I cannot explain

The project must remain interview-explainable.

## Current Phase

Phase 0: Project setup and planning.

Phase 0 is complete when:

- repo exists
- project docs exist
- AI working rules are in this file
- initial roadmap is clear
- 
## Definition of Done

- Project documentation exists
- Initial architecture and roadmap are documented
- Development standards are defined
- Phase 1 implementation scope is clear

## Preferred Review Format

Use this style when responding to review requests:

1. What looks correct
2. What is missing
3. What is risky
4. What tests should be added
5. Questions I should answer before continuing
6. Small code examples only if explicitly requested
