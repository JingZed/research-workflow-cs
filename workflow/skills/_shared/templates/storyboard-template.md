# Storyboard Template

| slide_num | working_title | claim | proof_object | visual_plan | required_asset | on_slide_text | speaker_note_point | source_provenance | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <slide number> | <claim-like draft title> | <one slide, one claim> | <figure, result, example, setup, quote, or transition> | <layout or visual treatment> | <asset id or path needed> | <visible text bullets or labels> | <one spoken beat for this slide> | <source file and section/page> | <planned | assets_needed | drafted | rendered | qa_needed | ready> |
| <slide number> | <claim-like draft title> | <one slide, one claim> | <figure, result, example, setup, quote, or transition> | <layout or visual treatment> | <asset id or path needed> | <visible text bullets or labels> | <one spoken beat for this slide> | <source file and section/page> | <planned | assets_needed | drafted | rendered | qa_needed | ready> |
| <slide number> | <claim-like draft title> | <one slide, one claim> | <figure, result, example, setup, quote, or transition> | <layout or visual treatment> | <asset id or path needed> | <visible text bullets or labels> | <one spoken beat for this slide> | <source file and section/page> | <planned | assets_needed | drafted | rendered | qa_needed | ready> |

Use one row per slide and keep production notes out of `on_slide_text`.

## Field Notes

- slide_num: <slide order number>
  Use stable numbering so QA fixes can point to exact slides.
- working_title: <claim-like draft title>
  Prefer a talk claim over a generic section label.
- claim: <one slide, one claim>
  Keep each slide mapped to one argument beat.
- proof_object: <figure, result, example, setup, quote, or transition>
  Name the evidence or object that earns the slide's place.
- visual_plan: <layout or visual treatment>
  Describe the intended slide composition before building it.
- required_asset: <asset id or path needed>
  Link the row to `asset-manifest.md` whenever a visual asset is required.
- on_slide_text: <visible text bullets or labels>
  Keep only text that should appear on the slide.
- speaker_note_point: <one spoken beat for this slide>
  Put delivery explanation here instead of overcrowding the slide.
- source_provenance: <source file and section/page>
  Make every claim traceable to a paper, note, figure, or source.
- status: <planned | assets_needed | drafted | rendered | qa_needed | ready>
  Use status to drive the next build or QA action.
