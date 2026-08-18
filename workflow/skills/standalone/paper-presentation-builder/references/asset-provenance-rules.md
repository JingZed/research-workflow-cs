# Asset Provenance Rules

Use these rules when filling `asset-manifest.md` and deck QA.

| source | allowed use | provenance required | when to redo |
| --- | --- | --- | --- |
| figure-plot-builder | Empirical plots, ablations, tables, heatmaps, metric comparisons. | Plot index entry, source data/script path, export path. | Redo when labels are unreadable, plot is stale, or slide crop changes interpretation. |
| conceptual-figure-builder | Framework, method, measurement, taxonomy, mechanism, or concept visuals. | Conceptual figure index entry, brief, export, manifest when available. | Redo when claim boundary changes, exact text is malformed, or editability is needed. |
| paper figure | Existing figure from the manuscript or source paper. | Paper path, figure number/page, caption or source note. | Redo or simplify when the figure is too dense, cropped context is misleading, or permissions/provenance are unclear. |
| screenshot | UI, tool output, document excerpt, or evidence snapshot. | Original file/URL, capture date when relevant, crop path. | Redo when resolution is low, private data appears, or the screenshot carries irrelevant chrome. |
| AI-generated | Icons, mini-scenes, background-free semantic assets, candidate visuals. | Prompt/spec path, generation date if known, asset path, intended semantic role. | Redo when text appears in raster, style conflicts, provenance is missing, or asset implies unsupported claims. |
| web image | Public image used only when user permits or it is necessary for context. | URL, license/credit note, access date, local copy path. | Redo or replace when license is unclear, image is stock-like, or source fidelity matters. |

## Labeling Rules

- Visible source footers are required for reused paper figures, web images, and
  third-party screenshots unless the deck context explicitly omits footers.
- Internal source paths may live in speaker notes or `asset-manifest.md` when
  visible footers would distract.
- Generated assets should not be cited as evidence; label them as schematic or
  illustrative in notes when ambiguity is possible.

## Redo Triggers

- Any asset that changes the source claim when cropped must be rebuilt or
  replaced.
- Any asset with unreadable embedded text at slide scale must be redrawn,
  simplified, or converted to native text.
- Any asset lacking provenance cannot be marked `ready`.
