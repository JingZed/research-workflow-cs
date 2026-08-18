---
name: claim-reference-auditor
description: "Narrow audit for whether manuscript claims are actually supported by their citations. Use when Codex needs to check claim-citation faithfulness before package readiness or manuscript review and produce `{paper-dir}/claim-ref-audit.md`."
---

# Claim Reference Auditor

## Overview
Check whether cited manuscript claims are actually supported by their cited
sources without rewriting the manuscript or becoming a full peer review.

## Consume
- Current manuscript draft from `paper/` or `drafts/`; prefer a materialized
  `paper/` workspace when available.
- `refs.bib`.
- Optional `<paper-dir>/INVARIANTS.md`, `claim-evidence-map.md`, and
  `experiments/results/summary.md` when citation wording also carries a
  paper-specific scope or evidence boundary.
- Optional `<paper-dir>/provenance.yaml` for citation locator or evidence trace
  hints.
- Optional locator metadata from refs, notes, summaries, or bibliography side
  metadata when available.

## Produce
- `<paper-dir>/claim-ref-audit.md`

## Workflow
1. Resolve the active manuscript source. Prefer `paper/` if materialized;
   otherwise inspect `drafts/`. Require an active `<paper-dir>` for canonical
   output. If no active `<paper-dir>` can be resolved, produce a blocker note
   in the session or the requesting skill's owned artifact and do not create
   `drafts/claim-ref-audit.md`.
2. Extract cited claims, prioritizing numeric, quantitative, causal,
   comparison, categorical, and trend claims.
3. For each citation, check that the cite key exists in `refs.bib`.
4. Check faithfulness: decide whether the cited source semantically supports
   the manuscript claim, using locator or provenance evidence when available.
   LLM-as-judge reasoning must state the evidence trail; do not mark a claim
   `supported` without an explicit source path, locator, excerpt, summary, or
   provenance chain.
5. When a claim also depends on project evidence or a paper-local invariant,
   verify that the citation has not been asked to support a stronger statement
   than either source allows.
6. Emit one per-claim verdict: `supported`, `unsupported`, `anchorless`,
   `fabricated`, or `access-limited`.
7. Summarize `unsupported` and `fabricated` findings as blockers, `anchorless`
   findings as warnings, and `access-limited` findings as warnings or blockers
   depending on claim criticality.

## Quality Bar
- Do not mark a paywall-blocked, unavailable, or otherwise inaccessible source
  as `fabricated`; mark it `access-limited`.
- Do not mark LLM inference as `supported` without a reasoning path grounded in
  visible source, locator, provenance, or project evidence.
- Every high-risk finding must include claim text or location, cite key,
  verdict, and why the support is insufficient or inaccessible.
- Treat missing cite keys in `refs.bib` as `fabricated` citation findings unless
  the manuscript citation is clearly malformed and can be resolved to an
  existing key without guesswork.
- Keep verdict labels exactly in the approved set so downstream checks can read
  the audit consistently.

## Boundaries
- Do not modify manuscript content.
- Do not perform a full peer review or evaluate novelty, contribution strength,
  or experimental adequacy beyond citation support.
- Do not own or edit `refs.bib`; it is read-only here.
- Do not create `drafts/claim-ref-audit.md`; the canonical output requires an
  active `<paper-dir>`.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
