# Prompt Library

Use only when actual imagegen is available or when handing off to an
imagegen-capable agent. Do not use these prompts to justify local PIL/SVG/Python
wireframes.

## Candidate Matrix Prompt

Keep candidate prompts visual-focused. They may be detailed, but they should
describe the target figure family rather than paste the whole spec. Exact long
prose and final label fidelity belong to spec/production.

```text
Create a polished academic schematic candidate for <figure job>.
Visual sentence: <one sentence>.
Canvas: <aspect-matched candidate size from spec, e.g. 1536x672 for 16:7>.
Layout grammar: <grammar>; treatment: <schematic_precision | editorial_clarity | mechanism_evidence>.
Show: <3-6 visual units and semantic relations>.
Main payoff: <five-second takeaway>.
Style: clean paper-native diagram, restrained palette, strong hierarchy,
clear text slots, no dense prose.
```

Example:

```text
Create a polished 1536x672 academic schematic candidate for WDCT measurement
setup. Three zones: Stakes, Paired task worked example, Analysis lanes. Make
center largest with SPEAK/ACT cards, A/B option slots, and coral
consistency_label = 0 badge. Show left coral GAP between stated preference and
later choice. Right has Behavior, Readout, Coarse edit stress tests,
Interpretive boundary. Bottom has prompt regimes chips. Clean paper-native
Figma style, soft amber/blue/lavender/green, coral accents, no dense text.
```

## Raster-First Final Prompt

```text
Create the strongest paper-native final PNG for this selected visual direction.

Use selected target as art direction: <path/description>
Preserve: <visual tokens from visual-direction>
Aspect/canvas: <binding size>
Text policy: avoid exact long prose in raster; reserve clean areas for native
text overlay if exact text is required.
Must show visually: <objects/relations/callouts>
Must not show: <forbidden claims/labels/internal ids>

Style: polished academic infographic for a research paper, restrained colors,
high readability, clear five-second payoff, no dashboard/form/template-slide
feel, no fake labels, no watermark.
```

## Scaffold Overlay Prompt

```text
Create a text-light scaffold PNG for a paper figure.

Use selected target as art direction: <path/description>
Reserve blank readable slots for these native text blocks:
<list blocks and approximate sizes>

Do not write final scientific labels. Use blank cards, placeholder bars, icons,
connectors, and panel structure only. Keep icon zones clear of text zones.
Aspect/canvas: <binding size>
Style: paper-native academic schematic, restrained, no decorative UI chrome.
```

## Icon Sheet Prompt

```text
Create a grid of semantic icon assets for a paper figure.

Icons:
1. <icon_id>: role=<role>, metaphor=<metaphor>, theme=<color>, size=<target>
...

Style: consistent paper-academic flat icons, transparent or solid chroma-key
background, no text, no letters, no numbers, no logos, no shadows, no 3D.
Each icon must remain legible at paper insertion size.
```
