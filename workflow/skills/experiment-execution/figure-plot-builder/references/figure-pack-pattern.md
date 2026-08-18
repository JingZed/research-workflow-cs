# Figure Pack Pattern

Use this pattern when `experiments/plots/` should behave like a reproducible paper figure pack rather than a pile of screenshots.

## Per-Figure Expectations

For each planned figure, keep:

- stable filename stem
- purpose
- claim supported
- source table or run IDs
- generation path if code exists
- short factual caption note

Store these in `experiments/plots/index.md` even if the generation scripts live elsewhere.

## Hero Figure Rule

Mark one figure as the hero figure when it carries the paper's central empirical message.

The hero figure should get:

- the cleanest layout
- the least cognitive overhead
- the strongest caption support

Do not hide the strongest result in figure 5 while leading the story with a weaker artifact.

## Consistency Rule

Across the whole figure pack, keep consistent:

- color semantics
- axis naming
- label abbreviations
- decimal precision
- model or dataset ordering

Readers should not have to relearn the visual language from one figure to the next.

## Export Rule

When code exists, prefer one figure one generation path and export both:

- manuscript-ready assets
- an editable or regenerable source path

That reduces silent drift between last-minute edits and future reruns.
