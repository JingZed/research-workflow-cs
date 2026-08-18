# Build Path Selection

Choose the build path after `deck-brief.md`, `storyboard.md`, and
`style-spec.md` have enough information to constrain production.

## Build Paths

| path | trigger conditions | input contract | output contract |
| --- | --- | --- | --- |
| Codex Presentations default | Native PPTX is requested, storyboard is stable, and no exact template replication is required. | Deck brief, storyboard, style spec, asset manifest, available assets. | Editable PPTX, optional contact sheet, QA notes. |
| ppt-master-style serial | Source is large, style consistency is high risk, template/spec lock matters, or preview gates are needed between stages. | Locked brief, locked style spec, storyboard with statuses, source inventory. | Incremental deck build with preview/QA checkpoints and final PPTX when available. |
| PPT-Visual-Replica-style replica | User provides a flat slide, infographic, screenshot, or figure that must become editable PPT elements. | Source image, visual inventory, semantic unit plan, asset manifest. | Rebuilt native text/layout plus replaceable assets, not a full-slide screenshot. |

## Decision Tree

1. Is the primary task to recreate an existing flat slide/figure as editable?
   - Yes: use `PPT-Visual-Replica-style replica`.
   - No: continue.
2. Is there a strict reference deck/template or large source requiring staged
   preview and spec lock?
   - Yes: use `ppt-master-style serial`.
   - No: continue.
3. Is a final PPTX requested and presentation-building capability available?
   - Yes: use `Codex Presentations default`.
   - No: produce brief, storyboard, style spec, and asset manifest only.

## Path Checks

- Default path still needs rendered QA when a PPTX is produced.
- Serial path should not become a new runtime dependency; it is a discipline
  for ingest, spec lock, storyboard, preview, and QA.
- Replica path must rebuild exact text natively where practical and should
  generate only local semantic assets when needed.
