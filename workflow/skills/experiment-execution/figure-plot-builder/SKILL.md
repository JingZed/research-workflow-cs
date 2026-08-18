---
name: figure-plot-builder
description: "Build paper-ready plots and caption notes from aggregated results. Use when Codex needs to choose visual encodings, organize the `experiments/plots/` folder, keep a consistent plot pack style, and prepare figure-level takeaways from `experiments/results/summary.md` before manuscript drafting."
---

# Figure Plot Builder

## Overview
Turn result tables into a consistent plot set with captions and takeaways that a paper draft can absorb later.

Optional plotting-agent ideas may be consulted as reference-only guidance for
caption discipline, but the native statistical plotting pipeline remains the
only default route here. Route framework figures, method schematics, pipeline
diagrams, and conceptual illustrations to `$conceptual-figure-builder`.

## Consume
- `experiments/results/summary.md` and any raw tables required for plotting.
- Canonical result IDs, baseline-use status, prediction branch, and anomaly or
  deviation status recorded in that summary.
- Optional target figure list from `drafts/outline.md`.
- Optional `experiments/conceptual-figures/index.md` when empirical plots need
  to align with a separate conceptual figure pack.
- Optional style constraints such as monochrome printing or venue figure limits.

## Produce
- `experiments/plots/`
- `experiments/plots/index.md`

## Workflow
1. Reconcile every plotted value with a canonical result tuple in
   `experiments/results/summary.md`. If the tuple is missing, internally
   conflicting, or blocked by an unresolved upstream reference, stop that plot
   and route the issue to `$result-aggregator`.
2. Choose the smallest set of figures that actually supports the current claims.
3. Designate a hero figure when one figure clearly carries the paper's main empirical message; demote the rest to supporting figures or tables.
4. Create or specify each figure with title, axes, legend, canonical result IDs,
   source table or run IDs, intended takeaway, and expected output filename.
5. Keep plot style, typography, color semantics, and file naming consistent across the whole figure pack.
6. Write `experiments/plots/index.md` so downstream writing skills know what each figure proves, how it was generated, and which claim it supports. For each
   paper-facing plot, reference the relevant result IDs, prediction IDs and
   selected outcome branch, baseline IDs and allowed use, plus any unresolved
   anomaly or deviation. Do not copy the upstream ledgers into the index.
**Step 6a.** If an active `<paper-dir>/provenance.yaml` already exists, append
   `figures[]` entries for each paper-facing figure produced in the current
   session. Include `figure_id`, `plot_script`, `result_file`, and optional
   `claim_tags`. If the file does not exist, skip this step and do not
   auto-create it. If `<paper-dir>` resolution is missing or ambiguous, skip
   the append and record in `experiments/plots/index.md` that provenance append
   was skipped due to missing or ambiguous paper-dir.
7. Keep figure captions factual and connected to the underlying conditions.
8. For every paper-facing figure or table, record caption notes with five fields when applicable: comparison, metric, condition, takeaway, and caveat.

## Quality Bar
- Maintain consistent naming, labeling, and color semantics across plots.
- Prefer one figure one generation path when code exists, so later refreshes do not require manual re-assembly.
- Make the main takeaway legible without reading the whole result table.
- Keep captions aligned with the numbers actually shown.
- Require plotted values and derived deltas to match their canonical result
  tuples after declared unit conversion and rounding.
- A contextual-only or incompatible baseline must never be visually framed as
  a primary gain. Ambiguous, negative, and technically blocked branches remain
  visible when they are material to the figure's interpretation.
- Make caption notes self-contained enough for downstream drafting: readers should be able to identify what is compared, what metric is shown, under which condition, what the takeaway is, and what caveat limits the figure if one matters.
- Follow `../../_shared/writing-constraint-layer.md` when writing caption
  notes. Name the comparison the figure supports, the tested condition, and
  any measured caveat directly instead of using defensive boilerplate.
- If caption-shaping reference is needed, use plotting-agent ideas only as
  optional guidance rather than as a route replacement.
- When appending to an existing `provenance.yaml`, record actual generation
  scripts and source result files. Do not infer or invent paths from figure
  names, captions, or memory.

## Boundaries
- Do not rewrite manuscript sections here.
- Do not use a plot to claim more than the results support.
- Do not hide missing baselines or weak comparisons behind polished visuals.
- Do not upgrade baseline parity, prediction-branch, or anomaly-adjustment
  status in a figure or caption.
- Do not use caption notes to imply a comparison, condition, or caveat that is absent from the plotted data or source table.
- Do not use defensive paper-positioning templates in caption notes. Concrete
  negative findings may remain when they report a measured result or ruled-out
  alternative.
- Do not create framework figures, method schematics, pipeline diagrams, or
  conceptual illustrations; route those to `$conceptual-figure-builder`.
- Do not replace the native statistical plotting pipeline with plotting-agent-style reference guidance.
- Do not use an image-generation model to create or alter empirical data marks,
  axes, error bars, labels, or values.
- Do not add new canonical outputs or Produce entries just to expose optional plotting references.
- Do not create `provenance.yaml`; optional provenance append is a side effect
  only when the file already exists.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `references/figure-pack-pattern.md` when you want a stable figure-pack structure with hero figure choice, per-figure provenance, and consistent export expectations.
- If PaperOrchestra is separately installed, consult its plotting-agent Skill
  only for optional caption-discipline or diagram-planning reference; do not
  treat it as the default path or a required dependency.

---

## Style Appendix: Academic Plot Style Guide

Use this appendix when generating or refreshing actual plot files under `experiments/plots/`. These rules tighten the visual contract so paper-facing plots are readable, print-safe, and stylistically consistent.

### Global Rendering Defaults

- Render all raster plots at **300 DPI** minimum.
- Use a headless matplotlib backend for batch rendering.
- Save with tight bounding boxes and small padding.
- Close every figure after saving so long plot batches do not leak memory.

Recommended matplotlib defaults:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "axes.labelsize": 8,
    "axes.linewidth": 0.6,
    "legend.fontsize": 7,
    "legend.framealpha": 0.95,
    "legend.edgecolor": "#cccccc",
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
    "grid.alpha": 0.15,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.3,
})
```

### Color Palette

Use a muted, print-safe academic palette. Do not use matplotlib default saturated colors.

```python
PALETTE = ["#2060cc", "#cc3030", "#208040", "#cc7020", "#8040cc", "#b08020", "#666666"]
# Blue / Red / Green / Orange / Purple / Gold / Gray
```

### Typography and Labeling

- Always include axis labels with units where applicable.
- Keep tick labels readable at final paper size.
- Use bold titles only when the title adds information beyond the caption.
- Prefer concise legend labels that match paper terminology exactly.

### Axis and Spine Rules

- Hide top and right spines for all standard plots.
- Use light grid lines only when they improve numeric readability.
- Avoid misleading axis truncation unless explicitly documented.

```python
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

### Legend Rules

- Keep legends inside the axes area when possible.
- If a legend must sit outside the axes, use an explicit anchor and verify it does not overflow.
- Use consistent ordering across plots when the same methods reappear.

### Aspect Ratio Contract

Choose one of the following ratios for paper-facing plots and keep it exact.

| Ratio | Inches (W × H) | Typical Use |
|---|---|---|
| `1:1` | 3.4 × 3.4 | Square ablation grid (single-column) |
| `2:3` | 3.4 × 5.1 | Portrait (single-column) |
| `3:2` | 5.1 × 3.4 | Landscape (spans two columns) |
| `4:3` | 4.0 × 3.0 | Standard rectangle (single-column) |
| `5:4` | 4.5 × 3.6 | Wide rectangle (single or narrow double-column) |
| `16:9` | 5.5 × 3.09 | Wide chart (double-column) |
| `21:9` | 7.0 × 3.0 | Multi-panel banner (full-width) |

Typical venue widths: single-column ≈ 3.0–3.5 in; double-column ≈ 5.0–7.0 in. Check the venue's LaTeX template for exact column widths — these ratios are shape guides, not hard placement rules.

If no enumerated ratio fits the panel structure or data layout, use the closest ratio as a starting point and document the actual dimensions and reason in `experiments/plots/index.md`.

### Pattern-Specific Rules

**Line charts**: line width ~1.3; smooth only when smoothing rule is documented; preserve raw generation path in provenance.

**Grouped bar charts**: white bar edges with thin lines; explicit error bars for CI (not textual claims in caption); consistent metric ordering across figures.

**Heatmaps**: perceptually ordered colormap; fix `vmin`/`vmax` intentionally for cross-panel comparisons; annotate cells only when grid is small enough to be legible.

**Multi-panel figures**: shared style, consistent axis semantics, aligned scales; keep panel titles short and bold.

### Caption Rules

- Every paper-facing figure must have a factual caption in `experiments/plots/index.md`.
- Captions must describe what is actually plotted, not what the paper wishes the plot implied.
- Caption notes should identify the comparison, metric, condition, takeaway, and caveat when those fields are applicable.
- Do not embed `Figure N:` text into captions.
- One figure, one takeaway whenever possible.

### Pre-Export QA Checklist

Before accepting a plot into the figure pack:
- [ ] Axis labels correct and units present
- [ ] Legend present when needed, no overlapping labels
- [ ] No unreadable text at final export size
- [ ] No misleading scaling choices
- [ ] Colors distinguishable in print
- [ ] Caption matches plotted data exactly
- [ ] Plot traceable to one source table or generation path

### Anti-Patterns

- No 3D charts, pie charts, or decorative gradients/shadows.
- No default matplotlib colors.
- No omitted axis labels or units.
- No legend outside axes without explicit anchoring.
- Never claim data that is not directly plotted.
