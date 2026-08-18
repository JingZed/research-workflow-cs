# Figure QA

- figure_id: <id>
- rendered_file: <path>
- source_file: <path or none>
- spec_file: <path or none>
- production_mode: <mode>
- checked_at_target_size: <yes | no>

## Focused Checks

- required_content_and_claim_scope: <pass | fail; note>
- text_legibility_and_containment: <pass | fail; note>
- reading_order_and_connectors: <pass | fail; note>
- reference_fidelity: <pass | fail | not applicable; note>
- local_visual_quality: <pass | fail; note>

## Result

- result: <ready | blocked>
- blocker: <one concrete defect or none>
- correction_passes: <0 | 1>

Do not add critic, gate, salvage, routing, reviewer, or next-owner fields.
