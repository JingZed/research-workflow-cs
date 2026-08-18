---
name: idea-backlog-manager
description: "Maintain a topic-level ranked backlog and the explicit promote/activate lifecycle for research ideas. Use when Codex needs to capture or rank candidate ideas, update `synthesis/idea-backlog.md`, create a registered `ideas/iNNN/idea.md`, activate a promoted idea with canonical resume state, change idea status, or preserve a legacy idea through a registered migration bridge."
---

# Idea Backlog Manager

## Overview
Keep research ideas organized, ranked, and connected to their evidence so promising directions do not disappear in notes.

## Consume
- `<topic-root>/synthesis/research-gaps.md`, linked paper-local `notes.md`, or raw idea notes.
- Optional current priorities, thesis constraints, or deadline context.
- Optional existing `<topic-root>/synthesis/idea-backlog.md`.
- Optional existing `<topic-root>/ideas/registry.yaml` when promoting an idea.

## Produce
- `<topic-root>/synthesis/idea-backlog.md`
- Optional `<topic-root>/ideas/registry.yaml` when the user explicitly promotes
  or changes the status of an idea
- Optional `<topic-root>/ideas/<id>/idea.md` when the user explicitly promotes
  one backlog item
- Optional `<topic-root>/ideas/<id>/notes/CURRENT.md` and
  `<topic-root>/ideas/<id>/notes/project-state.md` when the user explicitly
  activates a promoted idea

## Workflow
1. Resolve `<topic-root>` using the shared artifact contract. Stop for an
   explicit root if resolution fails.
2. Capture each idea with its source papers, expected value, feasibility, risk, and the smallest useful next action.
3. Merge duplicates or near-duplicates so the backlog stays navigable.
4. Re-rank ideas using the active constraints rather than keeping a static list forever.
5. Promote an idea only when the user explicitly selects it. Read
   `<topic-root>/ideas/registry.yaml` first. Use an explicit unused `iNNN` ID
   when supplied; otherwise allocate one greater than the highest registered
   numeric ID. Never reuse a retired or archived ID.
6. When the registry does not yet exist, initialize it with `active_id: null`,
   `active_entry: null`, and `ideas: []`. Do not add top-level or per-idea
   fields beyond this Skill's documented schema. Preserve unknown existing
   fields only to avoid destructive normalization; never copy them into new
   entries.
7. Create `<topic-root>/ideas/<id>/idea.md` for the selected item using
   `../../_shared/templates/idea-template.md`. Preserve the shaped central
   question/outcome, evidence basis, scope, non-goals, constraints, assumptions,
   open questions, and next decision; do not invent missing evidence. Append one
   registry entry with `id`, `title`, `slug`, `status: promoted`, and
   `canonical_dir`. Promotion reserves a stable identity; it does not make the
   idea active and does not scaffold resume, experiment, manuscript, or runtime
   directories.
8. Activate a promoted idea only when the user explicitly starts active work.
   Run `scripts/activate_idea.py` with the topic root, idea ID, concrete next
   action, and the best known phase/result/blockers. The script atomically:
   - creates the minimal `notes/CURRENT.md` and `notes/project-state.md` when
     neither exists;
   - changes the registry entry to `status: active`;
   - sets `active_id` and makes `active_entry` mirror `canonical_dir`;
   - refuses a registry whose existing `status: active` entries disagree with
     `active_id`;
   - refuses to replace another active ID or overwrite one-sided/existing state.
9. After activation, run the focused workspace validator. Repair a named
   registry, identity, or resume inconsistency that prevents the requested
   activation. Unrelated warnings do not block later bounded work and do not
   create an approval gate.
10. For an explicitly approved legacy promotion, create a stable in-topic
    canonical alias at `ideas/<id>` that resolves to the established physical
    root. Register `canonical_dir: ideas/<id>` and record `legacy_id`,
    `legacy_dir`, and `migration_status: canonical_alias`. Create `idea.md` in
    the single resolved tree; never copy resume state into a wrapper. Permit
    the alias only when its target stays inside the topic root and is verified
    to resolve to the legacy directory. Do not move an externally linked,
    active-run, or paper-facing tree merely to normalize its path. If the user
    explicitly requests a move, confirm the exact source and target, preserve a
    recoverable copy, inspect the direct file inventory, and verify the resolved
    destination before changing the registry.

## Quality Bar
- Make every idea traceable to a concrete paper, gap, or observation.
- Keep the ranking criteria visible and lightweight.
- Do not use second-person phrasing that could imply the cited papers were written by the user.
- Ensure stale ideas remain searchable instead of disappearing after reprioritization.
- Keep registry IDs, slugs, and canonical directories unique and stable.
- Keep promotion and activation distinct: promoted ideas are searchable;
  active ideas additionally have both canonical resume files.
- Keep at most one non-null `active_id` per topic. Exactly one entry has
  `status: active` when it is non-null, and that entry must match `active_id`;
  no entry may remain `active` while `active_id` is null. Stop for explicit
  direction before replacing a different active ID.

## Boundaries
- Do not write a full hypothesis unless the user selects an idea for active work.
- Do not confuse vague curiosity with an actionable idea.
- Do not overwrite an existing idea workspace, reuse an ID, or change registry
  status without explicit user intent.
- Do not create a second `CURRENT.md`, copy resume state into a bridge, or use a
  legacy migration as permission to move canonical paper or run outputs.

## Resume Continuity

After explicit activation, future work updates `notes/CURRENT.md` directly only
when a resume field materially changes and updates `notes/project-state.md`
only when scientific state changes. No state-maintenance Skill or automatic
next action is created.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../../_shared/templates/idea-backlog-template.md` when you need the specific structure, template, or integration note for this skill.
- Review `../../_shared/templates/idea-template.md` whenever promoting an item
  into its canonical `idea.md`.
