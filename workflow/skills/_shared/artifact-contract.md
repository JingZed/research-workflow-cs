# Artifact Contract

Use the nearest project rules first. Within those rules, each Skill owns the
paths listed in its `## Produce` section. Create the smallest set of artifacts
needed for the requested decision or handoff.

## General Rules

- Read an existing artifact before updating or replacing it.
- Prefer updating the established file over creating a parallel summary.
- Treat `## Consume` as possible inputs, not a checklist of files to create.
- Keep manuscript prose in `drafts/` or the named paper workspace.
- Keep experiment plans, runs, results, and plots under `experiments/`.
- Keep short resume state under `notes/`.
- Put imported repositories, raw family outputs, scratch work, and recoverable
  archives under the project-local workspace or archive directory.
- Never infer that a versioned candidate may replace a canonical artifact.
  Canonical boundaries come from the nearest project rules.

## Resume State

`notes/CURRENT.md` is the first resume file. Keep it readable in one glance,
at most 15 non-empty lines and 2 KB. Use exactly these six top-level fields in
this order:

```text
phase:
active_artifact:
current_result:
open_blockers:
next_action:
last_updated:
```

Update it only when one of those fields materially changes.

`notes/project-state.md` is the detailed scientific resume file. Update it when
the hypothesis, evidence, interpretation, paper story, major milestone,
blocker, or next scientific decision changes. Routine formatting, prose, and
implementation edits do not require a state entry.

Keep `notes/project-state.md` within 120 lines and 8 KB. Treat it as a current
scientific snapshot, not an append-only history or workflow controller. It may
summarize the current question, strongest evidence, bounded interpretation,
paper or delivery state, material scientific risks, and next scientific
decision. Do not store routing, Skill names, gate or approval status, session
manifests, manager/worker state, handoff ledgers, command or check logs, file
trees, or transient run telemetry. A dated Decision Log is only for a
user-confirmed scientific pivot, freeze, or abandonment.

Do not create phase-local routing files such as `ideation-entry.md`,
`experiments/execution-entry.md`, `drafts/writing-entry.md`, or
`notes/research-pipeline.md`. A durable decision belongs in the artifact that
owns the scientific or implementation state, not in a parallel routing layer.
A plain `TODO.md` or `notes/TODO.md` may hold a short backlog, but no Skill owns
it and it must not become a schema, handoff ledger, or status history.

## Literature

Before any literature write, resolve `<topic-root>` by walking upward from the
active project or idea to the nearest ancestor containing both `synthesis/` and
`ideas/`. If no such ancestor exists, require an explicit topic root. Never
default literature output to the current idea directory.

A topic root may cover a broad field with multiple overlapping subtopics. Keep
one topic-wide corpus and represent subtopics with stable `relevant_to` tags and
derived synthesis views. Reserve `iNNN` tags for promoted idea IDs; use stable
lowercase slugs such as `world-model` or `evaluation` for shared themes. Do not
encode subtopics as nested paper directories.

- `<topic-root>/synthesis/literature-corpus.jsonl` is the topic-wide source of
  truth for known papers.
- `<topic-root>/synthesis/literature-matrix.md` is the shared human-readable
  view, organized into useful topic clusters while keeping one row per paper.
- `<topic-root>/synthesis/topic-map.md` is the topic-wide map of branches,
  bridge papers, and sparse areas.
- `<topic-root>/synthesis/research-gaps.md` is the topic-wide shortlist of
  evidence-backed candidate gaps.
- `<topic-root>/synthesis/idea-candidates.md` is a generated, ranked candidate
  report; `idea-backlog.md` remains the canonical managed pool.
- `<topic-root>/synthesis/idea-backlog.md` is the ranked topic-wide pool of
  candidate ideas.
- `<topic-root>/synthesis/topic-profile.yaml`,
  `<topic-root>/synthesis/paper-leads.jsonl`, and
  `<topic-root>/synthesis/reading-queue.md` are the canonical discovery and
  intake artifacts.
- `<topic-root>/synthesis/team-corpus.jsonl` is the topic-wide source of truth
  for evidence-backed public research-team records. Optional
  `<topic-root>/synthesis/team-radar.md` is its derived human-readable view.
- Optional discovery audit output belongs at
  `<topic-root>/synthesis/search-report.md`.
- Optional cross-source library synthesis belongs at
  `<topic-root>/synthesis/library-search.md`.
- `<topic-root>/ideas/<id>/literature-matrix.md` is an optional derived view
  for one idea.
- `<topic-root>/ideas/registry.yaml` indexes promoted ideas. Each normal
  promotion owns `<topic-root>/ideas/<id>/idea.md` and any later project-local
  artifacts. A grandfathered project may temporarily use that stable path as
  an in-topic symlink to its legacy physical root only when the registry entry
  records `legacy_id`, `legacy_dir`, and
  `migration_status: canonical_alias`. The alias must resolve inside the topic
  root and does not authorize a physical move.
- Every single-paper artifact belongs under
  `<topic-root>/papers/<paper-id>/`. This includes `source.pdf`, `meta.yaml`,
  `paper.md`, `structure.md`, `summary.md`, `figures/`,
  `claim-evidence-map.md`, `reading-questions.md`, `notes.md`, acquisition
  reports, and conversion output.
- `claim-evidence-map.md` in a paper workspace maps claims made by that external
  source paper. Do not use that unqualified filename for project or manuscript
  claims.
- Idea directories may own derived literature analysis, but not duplicate
  discovery pools, queues, PDFs, or single-paper workspaces.
- Never create `<topic-root>/papers/<subtopic>/` or duplicate one paper into
  multiple folders. Use corpus tags and derived views for overlapping scope.

Check the shared literature and team corpora before rediscovering the same
papers, people, or teams.

## Active Idea and Experiments

Use an explicit lifecycle:

```text
backlog -> promoted -> active -> paused/finishing -> retired
```

- Promotion creates a stable registry entry and `idea.md`; it does not create
  resume or execution state.
- Activation requires explicit user intent. It creates both
  `notes/CURRENT.md` and `notes/project-state.md`, changes the entry to
  `status: active`, sets `active_id`, and makes `active_entry` mirror the
  entry's `canonical_dir`.
- Keep at most one non-null `active_id` per topic. Exactly one registry entry
  has `status: active` when it is non-null, and it must be that ID; when
  `active_id` is null, no entry may have `status: active`. Switching it requires
  explicit user direction and a state update for both the outgoing and incoming
  idea.
- Never allow only one of the two canonical resume files to exist for an active
  idea. Do not copy them into aliases or migration bridges.
- Do not create experiment, draft, or paper artifacts for a merely promoted
  idea. Validate registry, identity, and resume state before active work.

Common idea artifacts are:

- `idea.md`
- `hypothesis.md`
- `experiments/plans/experiment-plan.md`
- `experiments/runbooks/runbook.md`
- `experiments/results/summary.md`
- `experiments/plots/`

Long-running work belongs under `experiments/runs/<run-id>/`. Preserve enough
operational state to resume without chat history:

- exact command, working directory, environment or config;
- start time and process, job, or scheduler identifier;
- status and last checked time;
- stdout and stderr paths;
- checkpoint and expected output paths;
- recovery or resume command.

Keep rerun outputs staged. Only when the user explicitly asks to replace named
paper-facing canonical outputs, prepare a read-only plan containing exact
normalized relative paths, source and destination locations, byte sizes,
modification times, and direct content-comparison results. Use the `preview`
mode of `promote-run-outputs`; use its `apply` mode only after the user confirms
the displayed source, target, and file list in the current task. Archive
overwritten bytes, compare copied files directly, and record rollback
instructions. Research workflows never compute or record hashes, checksums,
digests, or tree fingerprints.

## Paper Writing

Create only the paper artifacts needed by the current bottleneck. Common
artifacts include:

- `drafts/story-brief.md`
- `drafts/contribution-brief.md`
- `drafts/outline.md`
- `drafts/intro.md`
- `drafts/related-work.md`
- `drafts/method-results.md`
- `drafts/abstract.md`
- `drafts/title-options.md`
- `drafts/style-profile.md`
- `drafts/figures/<figure-id>.spec.md`

Before any paper-local write, resolve the candidate without changing the
filesystem: read the nearest project rules, then `notes/CURRENT.md`, then
reconcile any explicit user target. Project protection rules are authoritative;
an explicit target must be permitted and must not conflict with the active
candidate. Stop on disagreement. Do not select a paper directory by scanning
version names or create a stub merely to host an output.

Each active paper candidate keeps its own:

- `<paper-dir>/INVARIANTS.md`
- manuscript source, bibliography, and figures;
- `<paper-dir>/finish-report.md`
- optional `<paper-dir>/review-log.md` when the user requests a durable review;
- optional `<paper-dir>/style-audit.md`
- `<paper-dir>/submission-checklist.md` near submission.

`INVARIANTS.md` records the relationship-level claim boundaries that must stay
true across sections. It is part of the named paper candidate and does not grant
permission to edit a protected canonical paper.

Reviews, audits, and critiques are read-only unless the user also requests
edits. Store durable review output only in the file owned by the review Skill.

Replacing a canonical paper is explicit-only and requires:

1. a user request naming the candidate and canonical target;
2. a current build and focused scientific/package check of the candidate;
3. an exact source-to-target plan and explicit current-task confirmation;
4. an archive of the previous canonical package;
5. source-only copy, clean rebuild, inspected diff, and direct file comparison;
6. a replacement manifest with rollback instructions.

### Promotion Identity Without Hashes

Use the same exact-path contract for paper and experiment promotion plans:

- express every path as a normalized root-relative POSIX path and sort paths
  lexicographically;
- record each regular file as `path`, `type: file`, byte `size`, and
  modification time;
- record an allowed symlink as `path`, `type: symlink`, and its literal target;
  reject symlinks whose resolved target escapes the declared root;
- represent every copy as an exact source-to-destination pair; never use a glob
  or an inferred directory sync;
- show the complete copy plan to the user in the current task and record their
  approval note;
- immediately before mutation, recheck paths, size, modification time, and
  direct content comparisons; after copying, compare source and destination
  bytes directly.

Any path, inventory, metadata, or direct-comparison change invalidates the plan
before mutation and requires fresh current-task confirmation.

## Standalone Deliverables

Unless the user asks to integrate them into an idea, use:

```text
<research-root>/presentations/<deck-id>/
<research-root>/deliverables/<task-id>/
```

Standalone deliverables do not change an idea’s scientific state by default.

## Language Defaults

- Working notes and reading artifacts default to Chinese.
- Manuscript-facing drafts, paper packages, submission checks, and rebuttals
  default to English.
- Preserve source language when converting a paper.
- Follow an explicit user language request over these defaults.

## Ownership and Safety

- A Skill may write only its declared outputs and explicitly requested companion
  state files.
- A reviewer does not silently become an editor.
- A run does not silently promote its outputs.
- A paper candidate does not silently replace a canonical paper.
- Archive before overwrite; inspect the actual diff and compare copied files
  directly; keep rollback instructions with every high-risk promotion.
