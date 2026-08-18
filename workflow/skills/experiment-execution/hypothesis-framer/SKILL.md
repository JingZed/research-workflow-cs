---
name: hypothesis-framer
description: "Turn a research idea into a falsifiable, measurable hypothesis. Use when Codex needs to define the intervention, expected effect, failure condition, required evidence, and success threshold before designing experiments or writing a story around the project."
---

# Hypothesis Framer

## Overview
Convert an interesting idea into a testable hypothesis with explicit success and failure conditions.

## Consume
- `<topic-root>/ideas/<id>/idea.md` or a selected item from
  `<topic-root>/synthesis/idea-backlog.md`.
- `<topic-root>/synthesis/research-gaps.md` when available.
- Optional `<topic-root>/synthesis/literature-corpus.jsonl` for novelty comparison.
- Optional target task, benchmark, or constraint from the user.

## Produce
- `hypothesis.md`

## Workflow
1. Compare the candidate idea against the local corpus: identify nearest-neighbor papers by task, method family, and dataset/benchmark overlap. Classify novelty risk as low / medium / high using the same three-dimension overlap rule, and cite the concrete nearest-neighbor papers driving the verdict. Record the novelty risk level and the key nearest neighbors in `hypothesis.md` under a "Novelty Risk" section. If risk is high and the claimed delta cannot be distinguished from existing work, surface this as a blocker before writing the hypothesis body. Medium risk: record the key nearest-neighbor papers and proceed, but the hypothesis body must explicitly state what distinguishes this work from those neighbors (task, method, or benchmark delta).
2. State the intervention, the target setting, and the expected measurable effect in plain terms.
3. Add a `Competing Predictions` section. Assign every entry a stable
   `prediction_id` and one role from `favored`, `serious_rival`, or
   `null_or_artifact`. Include at least one entry for each role, and record its
   `mechanism`, `predicted_observation`, `discriminator_against`, and
   `falsifier`.
4. Make every serious rival scientifically plausible rather than a straw man,
   and make its predicted observation distinguishable from the favored and
   null-or-artifact predictions with the planned evidence.
5. Write the project-level falsification condition so the project can fail honestly instead of drifting.
6. Define the minimum evidence and threshold that would count as early success.
7. Keep the hypothesis narrow enough that it can actually drive an experiment plan.

## Quality Bar
- Make the hypothesis measurable, bounded, and falsifiable.
- Keep causal language proportional to the available evidence plan.
- Avoid vague 'improves performance' wording without task, metric, and condition.
- Medium novelty risk is not a blocker but must be accompanied by an explicit delta statement in the hypothesis.
- Do not mark the hypothesis `COMPLETE` when a required prediction role is
  missing, a serious rival is not credible, or the predicted observations
  cannot discriminate among the competing explanations.

## Boundaries
- Do not turn the hypothesis into a full experiment matrix here.
- Do not assign datasets, test families, or command-level checks to the
  prediction entries; downstream planning owns those decisions.
- Do not add milestones or schedules here. If staged scientific decisions are
  needed, keep them in the later experiment specification; operational stages
  belong in the runbook.
- Do not treat a backlog idea as selected unless the user has promoted it.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
