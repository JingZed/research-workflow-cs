# Research Workflow

Use the smallest sufficient procedure for the requested research task. Work
inside one named topic, idea, or standalone task at a time and follow the
nearest `AGENTS.md` when a project adds narrower rules.

## Lightweight Research Workflow

Before substantive idea work, read `notes/CURRENT.md` in full, then open the
active artifact and only the evidence relevant to the request. Search
`notes/project-state.md` by heading or keyword; read it in full only for a
whole-project scientific review, story change, or explicit state compaction.
Local artifacts, not chat history, are the resume source.

Use this flow:

```text
inspect relevant state and evidence
→ make the requested bounded change
→ run checks that directly test that change
→ update resume state only when it materially changed
→ report actual files and checks
```

Keep inspection bounded. Exclude runtime, backup, archive, run-output,
candidate-package, and vendor trees unless one is directly in scope. Do not
compute or require content hashes, checksums, digests, or tree fingerprints.
Use exact paths, versioned names, direct file comparisons, focused semantic
checks, and recoverable archives instead.

When the user asks for a review, audit, scan, or critique, keep the pass
read-only unless edits were also requested. Present findings and a proposed
fix package before changing the reviewed artifact.

## Execution Authority

Use `workflow/skills/_shared/execution-authority.md`:

- L0 read-only inspection proceeds silently.
- L1 routine reversible work and same-contract technical repair proceed
  automatically.
- L2 noncanonical experiments use a compact run card and may proceed within
  the configured spend boundary.
- L3 requires a user decision for canonical promotion, material scientific
  direction, confirmatory-contract changes, material cost, or unresolved
  licensing, privacy, security, or authority.
- L4 requires exact-target confirmation for destructive, public,
  external-send, or effectively irreversible actions.

Freeze only the affected branch at L3 or L4. Keep routine technical retries in
the same run as `attempt-N`; create a new revision only for a materially
different scientific or implementation candidate.

## Resume State Contracts

Keep `notes/CURRENT.md` as a six-field resume card. Its only top-level fields,
in order, are:

```text
phase
active_artifact
current_result
open_blockers
next_action
last_updated
```

Keep it within 15 non-empty lines and 2 KiB. `active_artifact` must resolve to
one existing regular file no larger than 64 KiB.

Keep `notes/project-state.md` as a bounded scientific snapshot within 120
lines and 8 KiB. It may summarize the current question, strongest evidence,
bounded interpretation, delivery state, scientific risks, and next scientific
decision. It must not store routing, Skill names, gate status, session
manifests, handoff ledgers, command logs, or transient run telemetry.

After changing either resume file, run:

```bash
python -B workflow/scripts/validate_research_workflow.py --idea <idea-root>
```

## Literature Architecture

Resolve `<topic-root>` as the nearest ancestor containing both `synthesis/`
and `ideas/`. Treat `synthesis/literature-corpus.jsonl` as the source of truth;
matrices, maps, gaps, and idea-local views are derived. Keep one flat external
paper workspace at `papers/<paper-id>/` and represent overlap through tags
instead of duplicate theme folders.

Default to rapid structured reading. Escalate to page-by-page PDF review only
for high relevance, key evidence, material conflict, conversion ambiguity, or
an explicit request. Prefer trustworthy Markdown over rendering a PDF.

## Skill Architecture Quality

- A Skill must own a distinct reusable capability with a recognizable direct
  trigger and a primary artifact or tool integration.
- Extend an existing Skill with a named mode before adding another Skill.
- Do not create Skill-to-Skill router trees, generic plan/state trees, phase
  entry Skills, standalone gate Skills, or a second scientific-state hierarchy.
- The catalog has no fixed Skill-count cap. Preserve useful capabilities;
  merge only when an existing Skill exposes the full behavior as a clear mode,
  and retire a name only after its behavior remains directly discoverable.
- Preview and apply behavior for one operation stay inside the same Skill.
- Explicit-only trigger wording must be paired with
  `allow_implicit_invocation: false`, and that policy must not appear without
  matching trigger wording.

Legacy requests for `idea-discovery` map to `idea-creator` `discovery` mode.
Legacy `paper-writing` status requests map to `paper-finish-loop` `status`
mode. These are compatibility interpretations, not router Skills.

### Available skills

<!-- BEGIN AUTO-GENERATED SKILLS -->
#### Research Ideation
- paper-discovery-fetcher: Fetch and refresh literature candidates (file: workflow/skills/research-ideation/paper-discovery-fetcher/SKILL.md)
- paper-pdf-fetcher: Download one selected paper PDF (file: workflow/skills/research-ideation/paper-pdf-fetcher/SKILL.md)
- paper-inbox-triage: Prioritize new papers and reading queue (file: workflow/skills/research-ideation/paper-inbox-triage/SKILL.md)
- paper-metadata-normalizer: Normalize paper metadata into meta.yaml (file: workflow/skills/research-ideation/paper-metadata-normalizer/SKILL.md)
- paper-to-markdown: Convert source PDF into clean paper.md with MinerU (file: workflow/skills/research-ideation/paper-to-markdown/SKILL.md)
- figure-table-extractor: Extract figure assets and caption index (file: workflow/skills/research-ideation/figure-table-extractor/SKILL.md)
- citation-library-maintainer: Merge and normalize refs.bib entries (file: workflow/skills/research-ideation/citation-library-maintainer/SKILL.md)
- paper-summary-writer: Create one requested single-paper reading artifact (file: workflow/skills/research-ideation/paper-summary-writer/SKILL.md)
- literature-corpus-maintainer: Literature Corpus Maintainer (file: workflow/skills/research-ideation/literature-corpus-maintainer/SKILL.md)
- claim-evidence-mapper: Audit an external paper's claim support (file: workflow/skills/research-ideation/claim-evidence-mapper/SKILL.md)
- literature-matrix-builder: Build one matrix, topic map, or gap view (file: workflow/skills/research-ideation/literature-matrix-builder/SKILL.md)
- idea-backlog-manager: Rank, promote, and activate research ideas (file: workflow/skills/research-ideation/idea-backlog-manager/SKILL.md)
- research-team-mapper: Map active research teams from papers and public sources (file: workflow/skills/research-ideation/research-team-mapper/SKILL.md)
- idea-creator: Generate, test, and rank research ideas (file: workflow/skills/research-ideation/idea-creator/SKILL.md)
- novelty-check: Check global novelty against recent literature (file: workflow/skills/research-ideation/novelty-check/SKILL.md)
- novelty-sanity-check: Screen an idea against the local corpus (file: workflow/skills/research-ideation/novelty-sanity-check/SKILL.md)
- research-lit: Search local, library, note, and web sources (file: workflow/skills/research-ideation/research-lit/SKILL.md)
#### Experiment Execution
- hypothesis-framer: Turn an idea into a testable hypothesis (file: workflow/skills/experiment-execution/hypothesis-framer/SKILL.md)
- reproduction-planner: Plan reproduction of a target paper (file: workflow/skills/experiment-execution/reproduction-planner/SKILL.md)
- baseline-checklist-builder: List required baselines and controls (file: workflow/skills/experiment-execution/baseline-checklist-builder/SKILL.md)
- experiment-spec-writer: Write compact or confirmatory experiment plans (file: workflow/skills/experiment-execution/experiment-spec-writer/SKILL.md)
- runbook-generator: Create compact or full experiment runbooks (file: workflow/skills/experiment-execution/runbook-generator/SKILL.md)
- run-experiment: Run experiments with proportional run-local state (file: workflow/skills/experiment-execution/run-experiment/SKILL.md)
- result-aggregator: Aggregate raw runs into result summary (file: workflow/skills/experiment-execution/result-aggregator/SKILL.md)
- figure-plot-builder: Build paper-ready plots and captions (file: workflow/skills/experiment-execution/figure-plot-builder/SKILL.md)
- failure-analysis-writer: Analyze material scientific experiment failures (file: workflow/skills/experiment-execution/failure-analysis-writer/SKILL.md)
- experiment-watchdog: Report only material experiment state changes (file: workflow/skills/experiment-execution/experiment-watchdog/SKILL.md)
- promote-run-outputs: Preview or apply an exact run-output replacement (file: workflow/skills/experiment-execution/promote-run-outputs/SKILL.md)
- results-sufficiency-review: Judge whether evidence is ready for writing (file: workflow/skills/experiment-execution/results-sufficiency-review/SKILL.md)
#### Paper Writing
- paper-story-framer: Frame an evidence-backed story or contribution (file: workflow/skills/paper-writing/paper-story-framer/SKILL.md)
- targeted-critic: Bounded artifact, evidence, or paper critique (file: workflow/skills/paper-writing/targeted-critic/SKILL.md)
- paper-style-auditor: Audit manuscript style, framing, and readability (file: workflow/skills/paper-writing/paper-style-auditor/SKILL.md)
- paper-outline-builder: Build drafting-ready, evidence-linked paper outlines (file: workflow/skills/paper-writing/paper-outline-builder/SKILL.md)
- intro-problem-framer: Draft the introduction problem framing (file: workflow/skills/paper-writing/intro-problem-framer/SKILL.md)
- related-work-weaver: Weave matrix into related work prose (file: workflow/skills/paper-writing/related-work-weaver/SKILL.md)
- po-related-work-backend: Build optional PaperOrchestra related-work scaffolds (file: workflow/skills/paper-writing/po-related-work-backend/SKILL.md)
- method-results-drafter: Draft methods, results, and discussion (file: workflow/skills/paper-writing/method-results-drafter/SKILL.md)
- paper-finish-loop: Inspect, build, finish, or check one paper (file: workflow/skills/paper-writing/paper-finish-loop/SKILL.md)
- abstract-title-polisher: Polish abstract, title, and pitch (file: workflow/skills/paper-writing/abstract-title-polisher/SKILL.md)
- claim-reference-auditor: Audit whether claims match cited evidence (file: workflow/skills/paper-writing/claim-reference-auditor/SKILL.md)
- promote-paper-version: Preview or apply a recoverable paper replacement (file: workflow/skills/paper-writing/promote-paper-version/SKILL.md)
- reviewer-response-writer: Draft point-by-point reviewer responses (file: workflow/skills/paper-writing/reviewer-response-writer/SKILL.md)
- conceptual-figure-builder: Specify, explore, build, or critique one paper figure (file: workflow/skills/paper-writing/conceptual-figure-builder/SKILL.md)
- research-review: Run an explicit multi-round external review (file: workflow/skills/paper-writing/research-review/SKILL.md)
#### Standalone Utility Skills
- paper-presentation-builder: Paper Presentation Builder (file: workflow/skills/standalone/paper-presentation-builder/SKILL.md)
<!-- END AUTO-GENERATED SKILLS -->

### How to use skills

- Use the most relevant single Skill by default.
- Combine Skills only when the request needs both results and the first
  artifact is the direct input to the second action.
- Open shared references only when the selected Skill points to them.
- Create only the selected Skill mode's canonical artifact plus a necessary
  blocker note; do not fan out optional companion documents.
- If multiple interpretations would change artifact ownership, experiment
  launch behavior, or canonical manuscript state, state the assumption or ask
  instead of silently choosing.

## Standalone Outputs

Use `presentations/<deck-id>/` for standalone decks and
`deliverables/<task-id>/` for final user-facing packages. Keep build, staging,
probe, and verification scratch data outside `deliverables/`.
