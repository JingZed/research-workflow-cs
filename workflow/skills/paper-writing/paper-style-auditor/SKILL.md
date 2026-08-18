---
name: paper-style-auditor
description: "Run a read-only full-manuscript language, framing, and reader-experience audit. Find AI-flavored prose, unclear jargon, defensive positioning, weak contribution framing, awkward limitations, and internal workflow leakage without editing the paper."
---

# Paper Style Auditor

## Overview

Audit the manuscript as reader-facing academic prose. This Skill does not
rejudge the experiments or edit the source.

## Consume

- A named manuscript source and optional rendered PDF.
- `<paper-dir>/INVARIANTS.md`.
- Optional style profile, translation, experiment summary, and claim-evidence
  mapping when framing depends on them.

## Produce

- `<paper-dir>/style-audit.md`

## Workflow

1. Resolve the exact manuscript and keep the pass read-only.
2. Check title, abstract, introduction, methods, results, discussion,
   limitations, captions, and conclusion for:
   - problem and contribution clarity;
   - reader-first definitions and logical progression;
   - evidence-aware result language;
   - generic transitions, repeated framing, hype, and empty boilerplate;
   - defensive self-definition and stacked disclaimers;
   - vague internal shorthand or workflow vocabulary;
   - citation-list prose instead of related-work synthesis;
   - apologetic limitations without scope or next tests;
   - cold-reader failures in labels, captions, tables, and figures.
3. Compare claim-facing wording with invariants and evidence.
4. Classify findings as blocker, major, minor, or note and cite their location.
5. Produce the smallest ordered fix package and the appropriate writing Skill
   for each issue.
6. Present the audit and wait for user approval before any edit.

## Quality Bar

- Findings quote or locate the actual problem.
- Rewrites are recommendations, not silent source mutations.
- “AI-like” is explained through concrete language patterns.

## Boundaries

- Do not edit the manuscript.
- Do not create a separate claim-scope or revision ledger.
- Do not use style preferences to broaden scientific claims.

## Open References Only As Needed

- Review `../../_shared/writing-constraint-layer.md`.
- Review a project style profile when one exists.
