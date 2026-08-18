# Raster Scaffold Overlay

Use this mode when a paper-facing figure needs imagegen-level visual taste and
exact paper text, but a full native SVG/PPT redraw would likely degrade the
visual rhythm. The core split is:

- imagegen owns the visual scaffold: composition, icons, card rhythm, lens or
  visual family, palette, spacing, and paper-native polish;
- native overlay owns all exact text and small emphasis marks;
- native code must not redraw the full figure geometry.

This is different from `raster-first-final`: `raster-first-final` accepts a
visual PNG as the final output. `raster-scaffold-overlay` requires a clean
text-light scaffold plus editable native text placed on top.

## Required Outputs

- `<figure-id>_scaffold.prompt.md`
- `<figure-id>_scaffold.png`
- `<figure-id>_overlay.svg`
- `<figure-id>_overlay.png`
- `<figure-id>_overlay_map.json`
- `<figure-id>_overlay_qa.md`

The canonical source is the overlay SVG plus the scaffold prompt and scaffold
PNG. The background visual is raster-locked; the paper text is editable.

## Pipeline

1. **Inventory exact text before imagegen.**
   List every `verbatim_content_blocks` entry and required label that will be
   visible. For each block, estimate line count, minimum readable font size at
   insertion scale, and whether it needs a full card, compact chip, or callout.
   Also copy the spec's `figure_vs_caption_split` and hard aspect/canvas
   constraints. Text inventory is not permission to change the paper figure
   shape.

2. **Generate a text-slot-aware scaffold.**
   The scaffold prompt must request the selected visual target family and
   explicitly reserve blank writing zones sized for the real text inventory.
   It is not enough to ask for generic placeholder bars.

   Scaffold prompt requirements:
   - no concrete scientific labels, prose, pseudo-words, legends, captions, or
     fake metrics;
   - large blank text zones where native text will be placed;
   - icons and decorative bars must stay out of those text zones;
   - long text blocks get larger cards or simpler icons, not tiny icon cards;
   - no extra cards or leftover visual objects that have no spec-owned text;
   - use selected candidate/icon assets as image references when available and
     record `input_image_paths` or the backend limitation.

3. **Run a scaffold slot audit before overlay.**
   Do not place text until `<figure-id>_overlay_map.json` proves the scaffold
   has usable slots. Each slot row must include:
   - `slot_id`
   - `bbox`
   - `text_block_id` or `required_label`
   - `estimated_lines`
   - `planned_font_size`
   - `icon_exclusion_zones`
   - `placeholder_bar_collision: yes | no`
   - `fit_verdict: pass | fail`

   Fail the scaffold and regenerate it when any exact-text slot is too small,
   when an icon overlaps the planned text area, when placeholder bars run under
   the text, or when unrelated extra cards remain. If the scaffold cannot fit
   the `must_show_in_figure` payload while preserving binding aspect/canvas
   constraints, return to the selected visual target or spec split; do not
   silently stretch the canvas or switch to a slide-like ratio.

4. **Build the native overlay.**
   The SVG should contain one full-figure `<image>` background for the scaffold.
   Native layers may add exact text, small translucent backplates, and minimal
   payoff/callout emphasis. They must not redraw the full card system,
   connectors, icons, panels, or background visual family.

   Overlay rules:
   - preserve spec-locked text exactly;
   - do not shrink body text below the agreed insertion-scale minimum just to
     make a bad slot fit;
   - do not paste text across icons or decorative bars;
   - keep backplates subtle and local;
   - if the overlay looks like a correction patch, regenerate the scaffold.

5. **Render and QA the overlay.**
   QA must review both scaffold and final overlay visually. A string-presence
   check is not enough.

## Ready Gate

`raster-scaffold-overlay` can pass only when all are true:

- scaffold has no readable scientific text or fake pseudo-text;
- every visible exact text block has a planned slot before overlay;
- text is readable at the intended paper/deck insertion size;
- text does not collide with icons, placeholder bars, borders, or connectors;
- scaffold keeps the selected visual target's paper-native rhythm;
- final overlay still reads as the scaffold visual, not a full native redraw;
- no extra scaffold card or decorative object remains without a spec-owned role;
- binding aspect ratio, canvas, and venue placement constraints are preserved
  or a user-approved spec update records the trade-off;
- the figure-vs-caption split is respected;
- QA includes screenshot-first notes on visual integration, not only programmatic
  `missing_required=[]` checks.

## Known Failure Modes

- **Pretty scaffold, unusable text slots.** The figure looks good until native
  text is pasted into tiny placeholder cards. Fix by regenerating a larger
  text-slot-aware scaffold, not by shrinking text.
- **Aspect-ratio escape hatch.** The executor makes the canvas taller or more
  slide-like to fit verbatim text. Fix by choosing a different visual grammar or
  revisiting the figure-vs-caption split, not by silently changing a hard paper
  constraint.
- **Coordinate paste overlay.** Text is technically present but visually floats,
  covers icons, or sits on top of placeholder bars. Fix the scaffold slots or
  overlay map.
- **QA false pass.** The QA only verifies that strings exist in SVG metadata or
  `<text>` nodes. This does not prove paper readiness.
- **Full native redraw regression.** The executor replaces the raster visual
  with Python/SVG cards and loses the imagegen taste. This fails the mode.
