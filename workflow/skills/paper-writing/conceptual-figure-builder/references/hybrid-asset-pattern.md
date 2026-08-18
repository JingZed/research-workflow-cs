# Hybrid Asset Pattern

Use this pattern when a paper-facing conceptual figure needs more visual polish
than a pure box-and-arrow diagram, but exact labels, arrows, and panel structure
must remain editable. The final figure is native layout plus semantic image
assets, not a full-figure raster. This translates the PPT-Visual-Replica
discipline of image generation -> icon grid -> grid cut -> asset directory ->
native layout/embed into the conceptual-figure workflow.

## Pipeline

### Step 1 - Inventory

List every semantic visual unit before generating images. Each unit should be the
smallest asset that could reasonably be moved, replaced, or regenerated alone.

| unit_id | asset_name | function | visual cue | exact text nearby | generated? |
| --- | --- | --- | --- | --- | --- |
| <unit id> | <icon png stem> | <what this unit helps readers understand> | <simple metaphor> | <native label beside it> | <yes/no> |

Command example:

```bash
mkdir -p experiments/conceptual-figures/<figure-id>-icons
```

Do not combine multiple semantic units into one raster asset. If an icon contains
both a prompt, a model, and a metric, split it.

## Asset Source Classes

| class | source | use for paper-facing? |
| --- | --- | --- |
| `imagegen_asset` | generated via image API (OpenAI image / Gemini imagegen / similar that accepts image inputs and returns polished semantic visuals) | preferred |
| `provided_asset` | user-supplied polished bitmap (icon library, manual download, vetted) with provenance recorded in manifest | acceptable |
| `script_drawn_asset` | deterministic PIL/SVG line-art drawn by the render script itself | absolutely prohibited for `status: ready` paper-facing figures; internal wireframe placeholder only |

If the current session cannot call an image API and the user has not provided
polished icons, do not self-substitute `script_drawn_asset` and claim hybrid-asset
success. Write the prompt/plan artifacts, mark `status: blocked` with blocker
`missing_imagegen_backend`, ask the user or handoff target for an
imagegen-capable execution pass, and stop.

`codex exec`, local Python/PIL, hand-written SVG, or any coding agent that writes
a renderer counts as `script_drawn_asset` unless it invokes a real
image-generating backend and saves returned image files. It can build the native
layout and wireframe, but it is not evidence that polished semantic assets were
generated.

### Step 2 - Plan-Then-Execute Contract (mandatory before any imagegen call)

Before invoking any image API or PIL drawing, write a complete prompt
specification to `<figure-id>.prompt.md`. This file is the single source of
truth for what icons should be generated and the contract between planning
and execution. The same agent or a different downstream agent may execute,
but no agent is allowed to inline-improvise icon prompts at execution time.

`<figure-id>.prompt.md` must contain:
- Icon inventory (one row per icon: icon_id / role / metaphor / target_size / paper-native style constraints)
- Per-icon prompt block (verbatim imagegen text using `prompt-library.md > Icon Generation Prompts` mandatory template)
- Grid sheet prompt if requesting a multi-icon grid (rows x cols / margin / gap / background / no-text rule)
- Asset slot manifest (where each icon will be placed in the final figure)

Only after this file is committed may execution proceed:
- current agent has image API: invoke imagegen, quoting prompts verbatim from
  the committed file. Do not rewrite at call time.
- current agent lacks image API: hand off to an imagegen-capable agent (e.g.
  `ccb ask <agent>`) referencing the prompt file path.

Inline-improvised imagegen calls without a prior `<figure-id>.prompt.md` commit is a Blocking failure regardless of icon quality.

Record `visual_generation_evidence` before final assembly:

| field | required content |
| --- | --- |
| backend | imagegen backend/tool/agent that returned the images, or `provided_asset` |
| prompt_file | path to `<figure-id>.prompt.md` or provenance file |
| handoff_id | CCB/job/tool id when another agent generated the assets, otherwise `none` |
| generated_files | icon sheet and per-icon file paths, or provided asset paths |
| asset_count | number of polished assets actually used in the final figure |
| source_class | `imagegen_asset` or `provided_asset`; never `script_drawn_asset` for ready paper figures |

If this evidence cannot be filled, do not run the final polished assembly.

### Step 3 - Grid Cut

Cut the sheet into one PNG per semantic unit:

```text
experiments/conceptual-figures/<figure-id>-icons/<icon-name>.png
```

Script skeleton:

```python
from pathlib import Path
from PIL import Image

sheet_path = Path("experiments/conceptual-figures/<figure-id>-icons/icon_sheet.png")
out_dir = sheet_path.parent
names = ["<icon-name-1>", "<icon-name-2>", "<icon-name-3>", "<icon-name-4>"]
rows, cols = 2, 2
margin, gap = 48, 32

im = Image.open(sheet_path).convert("RGBA")
cell_w = (im.width - 2 * margin - (cols - 1) * gap) // cols
cell_h = (im.height - 2 * margin - (rows - 1) * gap) // rows

for idx, name in enumerate(names):
    r, c = divmod(idx, cols)
    x0 = margin + c * (cell_w + gap)
    y0 = margin + r * (cell_h + gap)
    crop = im.crop((x0, y0, x0 + cell_w, y0 + cell_h))
    crop.save(out_dir / f"{name}.png")
```

If the sheet uses chroma-key, convert that background to alpha before saving the
per-icon PNGs. Trim only outer whitespace; never crop away visual meaning.

### Step 4 - Render Script

Assemble the final figure with a fixed canvas. Use native `<text>` for every
exact label, native shapes for panels/connectors, and base64 `<image>` embeds for
icons. PPT builds should follow the same separation: native text boxes and image
placements, not a full-slide raster.

SVG render skeleton:

```python
import base64
from pathlib import Path

W, H = 2400, 1050
icon_dir = Path("experiments/conceptual-figures/<figure-id>-icons")

def icon_href(name):
    data = base64.b64encode((icon_dir / f"{name}.png").read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="2400" height="1050" fill="#ffffff"/>',
    '<rect x="80" y="120" width="560" height="760" rx="24" fill="#f7fbff" stroke="#b8c7d9"/>',
    '<text x="120" y="180" font-size="32" font-family="Arial" fill="#20242a">Exact native label</text>',
    f'<image x="140" y="220" width="72" height="72" href="{icon_href("<icon-name>")}" preserveAspectRatio="xMidYMid meet"/>',
    '</svg>',
]
Path("experiments/conceptual-figures/<figure-id>.svg").write_text("\n".join(svg))
```

Command example:

```bash
python experiments/conceptual-figures/render_<figure-id>.py
```

### Step 5 - Manifest And Validate

Record each icon as a separate `semantic_units` entry with
`source_kind: generated` and `editability: replaceable_asset`. Record exact text
as native text. QA must inspect the rendered SVG/PNG/PPT at target size.

Validation checklist:

- Each required label is native text, not raster text.
- Each generated icon is one semantic unit.
- Every paper-facing generated/provided icon has `visual_generation_evidence`.
- The final source contains native panels/connectors plus embedded image assets.
- The manifest has one row per icon asset and one row per critical text or panel
  group.
- No final artifact is a full-figure raster unless the explicit mode is
  `candidate-image` or `replica-adaptation` preview.
- No paper-facing final at `status: ready` uses `script_drawn_asset` for
  polished semantic icons. Any occurrence blocks ready status and must be
  treated as `missing_imagegen_backend` or replaced with `imagegen_asset` /
  `provided_asset`.

## Worked Example: WDCT Measurement Setup

The user WDCT figure pipeline demonstrates the intended shape:

- Inventory identified small semantic icons for speech, scales, question,
  inconsistency gap, person-speech, school response, not-equal mark, bars,
  brain/readout, shield, warning, and related prompt-regime support.
- The asset directory contained 14 PNG files under `assets/wdct-icons/`,
  including individual icons plus intermediate `icon_sheet_alpha.png` and
  `icon_sheet_chromakey.png`.
- The render script used PIL for the PNG export and emitted an SVG with a fixed
  `2400 x 1050` canvas.
- The final SVG embedded 11 PNG icon placements as base64 `<image>` elements and
  kept exact labels as native SVG text/tspan fragments.
- The final layout combined generated icon assets with native panels, connectors,
  labels, and the boundary statement.

Use this as a pipeline reference, not as a filename or visual-design template.
For a new paper figure, invent the semantic inventory from the current brief and
generate a fresh icon sheet instead of copying the WDCT assets.
