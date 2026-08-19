---
name: novelty-check
description: "Run a current, multi-source novelty investigation for a proposed research idea, method, setting, or finding. Use when the user asks for 查新, closest prior work, whether something has already been done, concurrent-work risk, or a defensible novelty delta before implementation or submission."
---

# Novelty Check

## Role

Assess global novelty risk against current literature. This is a systematic
search and evidence comparison, not proof that no prior work exists.

## Consume

- The exact proposed idea, method, setting, finding, or contribution claim.
- Optional `idea.md`, `hypothesis.md`, manuscript text, local corpus, matrices,
  bibliography, and already-known closest papers.
- Optional date window, venues, disciplines, languages, or source exclusions.

## Produce

- An in-session report by default.
- Optional `<target-dir>/novelty-check.md` when the user requests a durable
  report.

## Workflow

1. Decompose the proposal into 3–5 independently checkable novelty claims:
   problem/task, mechanism or method, data/setting, evaluation design, and
   expected finding. Separate method novelty from finding or benchmark novelty.
2. Search the local topic corpus and bibliography first to identify terminology,
   aliases, foundational work, and obvious nearest neighbors.
3. For every core claim, search current primary literature using at least three
   query families: exact technical terms, functional descriptions without the
   proposed name, and combinations of task + mechanism + setting. Include the
   most recent 6–12 months and the latest available proceedings or preprints.
4. Use multiple discovery surfaces when available, but verify retained
   candidates against primary sources such as the paper, official proceedings,
   DOI/publisher record, or repository metadata. Search snippets are leads, not
   evidence.
5. Follow backward references and forward or citing work for the closest
   candidates. Read the abstract plus the exact method, experiment, or related
   work passages needed to resolve overlap; do not rely on titles alone.
6. Compare each retained paper on task, mechanism, setting/data, evaluation,
   claimed contribution, and temporal priority. Distinguish formal publication,
   preprint, workshop paper, thesis, patent, code release, and concurrent work.
7. Classify each claim as `likely distinct`, `partial overlap`, `likely
   covered`, or `inconclusive`. Give the closest evidence and the smallest
   wording, experiment, or scope change needed to make the delta defensible.
8. Optionally, when the user explicitly requests cross-model verification, ask
   one independent reviewer to challenge the comparison. Treat that judgment as
   a secondary critique, never as literature evidence.
9. Report search date, databases/surfaces used, query families, coverage gaps,
   closest work, claim-level verdicts, overall risk, and a recommendation:
   `PROCEED`, `REFRAME`, `SEARCH MORE`, or `STOP`.

## Quality Bar

- The closest prior work is named and compared claim by claim.
- Recent and concurrent work is checked relative to the actual run date.
- “Not found” is reported as bounded search coverage, not global absence.
- A non-novel method can still have a novel finding or evaluation contribution,
  and the report says so explicitly.

## Boundaries

- Do not assert absolute novelty or legal patent clearance.
- Do not use an external model's opinion as a substitute for source evidence.
- Do not download or ingest papers into the canonical corpus unless separately
  requested.
- Do not design the full experiment program here.

## Open References Only As Needed

- Read `references/novelty-search-protocol.md` for query expansion, evidence
  fields, and the report template.
- Read `../../_shared/artifact-contract.md` when durable output ownership is
  unclear.
