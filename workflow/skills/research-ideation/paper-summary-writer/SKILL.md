---
name: paper-summary-writer
description: "Read one external paper from trustworthy Markdown and produce the one requested reading artifact. Summary mode writes the default one-page `summary.md`; structure, questions, and notes modes preserve optional deeper reading outputs without creating every sidecar or rendering every PDF page."
---

# Paper Summary Writer

## Role

Perform rapid structured reading of one paper. Default to one concise summary;
create deeper sidecars only when the user explicitly asks for that artifact or
an existing task is continuing it.

## Modes

- **summary** (default): one-page reading summary.
- **structure**: compact section-level scaffold.
- **questions**: prioritized critical reading questions.
- **notes**: short links from the paper to active topics or ideas.

## Consume

- `<topic-root>/papers/<paper-id>/paper.md` and `meta.yaml`.
- Existing `structure.md`, `summary.md`, `claim-evidence-map.md`, `notes.md`, or
  `figures/index.md` only when relevant to the selected mode.
- `source.pdf` only for a named evidence, figure, table, or conversion ambiguity
  that trustworthy Markdown cannot resolve.

## Produce

- Summary mode: `<topic-root>/papers/<paper-id>/summary.md`.
- Structure mode: `<topic-root>/papers/<paper-id>/structure.md`.
- Questions mode: `<topic-root>/papers/<paper-id>/reading-questions.md`.
- Notes mode: `<topic-root>/papers/<paper-id>/notes.md`.

Produce one mode's artifact by default. Do not fan out all four files.

## Workflow

1. Resolve the exact paper workspace and select one mode from the request. Reuse
   trustworthy `paper.md`; do not reconvert or render the PDF page by page.
2. Read the minimum relevant sections. If source ambiguity remains, inspect one
   or two target PDF pages per call and stop when that ambiguity is resolved.
3. Apply the selected mode:
   - **summary**: write citation, `Reading basis`, problem, core idea, setup,
     strongest result, limitations, and follow-up in a stable one-page order;
   - **structure**: map problem, method, setup, key results, and limitations to
     source sections or figures, using `unknown` where necessary;
   - **questions**: write a short ranked set across comprehension, validity,
     reproduction, and extension, each tied to its motivating evidence;
   - **notes**: record only concrete links to an active topic, method, dataset,
     question, or idea, distinguishing source facts from interpretation.
4. Keep claim strength proportional to `Reading basis`: `title/abstract only`,
   `partial read`, `full read`, or `unknown`.
5. Return the requested artifact and stop. Do not update the topic corpus,
   build a matrix, or create another reading artifact unless the user asks.

## Quality Bar

- Important conclusions point to explicit paper evidence.
- The result is short enough to scan during later synthesis.
- Missing information stays visible instead of being guessed.
- Default summary headings and note prose are Chinese unless English is asked.

## Boundaries

- Do not compare multiple papers or promote ideas here.
- Do not treat abstract-only evidence as a full-paper conclusion.
- Do not duplicate one paper into several theme folders.

## Open References Only As Needed

- Review `../../_shared/artifact-contract.md` for paper workspace ownership.
- Review `../../_shared/templates/paper-summary-template.md` only in summary
  mode when the exact template is useful.
