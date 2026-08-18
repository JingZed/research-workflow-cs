---
name: claim-evidence-mapper
description: "Map one external source paper's major claims to concrete evidence, assumptions, and gaps in its topic-level paper workspace. Use when Codex needs to audit whether that paper's stated contributions are supported by figures, tables, experiments, or assumptions before reuse, criticism, or reproduction. Do not use for the active project's manuscript claims."
---

# Claim Evidence Mapper

## Overview
Separate claims from evidence so an external source paper can be reused
critically instead of taken at face value. This Skill does not own project or
manuscript claim mapping.

## Consume
- `<topic-root>/papers/<paper-id>/paper.md`, `structure.md`, and `summary.md`
  when available.
- Optional `<topic-root>/papers/<paper-id>/figures/index.md` for figure and
  table references.
- Optional user focus on one claim, section, or experiment.

## Produce
- `<topic-root>/papers/<paper-id>/claim-evidence-map.md`

## Workflow
1. Resolve the selected `<topic-root>/papers/<paper-id>/` workspace before
   writing.
2. List the external paper's major claims in a small, ranked set rather than trying to map every sentence.
3. Attach the strongest supporting evidence for each claim, including figures, tables, or ablations when available.
4. Note hidden assumptions, weak controls, or missing evidence explicitly for each claim.
5. Distinguish the authors' claim from your confidence assessment so criticism stays precise.

## Quality Bar
- Give every claim either evidence or an explicit support gap.
- Reference the source section or artifact whenever possible.
- Keep the map easy to scan during reproduction or rebuttal work.

## Boundaries
- Do not convert the map into a rebuttal letter directly.
- Do not redesign experiments or propose a full reproduction plan here.
- Do not blur factual support with your own extension ideas.
- Do not write an idea-root or manuscript-facing `claim-evidence-map.md`.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../../_shared/templates/claim-evidence-map-template.md` when you need the specific structure, template, or integration note for this skill.
