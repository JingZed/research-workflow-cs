# Asset Manifest Template

| asset_id | source | slide_placement | provenance_path | status |
| --- | --- | --- | --- | --- |
| <stable asset id> | <figure-plot-builder | conceptual-figure-builder | screenshot | generated | paper-figure> | <slide number and role> | <source path, paper page, prompt, or figure registry entry> | <needed | available | needs_redraw | needs_permission | ready> |
| <stable asset id> | <figure-plot-builder | conceptual-figure-builder | screenshot | generated | paper-figure> | <slide number and role> | <source path, paper page, prompt, or figure registry entry> | <needed | available | needs_redraw | needs_permission | ready> |
| <stable asset id> | <figure-plot-builder | conceptual-figure-builder | screenshot | generated | paper-figure> | <slide number and role> | <source path, paper page, prompt, or figure registry entry> | <needed | available | needs_redraw | needs_permission | ready> |

Track every nontrivial visual asset so the final deck can be audited for source fidelity and editability.

## Field Notes

- asset_id: <stable asset id>
  Use a durable id that storyboard rows can reference.
- source: <figure-plot-builder | conceptual-figure-builder | screenshot | generated | paper-figure>
  Classify the origin so provenance and redo rules are clear.
- slide_placement: <slide number and role>
  Record where the asset appears and what job it performs.
- provenance_path: <source path, paper page, prompt, or figure registry entry>
  Make the asset traceable back to the source or generation spec.
- status: <needed | available | needs_redraw | needs_permission | ready>
  Use status to decide whether the deck can proceed to build or QA.
