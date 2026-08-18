# Deck QA Template

## Deck

- deck_id: <stable deck id>
  Match the id used in the brief, storyboard, and exported PPTX.
- reviewed_artifact: <PPTX, PDF export, contact sheet, or preview path>
  Review the artifact that will be delivered or presented.
- review_context: <duration, audience, language, and display condition>
  QA should reflect the actual talk setting.

## Checklist

- thumbnail_rhythm: <pass | needs_update; rhythm issue>
  The contact sheet has a clear progression without repetitive or abrupt slide patterns.
- text_overflow: <pass | needs_update; overflow issue>
  No visible text clips, overlaps, or becomes unreadable in presentation mode.
- figure_legibility: <pass | needs_update; figure issue>
  Figures and labels are readable from the expected viewing distance.
- alignment: <pass | needs_update; alignment issue>
  Margins, titles, footers, and primary objects align consistently.
- asset_quality: <pass | needs_update; asset issue>
  Screenshots, generated assets, and imported figures are sharp enough and not distorted.
- source_footers: <pass | needs_update | not_applicable; citation issue>
  Source footers are present where needed and do not overcrowd slides.
- internal_leakage_check: <pass | needs_update; leaked instruction>
  Visible slides do not contain prompt text, timing constraints, workflow notes, or hidden requirements.

## Verdict

- verdict: <pass | needs_update>
  Use pass only when the deck is ready for the requested delivery context.

## Fix Items

- fix_1: <blocking or nonblocking fix with slide number/path>
  Make the fix actionable without rereading the whole deck.
- fix_2: <blocking or nonblocking fix with slide number/path>
  Add another item only when it changes the next build step.
