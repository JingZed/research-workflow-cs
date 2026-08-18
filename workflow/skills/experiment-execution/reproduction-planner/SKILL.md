---
name: reproduction-planner
description: "Plan how to reproduce a target paper or baseline. Use when Codex needs to turn a paper into a concrete reproduction checklist covering code, environment, data, hidden assumptions, checkpoints, and minimum success conditions before any execution starts."
---

# Reproduction Planner

## Overview
Make reproduction explicit enough that hidden prerequisites surface before you burn time on execution.

## Consume
- `<topic-root>/papers/<paper-id>/summary.md`, `claim-evidence-map.md`,
  `paper.md`, and `meta.yaml` for the external target paper.
- Optional public code links, repository notes, or environment constraints.
- Optional target fidelity level such as exact reproduction or functional baseline.

## Produce
- `experiments/plans/reproduction-plan.md`

## Workflow
1. List all known prerequisites: code, data, checkpoints, libraries, hardware, and evaluation scripts.
2. Separate confirmed requirements from assumptions inferred from the paper.
3. Define the minimum reproduction target so success does not remain vague.
4. Record blockers and fallback branches when public artifacts are incomplete or unavailable.

## Quality Bar
- Expose hidden dependencies and nontrivial assumptions early.
- Keep success criteria realistic and measurable.
- Distinguish exact-match goals from approximate baseline goals.

## Boundaries
- Do not run experiments from this artifact.
- Do not design novel ablations beyond what the reproduction target needs.
- Do not hide missing resources; surface them as blockers.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
