# Output Mode Selection

Choose the simplest mode that preserves the figure's content, target use, and
editability needs. Do not add an exploration or review phase merely because the
figure is paper-facing.

| Mode | Use when | Minimum outputs |
| --- | --- | --- |
| native editable | Structure and exact text matter most | editable source, PNG, short QA |
| hybrid assets | Native layout/text needs a few polished semantic assets | editable source, assets, PNG, short QA |
| raster first | A polished final PNG matters more than editability | prompt, PNG, short QA |
| scaffold overlay | Imagegen supplies visual structure while exact text stays native | scaffold, overlay source, PNG, short QA |
| restoration | A supplied successful target needs bounded revision | revised source or PNG, short QA |

## Decision Rules

1. Reuse a supplied target or existing selected direction when it satisfies the
   claim and target-use constraints.
2. Prefer native editable output for exact-text diagrams and taxonomies.
3. Use hybrid assets only when semantic visual landmarks materially improve
   comprehension.
4. Use raster-first only when the requested deliverable is a polished image
   and exact editable text is not required in this pass.
5. Use scaffold-overlay when exact labels are required but the visual structure
   benefits from image generation.
6. If the visual family is unresolved, create one primary draft and at most one
   alternative only in explicit `explore` mode.

## Stop Rules

- Stop when required content cannot fit legibly at the binding aspect ratio.
- Stop after one local correction pass if the actual render still fails.
- Report a missing image-generation capability as a concrete blocker; do not
  create a handoff file, candidate matrix, or reviewer state.
- A separate `critique` mode pass is optional and explicit-only.
