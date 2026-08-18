---
name: paper-presentation-builder
description: "Use when a research paper, PDF, draft, or project needs a PowerPoint/PPTX, research talk deck, thesis/group-meeting presentation, conference talk storyboard, slide script, or paper-to-slides workflow."
---

# Paper Presentation Builder

## Overview
Turn a paper or research project into a talk deck with a clear claim spine,
usable slide rhythm, controlled visual assets, and rendered QA. This skill owns
the workflow artifacts for paper-to-PPT work; the final PPTX should be built
with the available presentation-building capability when a native deck is
requested.

This is a standalone utility skill, not a downstream paper-writing pipeline
step. By default it writes relative to the user's current working directory or
an explicit output directory. It writes into an idea workspace only when the
user explicitly requests idea-integrated output.

Treat audience, duration, meeting type, slide count, and language as production
constraints. Do not leak internal requirements such as "20 minutes", "for PhD
students", "use English", or process notes into visible slide text unless the
user explicitly asks for those words to appear.

## Consume
- Source paper, PDF, Markdown, LaTeX, manuscript draft, notes, or URL supplied
  by the user.
- Optional standalone output root supplied by the user, such as an explicit
  `--output-dir` or named destination folder.
- Optional `paper/` or `<paper-dir>/` workspace when a canonical manuscript
  exists and the user wants the deck to follow that manuscript.
- Optional `drafts/story-brief.md`, `drafts/contribution-brief.md`,
  `drafts/outline.md`, `claim-evidence-map.md`, and
  `experiments/results/summary.md` when the deck should follow the current
  paper story.
- Optional `experiments/plots/index.md` and exported figure assets when result
  visuals are needed.
- Optional `experiments/conceptual-figures/index.md` and figure exports when
  framework, concept, or method visuals already exist.
- Optional `notes/project-state.md` when the user is deliberately working from
  an idea workspace and wants current project state checked.
- Optional user constraints: audience, duration, target venue, slide count,
  delivery language, speaker-notes depth, template/reference deck, and output
  format.

## Produce
- `presentations/<deck-id>/` relative to the selected output root.
- `presentations/<deck-id>/deck-brief.md`
- `presentations/<deck-id>/storyboard.md`
- `presentations/<deck-id>/style-spec.md`
- `presentations/<deck-id>/asset-manifest.md`
- Optional `presentations/<deck-id>/slide-script.md` when speaker notes or a
  timed narration are requested.
- Optional `presentations/<deck-id>/contact-sheet.png` when a rendered deck or
  image previews are produced.
- Optional `presentations/<deck-id>/qa.md` when a rendered deck is reviewed.
- Optional `presentations/<deck-id>/<deck-id>.pptx` when the final requested
  artifact is a local PowerPoint deck.

## Workflow
1. Choose the output mode and root before writing files:
   - `standalone mode` (default): write `presentations/<deck-id>/` relative to
     the user cwd or an explicit output directory. Do not require an idea
     workspace.
   - `idea-integrated mode` (optional): write under the active idea's
     `presentations/` directory only when the user explicitly asks for that
     placement.
2. Establish the deck contract in `deck-brief.md`: source files, output mode,
   output root, audience, delivery language, target duration, expected slide
   count, depth level, template/reference deck if any, must-cover claims,
   must-avoid claims, and final artifact format. Use the field shape from
   `../../_shared/templates/deck-brief-template.md`.
3. Ingest the source. For PDFs, use the configured PDF-to-Markdown workflow
   when plain text extraction is insufficient. Extract the paper's problem,
   central claim, method, datasets/evidence, core results, limitations, and
   take-home message before planning slides.
4. Separate production metadata from slide text. Keep timing, audience,
   "explain to PhD peers", and similar instructions in `deck-brief.md` or
   speaker notes; visible slide copy should read like a polished research talk,
   not like a prompt.
5. Build the claim spine before slide layouts. Write 5-8 talk claims in order:
   motivation, gap, method idea, measurement/setup, evidence, interpretation,
   boundary, and takeaway. Every planned slide should map to exactly one claim
   or one transition.
6. Choose the slide budget. As a default, use 8-10 slides for an 8 minute talk,
   14-18 slides for a 15 minute talk, and 18-22 slides for a 20 minute talk.
   Dense PhD peer talks may use more backup slides, but the main deck should
   still have a clear route.
7. Plan the asset stack in `asset-manifest.md`:
   - empirical plots and tables come from `$figure-plot-builder` or existing
     paper assets;
   - framework, method, measurement, taxonomy, or concept visuals come from
     `$conceptual-figure-builder`;
   - source screenshots, logos, paper figures, and generated illustrations must
     record provenance and intended slide placement.
   Use the field shape from
   `../../_shared/templates/asset-manifest-template.md`.
8. Write `storyboard.md` with one row per slide: slide number, working title,
   claim, proof object, visual plan, required asset, on-slide text, speaker-note
   point, source/provenance, and status. Keep slide titles claim-like; avoid
   generic labels such as "Background" when a sharper claim exists. Use the
   field shape from `../../_shared/templates/storyboard-template.md`.
9. Lock `style-spec.md` before building slides. Include aspect ratio, typeface
   preference, palette, figure treatment, section divider rhythm, title style,
   citation/footer convention, density target, and template rules. Use the
   field shape from `../../_shared/templates/style-spec-template.md`.
10. Select the build path:
   - Default Codex path: use the available Presentations capability to build
     editable PPTX slides from the storyboard and style spec, then render and
     QA previews.
   - Use a `ppt-master`-style serial workflow when the source document is large,
     template replication matters, or live preview/spec locking is more
     valuable than speed.
   - Use a `PPT-Visual-Replica`-style pass only when recreating an existing flat
     infographic or slide image as editable PPT elements.
   - Use the candidate-board workflow from `$conceptual-figure-builder` before
     deck construction when the deck depends on a new framework/concept figure.
11. Build the deck sequentially from the storyboard. Each slide needs a claim,
    a proof object, and a reason to exist. Use speaker notes for explanation
    that would overcrowd the slide.
12. Render previews and create `contact-sheet.png` when a deck is produced.
    Review thumbnail rhythm, text overflow, figure legibility, alignment,
    repeated slide patterns, asset quality, source footers, and whether any
    internal production instruction appears on slides.
13. Write `qa.md` with pass/fail notes and fixes. Do not mark the deck ready
    until visible slide text, notes language, source fidelity, and exported PPTX
    have been checked. Use the field shape from
    `../../_shared/templates/deck-qa-template.md`.

## Quality Bar
- The deck should feel like a research talk, not a paper pasted into slides.
- A PhD peer audience should get enough technical detail to judge the method
  and evidence, without undergraduate-level padding.
- Every slide should have one main claim, one primary visual/proof object, and
  enough whitespace to survive presentation mode.
- Slide text and speaker notes should follow the requested language. If the
  user asks for English presentation content, all visible text and notes should
  be in English unless quoted source text must remain unchanged.
- Internal constraints, generation prompts, timing notes, and workflow comments
  must stay out of visible slide text.
- Figures should be redrawn, simplified, or rebuilt when screenshot quality or
  text density would fail at slide scale.
- The final PPTX should be editable where practical: native text, native
  shapes, charts, and separately managed assets are preferred over full-slide
  screenshots.

## Boundaries
- Do not assume an idea workspace exists. Use idea-local `presentations/` only
  when the user explicitly requests idea-integrated mode.
- Do not invent results, baselines, dataset details, citations, or limitations
  to make the story cleaner.
- Do not create empirical charts from memory; use existing figures/data or
  route to `$figure-plot-builder`.
- Do not create framework or concept visuals that widen the paper's claim;
  route to `$conceptual-figure-builder` when visual claim boundaries need to be
  established.
- Do not treat duration or audience notes as required visible content.
- Do not deliver a final deck without rendered QA when a PPTX is requested and
  rendering is available.
- See `references/deck-qa-rubric.md` Blocking Criteria for the explicit
  kill-switch list.

## Open References Only As Needed
- Templates: when producing deck-brief/storyboard/style-spec/asset-manifest/qa,
  follow the field shape in `../../_shared/templates/deck-brief-template.md`,
  `../../_shared/templates/storyboard-template.md`,
  `../../_shared/templates/style-spec-template.md`,
  `../../_shared/templates/asset-manifest-template.md`, and
  `../../_shared/templates/deck-qa-template.md`.
- Review `references/deck-format-library.md` when choosing slide budget,
  duration variant, claim-spine shape, or density rules.
- Review `references/deck-qa-rubric.md` when scoring rendered previews,
  contact sheets, speaker notes, or final PPTX readiness.
- Review `references/build-path-selection.md` when selecting between Codex
  Presentations default, ppt-master-style serial workflow, or
  PPT-Visual-Replica-style replica adaptation.
- Review `references/asset-provenance-rules.md` when adding assets to
  `asset-manifest.md`, deciding source footers, or determining whether an
  asset must be redone.
- Review `references/speaker-script-pattern.md` when writing slide speaker
  notes, timed narration, or bilingual delivery notes.
- Review `../../_shared/artifact-contract.md` when file ownership, canonical
  paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working
  notes with English slide text or speaker notes.
- Review `../../_shared/engineering-patterns.md` when using
  `notes/project-state.md` or other workflow state to resume deck work.
