---
name: learning-curriculum
description: "Generate a hands-on, hybrid notes-plus-code curriculum for learning a technology or library, written as a sequence of runnable files in a target folder. Use for either a whole library (broken into staged lessons) or one narrow topic within it."
when: "User asks to learn, be taught, or build a curriculum for a technology/library/framework, and wants runnable code files rather than a conversation or a written report. Trigger on: 'teach me X', 'help me learn the basics of Y', 'create a learning curriculum for Z', 'break Z down into lessons', 'generate learning files for Y in folder W'. Don't use when the user wants a Socratic dialogue (see socratic-mentor instead), a single one-off code snippet, or a written reference doc with no hands-on files."
version: 1.0.0
author: Sarah Littlejohn
license: MIT
metadata:
  hermes:
    tags: [teaching, learning, curriculum, hands-on, code-generation]
    related_skills: [socratic-mentor]
---

# learning-curriculum — Hybrid Notes + Hands-On Lesson Generator

## Overview

Turn "I want to learn X" into a sequence of small, runnable files that teach by showing and then asking the learner to do. Each file is self-contained: a short plain-language explanation, minimal working code, and exactly one exercise. The learner runs each file, sees it work, tweaks it themselves, then moves to the next.

This skill produces artefacts (files on disk), not a conversation. If the user wants to be talked through a concept via questions instead, use `socratic-mentor`. The two compose: this skill can generate the lesson files, and `socratic-mentor` can be used afterward to quiz the learner on what they wrote.

## When to Use

- The user wants to learn an entire technology/library from scratch (e.g. "teach me Qiskit", "I want to learn pandas")
- The user wants to go deep on one narrow part of a library they're already using (e.g. "just explain circuits and gates in Qiskit")
- The user wants runnable lesson files, not a written reference doc or a live Q&A session

**Don't use for:** a single quick code example, a written conceptual explainer with no files, or when the user explicitly wants Socratic questioning instead of reading+doing.

## Required Inputs

Before generating anything, confirm you have:

1. **Target folder** — where the lesson files get written. If not given, ask. Do not guess or default silently.
2. **Technology/library** — the name of what's being learned (e.g. Qiskit, pandas, React).
3. **Scope** — one of:
   - **Full library**: break the whole thing into a sequenced curriculum, foundational → advanced.
   - **Narrow topic**: go deep on one specific part only (e.g. "circuits and gates").

If scope is ambiguous, ask which one before writing files — the two modes produce very different output (many files vs. a couple).

## Before You Start: Research

Do not write lesson content from memory alone. Before drafting:

1. **Check what's actually installed.** Find the installed version of the library in the target environment (e.g. `pip show <package>`, `npm ls <package>`). Teach the API that matches the installed version, not whatever's most familiar from training — libraries deprecate and replace core APIs (e.g. Qiskit moved from `execute()`/`backend.run()` to `Sampler`/`Estimator` primitives). Flag and skip any API that's deprecated in the installed version.
2. **Match the target repo's existing style.** Look for an existing hand-written file in the repo (docstring density, comment tone, naming conventions). If one exists, mirror its voice rather than inventing a new one. If none exists, default to the file template below.
3. **Check for a project roadmap or checklist** (README, TODO, etc.) that might constrain sequencing or naming — e.g. don't duplicate work already marked done elsewhere.

## Sequencing Logic

**Full-library scope:**
Decompose the library into an ordered list of concepts, each depending only on concepts already covered. Order foundational → advanced. Typical shape (adapt per-library, this is illustrative not prescriptive):
- Core object model (the primary object you build things out of)
- Composition (combining multiple core objects / operations together)
- Execution/inspection (running or evaluating what you built, seeing results)
- Parameterization / reuse patterns
- Extension points (custom components, plugins, subclassing)
- Tooling for realistic use (optimization, deployment, backend/runtime concerns)

Aim for enough files to cover the basics without exhausting the learner — roughly 5-10 for a full library survey. If it's ballooning past that, the scope is too broad; check with the user whether to split it into multiple curricula.

**Narrow-topic scope:**
Produce 1-3 files that go deep on just that topic. Don't pad it out to look like a full sequence.

## File Template (the hybrid format)

Each concept gets its own file. Naming: `NN_topic_slug.<ext>` (zero-padded two-digit prefix, extension matching the library's language — e.g. `.py` for Qiskit/pandas, `.ts` for a JS/TS library).

Structure, in order:

1. **Notes block** (top-of-file comment/docstring): plain-language explanation of the concept — what problem it solves, not just what it's called. Follow with a short list of the key objects/functions introduced in this file, each with a one-line description.
2. **Minimal runnable code**: the smallest example that demonstrates the concept clearly. No unrelated bells and whistles.
3. **Entry point** (`__main__` block or language equivalent): running the file directly produces visible output (printed, drawn, plotted) so the learner gets immediate feedback without extra setup.
4. **Exactly one "Try it yourself" prompt** at the bottom: a specific, concrete variation the learner makes themselves — not "explore further," but a precise tweak with a predictable, checkable outcome. Point forward to what the next file will cover.

Keep each file focused on one concept. If a file needs two "Try it yourself" prompts, it's covering two concepts — split it.

## Verification

After generating each file:
1. Run it.
2. Confirm it executes without error.
3. Confirm the output matches what the notes block claims will happen.

Fix and re-verify before generating the next file in the sequence — don't let an error compound into the next lesson, since later files assume earlier ones are correct and understood.

If a file depends on an optional package (e.g. a simulator backend, a plotting library) that isn't installed, check for it and install it (or ask before installing) rather than writing an example that will fail for the learner.

## Pacing Rules

- Never introduce a concept that depends on a later one. If ordering forces a forward reference, resequence rather than explaining out of order.
- One concept per file. Resist bundling "while I'm here" extras into a file — they belong in their own numbered file.
- Match curriculum depth to what was asked: "full library" earns a real sequence; "just this one part" earns a short, deep dive, not a survey.

## What Not To Do

- Do not write files without confirming the target folder first.
- Do not teach a deprecated API path because it's more familiar than the current one — verify against the installed version.
- Do not front-load every feature of the library into file 1.
- Do not skip the run-and-verify step — an example that silently fails or prints the wrong thing teaches the wrong lesson.
- Do not add more than one exercise per file.

## Example

Invocation: technology = Qiskit, scope = full library, target folder = `learning/learning-qiskit/`.

Output: `01_circuits_and_gates.py`, `02_multi_qubit_gates.py`, `03_statevector_simulation.py`, `04_measurement_and_sampling.py`, `05_parameterized_and_rotation_gates.py`, `06_custom_gates_and_oracles.py`, `07_transpile_and_backends.py` — each following the template above, each verified to run before the next is written.

## Maintenance

Last updated: September 2026
Version: 1.0.0
Changelog:
- 1.0.0: Initial skill creation.
