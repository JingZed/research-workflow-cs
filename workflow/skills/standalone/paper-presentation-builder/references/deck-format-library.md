# Deck Format Library

Use this library to set the slide budget and talk rhythm before writing the
storyboard.

| variant | slide_budget | claim_spine_shape | density_rules | typical_pitfalls |
| --- | --- | --- | --- | --- |
| 8-min lightning | 7-10 main slides, 0-3 backup slides. | Problem -> gap -> key idea -> one decisive evidence slide -> takeaway. | One primary visual per slide, minimal method detail, no long related-work detour. | Trying to summarize the whole paper, too many setup slides, unreadable result tables. |
| 15-min conference | 14-18 main slides, 3-8 backup slides. | Motivation -> problem -> method/framework -> setup -> 2-3 evidence slides -> limitation/boundary -> takeaway. | Technical peer density is acceptable, but each slide still needs one claim and one proof object. | Method overwhelms evidence, slide titles become section labels, limitations are hidden. |
| 20-min long talk | 18-22 main slides, 8-15 backup slides. | Motivation -> field gap -> framework -> method details -> setup -> result sequence -> interpretation -> boundary -> future work. | Can include method builds and ablations, but split dense explanations across beats. | Bloated background, repeated result slides without interpretation, no clear midpoint reset. |
| poster talk | 5-8 spoken stops over poster or compact deck. | Hook -> map of poster -> method/evidence highlight -> boundary -> invitation for questions. | Use large labels, fewer transitions, and explicit navigation cues. | Reading the poster aloud, tiny panels, missing "where to look now" cues. |

## Selection Checks

- If duration is missing, infer from user context only when safe; otherwise
  mark `duration` as unknown in `deck-brief.md`.
- If the deck must serve two durations, write the main route for the shorter
  variant and put extra material in backup slides.
- If the audience is nonexpert, lower density one level but do not invent
  simplified claims absent from the source.

## 8-Min Lightning

### Storyboard fragment example

| slide_num | claim | proof_object | on_slide_text |
| --- | --- | --- | --- |
| 1 | The task exposes a concrete reliability gap. | One motivating example. | One-sentence problem claim plus example label. |
| 4 | The proposed measurement isolates the key comparison. | Setup schematic. | Three short labels: input, readout, metric. |
| 7 | The main result changes how the audience should read the system. | One hero plot. | Claim title plus one takeaway callout. |

## 15-Min Conference

### Storyboard fragment example

| slide_num | claim | proof_object | on_slide_text |
| --- | --- | --- | --- |
| 2 | Existing evaluations miss the failure mode that matters here. | Related-work contrast table. | Two contrast bullets, no citation dump. |
| 8 | The method turns the research question into a measurable setup. | Framework or measurement figure. | Method claim plus compact panel labels. |
| 14 | The evidence supports the claim within a clear boundary. | Main result plus limitation callout. | Result takeaway and boundary phrase. |

## 20-Min Long Talk

### Storyboard fragment example

| slide_num | claim | proof_object | on_slide_text |
| --- | --- | --- | --- |
| 3 | The field gap has both conceptual and measurement sides. | Problem map. | Two-axis gap framing. |
| 11 | The experiment design separates the competing explanations. | Setup diagram plus control list. | Claim title and three controls. |
| 19 | The result pattern is stable enough to motivate the next question. | Result sequence. | Synthesis sentence plus next-question cue. |

## Poster Talk

### Storyboard fragment example

| slide_num | claim | proof_object | on_slide_text |
| --- | --- | --- | --- |
| 1 | The poster answers one central question. | Poster map or title region. | Question headline. |
| 3 | The method panel shows how to read the evidence. | Method figure. | "Start here" label plus two method terms. |
| 5 | The takeaway is visible without a full paper walkthrough. | Main result and summary box. | One claim and one boundary note. |
