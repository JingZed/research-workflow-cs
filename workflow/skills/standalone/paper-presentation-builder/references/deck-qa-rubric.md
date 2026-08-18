# Deck QA Rubric

Score each item 0, 1, or 2. A deck is ready only when all blocking items score
2 and no visible slide has unresolved overflow.

| item | pass criteria for 2 | score 1 | score 0 |
| --- | --- | --- | --- |
| Claim spine | Slides form a coherent argument from problem to takeaway. | Mostly coherent with one weak transition. | Slides read as paper sections without an argument. |
| One claim per slide | Each slide has one main claim and one proof object. | One or two slides carry two claims. | Multiple slides are unfocused or purely decorative. |
| Slide budget | Main slide count fits duration and audience. | Slightly over budget with clear removable slides. | Deck cannot fit the requested duration. |
| Thumbnail rhythm | Contact sheet alternates setup, evidence, and synthesis cleanly. | Some repetitive layouts but readable. | Visual rhythm is monotonous or chaotic. |
| Text overflow | No clipping, overlap, or unreadable small text. | Minor line wrap issue on one slide. | Any slide has clipped or overlapping visible text. |
| Figure legibility | Figures remain readable in presentation mode. | One figure needs cropping or callouts. | Critical figure text or marks cannot be read. |
| Alignment | Titles, margins, footers, and primary visuals align consistently. | Small inconsistencies remain. | Layout looks assembled ad hoc. |
| Asset quality | Assets are sharp, undistorted, and source-appropriate. | One asset is acceptable but should be redrawn later. | Screenshot or generated asset quality blocks delivery. |
| Source fidelity | Claims, numbers, and examples match source files. | One citation/provenance detail needs checking. | Deck invents or distorts source evidence. |
| Source footers | Footers or notes cite reused assets where needed. | Some noncritical source markers missing. | Reused figures or screenshots have no provenance. |
| Speaker notes | Notes support delivery without duplicating slide text. | Notes are sparse or too verbose in places. | Notes contradict slides or include prompt/process text. |
| Language consistency | Visible text and notes follow requested language rules. | Minor untranslated phrase remains. | Mixed language violates the deck contract. |
| Internal leakage | No prompt, workflow, timing, or audience instruction appears visibly. | One notes-only production comment remains. | Any visible slide leaks internal instructions. |

## Blocking Failures

- Score 0 in text overflow, source fidelity, internal leakage, or figure
  legibility blocks readiness.
- A requested PPTX cannot be marked ready without either rendered QA or an
  explicit note that rendering was unavailable.

## Mini Case

Mock slide: a 15-minute conference deck uses one result slide with a claim
title, a cropped paper figure on the left, and two short interpretation bullets
on the right. A small footer cites the manuscript figure. Speaker notes explain
the takeaway and transition, while visible text avoids duration, audience, and
prompt instructions.

Pass angle:

- `figure_legibility` can pass if the crop preserves axis labels, the key trend
  is readable in presentation mode, and the speaker note explains details that
  would overcrowd the slide.

Needs-update angle:

- `internal_leakage` fails if the slide title or bullet text includes metadata
  such as "15-minute talk", "for PhD students", "use English", or "explain the
  result simply".

## Blocking Criteria

- Visible slide text must not contain audience descriptions, duration notes,
  prompt instructions, internal workflow comments, or production metadata such
  as "for PhD students", "20 minutes", "use English", or "explain X to Y".
- Do not mark a deck `ready` if any slide is a full-slide raster screenshot of
  a non-replica source; rebuild as native PPT elements or hybrid-asset layout,
  except when the explicit task is a replica-adaptation pass.
- Do not mark a deck `ready` without a rendered preview QA pass recorded in
  `qa.md`.
- Do not mark a deck `ready` if `source_fidelity` scores 0 (any cited number,
  figure, dataset, or quote diverges from the manuscript or source); rebuild
  the affected slide to match the source or remove the unsupported claim.
