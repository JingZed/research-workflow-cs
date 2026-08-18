---
name: paper-outline-builder
description: "Build an evidence-linked manuscript outline and storyline from the current active idea evidence. Use when Codex needs to create `drafts/outline.md`, choose the paper's narrative spine, map claims to evidence, assign section and paragraph roles, plan key sentence functions, designate the hero figure, or budget the paper before drafting."
---

# Paper Outline Builder

## Overview
Choose a paper story that the current evidence can actually support before drafting paragraphs.

Use the outline to separate macro framing from micro technical positioning so
the downstream introduction and related-work drafts do not collapse into the
same argument twice.

## Consume
- `hypothesis.md`, `experiments/results/summary.md`, and relevant gap notes.
- The nearest project rules and `notes/CURRENT.md` for active-candidate and
  protected-directory boundaries.
- Optional `drafts/story-brief.md` when the paper's narrative angle has already
  been selected by `$paper-story-framer`.
- Optional `drafts/contribution-brief.md` when the paper's contribution ladder
  has already been sharpened by `$paper-story-framer`.
- Optional `experiments/plots/index.md`,
  `experiments/conceptual-figures/index.md`, or target venue constraints.
- Optional current thesis chapter or paper positioning context.

## Produce
- `drafts/outline.md`
- Optional `<paper-dir>/INVARIANTS.md` only when an existing writable paper
  candidate is resolved unambiguously and either the user requested an
  invariant update or the approved paper-global claim structure materially
  changed. This is a paper-global constraint registry, not a draft section.

## Resolve The Paper Directory

Resolve `<paper-dir>` without changing the filesystem:

1. Read the nearest project rules first. Record any explicitly active, writable,
   protected, read-only, or prohibited paper directories.
2. Read `notes/CURRENT.md` next. Prefer `active_paper_dir`; otherwise derive the
   candidate directory from `candidate` or `active_artifact` when either names a
   file inside a paper workspace.
3. Normalize any paper directory explicitly named by the user.
4. Reconcile the three sources:
   - project rules are authoritative for protection and allowed write scope;
   - a current-state candidate is the default active candidate;
   - an explicit user target is usable only when project rules permit it and it
     does not conflict with the current active candidate;
   - any disagreement among applicable sources requires confirmation before
     writing paper-local files.
5. Require the resolved candidate directory to exist and be a directory. If no
   candidate resolves, continue with `drafts/outline.md` only and report that
   paper-local invariant output is unresolved.

Do not scan for `paper/` or `paper_vN/`, choose a highest version, create a
directory, or create a stub as part of target selection.

## Choose Outline Depth

Use the narrowest depth that leaves the next writer able to proceed:

- **Structural:** use when the story is still being selected or the user asks
  for a compact, high-level plan. Include the spine, claim-evidence matrix,
  section contracts, hero visual, and page budget.
- **Drafting-ready:** prefer for a full-paper outline with stable evidence, or
  when the user asks what each section, paragraph, or sentence should do. Add a
  paragraph-function contract for every planned section. Add ordered
  sentence-function maps for the abstract, Introduction, contribution
  paragraph, Discussion synthesis, Conclusion, and any claim-sensitive passage.

If the user explicitly asks for the logic of every sentence, extend the
sentence-function map to every planned paragraph. In technical sections, use
sentence-or-move slots when fixing an exact sentence count would be artificial.
The slots specify argumentative obligations; the final prose may merge or split
them for clarity and rhythm.

## Workflow
1. Resolve the paper directory using the read-only procedure above before
   considering any paper-local output.
2. Choose the paper's main claim, fallback weaker claim, and supporting storyline based on the strongest current evidence. If `drafts/story-brief.md` exists, treat it as the proposed narrative lens to validate against evidence rather than as an unchangeable mandate. If `drafts/contribution-brief.md` exists, treat its contribution ladder as the proposed paper-facing claim structure to validate, order, and budget. If the contribution ladder contains more rungs than the page budget or section structure can support, flag the tension and name which rungs should be merged, deferred to appendix/supporting discussion, or routed back to `$paper-story-framer` before proceeding.
3. Build a compact claim-evidence matrix inside the outline so every major claim points to specific runs, tables, or figures.
4. Write one spine sentence for the full paper and make every top-level section serve, qualify, or defend that sentence.
5. Explicitly separate section scopes early: Introduction should cover macro problem context, stakes, and gap; Related Work should cover micro technical clusters, nearest-neighbor comparisons, and why the paper's positioning is different.
6. Build the section plan in writer-facing form as section function contracts:
   for each top-level section, state what it must accomplish, its argument role
   in the full-paper spine, how it should be written, what each subsection
   contributes, which evidence owns it, which takeaway it must land, which
   interpretation boundary must stay explicit, which citation or source
   obligation it carries, and which report-like shape it must avoid. These are
   role contracts, not reusable prose templates; adapt them to the paper type,
   venue, and evidence rather than forcing a generic IMRaD or conference-paper
   skeleton.
7. At drafting-ready depth, give every planned paragraph one primary
   argumentative job, an ordered set of content moves, its evidence or source
   owner, the conclusion it must land, and the transition it creates. Add
   sentence-function maps at the depth selected above. Derive these maps from
   this paper's evidence rather than importing a generic abstract,
   Introduction, or IMRaD template.
8. For sections that rely on prior work positioning, identify the live methodology clusters, the limitation hypothesis for each cluster, and the bridge sentence showing how the current paper differs.
9. Make section-level citation obligations explicit enough that downstream drafting names the key baselines, datasets, metrics, and foundational methods/models instead of hand-waving them later; treat these obligations as exhaustive coverage for whatever the outline itself mentions.
10. If a section needs subsections, make the hierarchy complete rather than incomplete: do not create X.1 without deciding whether X.2 exists or whether the section should remain undivided.
11. Designate one hero figure, conceptual figure, or table that carries the
    paper's central message, then assign the remaining figures to supporting
    roles. If the needed hero figure is conceptual and does not exist yet, route
    to `$conceptual-figure-builder` rather than asking `$figure-plot-builder` to
    create a schematic.
12. Budget the section structure explicitly: expected section count, rough page weight, and which evidence each section must carry.
13. Give Results and Discussion explicit contracts. Results should not default
    to experiment execution order unless that order serves the argument.
    Discussion should specify the broader meaning, the assumption the paper
    weakens or revises, and the uncertainty that remains but is now better
    located.
14. When the optional invariant-output condition is satisfied, write
    `<paper-dir>/INVARIANTS.md` only to the existing candidate resolved above.
    Use the main claim, fallback claim, evidence owners, section interpretation
    boundaries, and known drift risks to define a small set of paper-global
    invariants plus directive forbidden practices. If `INVARIANTS.md` already
    exists, check whether the main claim changed enough to justify updating it.
    If updating, record the reason explicitly; do not silently regenerate it.
    For each forbidden practice that could be phrased as `not X`, also record
    the paper-facing positive counterpart so downstream drafting does not copy
    the internal constraint language into the manuscript.
15. Keep speculative or weakly supported claims out of the core outline, or demote them to limitations or future work.

## Quality Bar
- Make the outline evidence-first rather than hype-first.
- Ensure every top-level claim has a visible evidence owner and no orphan claim survives in the main arc.
- Ensure every paper-facing claim has an explicit scope boundary: tested
  setting, evidence owner, and the nearest comparison it is allowed to support.
- Do not stop at headings: the outline must explain what each section is for, not just what it is called.
- Keep macro framing and micro technical positioning distinct enough that Introduction and Related Work are not forced to repeat the same logic.
- Every planned top-level section should have a section function contract that
  names its role in the paper, evidence/source owner, required takeaway,
  citation obligation when applicable, interpretation boundary, and failure
  mode to avoid. Do not import fixed section templates from external template
  libraries; use them only as reminders that sections need explicit jobs.
- The outline block for the Introduction should explicitly plan a compact
  prior-work motivation bridge: the most relevant prior-work clusters that
  motivate the paper's question, plus the named gap the current paper tests. A
  full conference paper often needs two to four clusters; shorter or tightly
  scoped papers may need fewer. Do not rely on `$intro-problem-framer` to invent
  this bridge without outline-level guidance.
- Use the section archetypes and results-arc pattern when they fit, rather than inventing a flat section list by default.
- Make subsection roles explicit enough that downstream drafting can proceed without re-planning the section.
- At drafting-ready depth, make the paragraph order complete enough that a
  downstream writer does not need to invent the argument sequence.
- Give each paragraph one primary job. Make its ordered sentence or move
  functions serve that job rather than forming a disconnected checklist.
- Make sentence-function maps paper-specific and evidence-linked. A fixed
  seven-sentence abstract or generic Introduction sequence is not a quality
  substitute for reasoning from the manuscript's actual claim and evidence.
- Make each section specific enough that a downstream skill knows how to draft it and what overclaim to avoid.
- Record the main overclaim or drift risk for any section that is easy to miswrite.
- Keep section-level claims paper-local by tying them to setting, evidence owner, and nearest comparison point.
- Prefer condition-specific results, failure modes, and evidence-linked scope boundaries over generic limitation boilerplate.
- Treat missing methodology clusters, missing limitation hypotheses, or missing bridge sentences in prior-work-dependent sections as outline quality failures, not as details to improvise later.
- Treat missing citation obligations for baselines, datasets, metrics, or foundational methods/models named in the outline as an outline quality failure, not as an acceptable drafting shortcut.
- Treat orphan subsection hierarchies as an outline quality failure, not as a harmless formatting detail.
- Choose the hero figure early enough that weak stories fail before full drafting.
- If the hero figure is conceptual rather than empirical, name the exact
  framework or schematic role it must play.
- Keep section objectives explicit enough that drafting can proceed without re-planning.
- Every section should state how it serves, qualifies, or defends the
  full-paper spine sentence.
- Treat missing forbidden report shapes as outline quality failures; downstream
  writers should know what kind of flat report not to write.
- Treat a missing Discussion meaning contract as an outline quality failure.
- Use figure placement and rough page budget to test narrative flow early.
- Keep `INVARIANTS.md` small and relationship-level. It should freeze the
  paper's contribution constraints, not record every past mistake.
- In section contracts, name interpretation boundaries as
  positive roles when possible: `serves as a boundary stress test`, `is scoped
  to the tested setting`, `is interpreted as condition-dependent`, or `is a
  label-proximal upper bound`. Avoid making `what not to claim` the sentence a
  downstream writer is likely to paste into paper-facing prose.

## Boundaries
- Do not draft full paragraphs here.
- Do not turn sentence-function maps into reusable prose templates or force an
  exact final sentence count when the argument reads more clearly after
  merging or splitting a slot.
- Do not solve venue formatting details yet.
- Do not keep unsupported side stories in the main arc.
- Do not create, select by version heuristic, or materialize a paper directory.
- Do not write to a protected or conflicting paper target.
- Outline-ready prose must follow
  `../../_shared/writing-constraint-layer.md`. When a scope boundary belongs in
  the outline, state the tested condition and positive evidential role rather
  than drafting defensive boilerplate for later sections to copy.
- Do not defer missing macro/micro scope split, cluster design, bridge logic, or citation obligations to downstream drafting if the outline already names the relevant section content.

## Open References Only As Needed
- Use `scripts/resolve_paper_dir.py` to reconcile nearest project rules,
  `notes/CURRENT.md`, and an optional explicit target without writing files.
- Review `../../_shared/writing-constraint-layer.md` before generating or
  updating `INVARIANTS.md`.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `references/paper-plan-pattern.md` when you want a reusable structure for claim-evidence mapping, hero figure choice, and section/page budgeting inside `drafts/outline.md`.
- Review `references/writer-facing-outline-pattern.md` for drafting-ready
  paragraph contracts, key sentence-function maps, section intent, subsection
  roles, and interpretation boundaries.
