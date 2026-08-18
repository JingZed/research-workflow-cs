# Figure Spec: <figure-id>

## Purpose

- figure_job: <framework | method | measurement | pipeline | taxonomy | case | other>
- target_use: <paper single-column | paper double-column | deck | other>
- reader_question: <one sentence>
- visual_payoff: <what should be clear in five seconds>

## Claim Boundary

- allowed_message: <bounded claim or organizing relation>
- evidence_source: <path and relevant section/result>
- must_not_imply: <stronger or unsupported claim>

## Visible Content

- required_objects_or_panels:
  - <object/panel and role>
- required_labels_or_verbatim_blocks:
  - <exact text>
- caption_only:
  - <detail kept out of the visual surface>
- forbidden_content:
  - <internal or unsupported content>

## Layout Relations

| region | role | required content | relative placement |
| --- | --- | --- | --- |
| <id> | <role> | <content> | <placement> |

- connectors:
  - <source> -> <target>: <flow | comparison | grouping | transformation | measurement | evidence | boundary>
- semantic_icons: <few useful icons and their meaning, or none>

## Reference

- path: <path or none>
- role: <restore | compare | style only | none>
- traits_to_preserve_or_improve: <short list>
- required_content_changes: <short list or none>

## Production Constraints

- aspect_ratio_or_canvas: <binding value or unspecified>
- intended_insertion_size: <value or unspecified>
- native_text_or_editability: <requirements>
- expected_outputs: <PNG/SVG/PPT/etc.>
- minimum_legibility: <constraint>

## Unresolved Material Decision

<one user/scientific decision, or omit this section when none remains>

Omit unused rows or sections. Do not add workflow status, gate, reviewer,
approval, retry, handoff, salvage, or next-owner fields.
