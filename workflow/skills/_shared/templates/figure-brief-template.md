# Figure Brief Template

## Identity

- figure_id: <stable figure id, e.g. fig1_framework>
  Use this id consistently across brief, candidate board, manifest, QA, and exports.
- job: <framework overview | method schematic | pipeline | taxonomy | case walkthrough | measurement setup | mechanism sketch>
  State the single reader job this figure must perform.
- audience: <venue, reviewer type, talk audience, or paper section>
  Name who must understand the figure and at what depth.
- aspect_ratio: <single-column | double-column | 16:9 | custom width x height>
  Fix the target shape before layout decisions are made.
- hard_visual_constraints:
    aspect_ratio: <binding | flexible, with source>
    canvas_or_slot: <binding | flexible, with source>
    failure_action: <change grammar | change split | needs_user_decision>

## Paper Foundation

- visual_sentence: <one sentence naming what the figure makes visible>
- reader_question: <what question this figure answers for the reader>
- paper_objects: <objects/variables/components that must be visually represented>
- semantic_relations: <relations that must become connectors/grouping/contrast/sequence>
- visual_payoff: <what should be remembered in a five-second read>

## Figure-vs-Caption Split

- must_show_in_figure: <exact blocks/relations/labels that must stay visible>
- may_show_if_space: <optional visual labels/details>
- caption_only: <definitions, caveats, or procedural details reserved for caption>
- omit: <internal labels, unsupported claims, redundant text>
- split_risk: <where text pressure could break layout, density, or hard constraints>

## Label Contract

- required_labels: <exact labels that must appear as native text when possible>
  Keep exact scientific terms here so generation does not paraphrase them.
- forbidden_labels: <terms, claims, or wording that must not appear>
  List labels that would widen claims, leak workflow notes, or confuse scope.

## Visual Target Contract

- visual_direction_file: <experiments/conceptual-figures/<figure-id>.visual-direction.md or none>
  Required for nontrivial greenfield paper-facing figures before production.
- reference_file: <path or none>
  Use when a prior successful figure, user target, or editable source sets the visual quality bar.
- reference_source_file: <editable SVG/PPT/script path or none>
- reference_role: <restoration_target | baseline_to_beat | style_reference | none>
  `restoration_target` means preserve/repair the reference. `baseline_to_beat`
  means compare against it but do not select or restore it as the final target.
  `style_reference` means borrow only named visual tokens.
- preserve_visual_tokens:
    panel_rhythm: <what must stay>
    card_density: <what must stay>
    icon_scale_and_presence: <what must stay>
    callout_hierarchy: <what must stay>
    typography_hierarchy: <what must stay>
    palette_and_border_weight: <what must stay>
    connector_style: <what must stay>
- allowed_changes: <labels, local spacing, arrows, broken assets, claim-safety wording, etc.>
- forbidden_visual_regressions: <weaker icons, emptier boxes, softer payoff, lower density, generic rebuild, etc.>
  For greenfield figures, set `reference_file` to the selected candidate or
  sketch path and treat it as the visual target for first-render comparison.

## Layout Contract

- panel_structure: <panel count, panel names, and reading order>
  Describe the visible organization before choosing visual style.
- connector_contract:
    required_connectors: <source -> target list for every required visible arrow/line/brace>
    connector_style: <downward arrows | left-to-right arrows | braces | comparison marks | none-with-reason>
    visibility_rule: |
      Required flow, comparison, or sequence relations must be visible native
      connectors in the final source. Arrows embedded only in text strings
      (e.g. model outputs) or semantic icons do not satisfy this contract.
  Use `none-with-reason` only when the layout is intentionally non-sequential.
- worked_example_panel:
    required_for_types: [measurement-setup, case-walkthrough]
    description: <one concrete instance walked verbatim through the figure's flow>
    fields:
      input_stimulus_verbatim: <exact prompt text, A/B options, framing — no paraphrase>
      model_intermediate_state: <exact intermediate response, e.g. word/speak answer>
      model_output_verbatim: <exact deed/action response>
      derived_label: <how input + output yields the figure's central label, e.g. consistency_label = 0>
    hard_rule: |
      The verbatim fields must be quoted from real benchmark items, not
      paraphrased. Paraphrasing the prompt or model responses fails the
      `worked_example_specificity` dimension of Reference Alignment Gate
      (see figure-qa-rubric.md Blocking Criteria).
  Include a concrete worked example when the figure type needs readers to track a case through the setup.
- arrows_relations: <source -> target relation list with semantics>
  Define whether each connector means flow, contrast, dependency, evidence, or transformation.
- visual_style: <clean schematic | technical diagram | minimalist icon system | paper-native line art | other>
  Choose a style that fits the venue and paper tone.
- output_mode: <reference-restoration | editable-diagram | candidate-image | hybrid-asset | raster-scaffold-overlay | raster-first-final | replica-adaptation>
  Record the build path so downstream QA knows what editability to expect.
- visual_generation_capability: <actual_imagegen_available | api_fallback_available | imagegen_handoff_required | provided_visual_target_only | no_visual_generation>
  Required when output_mode is `candidate-image`, `hybrid-asset`,
  `raster-scaffold-overlay`, or `raster-first-final`. Local
  SVG/PIL/code-rendered sketches are wireframes and do not count as actual
  imagegen capability.
- workflow_blocker: <none | requires_desktop_visual_session | missing_imagegen_backend>
  For paper-facing framework, measurement-setup, pipeline-process,
  mechanism-sketch, or case-walkthrough figures, `no_visual_generation` blocks
  final image production.
- visual_generation_plan:
    source_classes_allowed: <imagegen_candidate/provided_reference/paper_figure_reference>
    evidence_required: <backend/tool, prompt file, generated files, run id, or provided/reference path; if ~/.codex/private/openai-imagegen.env is used, record key as redacted>
    input_image_paths: <selected candidate/icon sheet/icon assets used as image inputs, or none>
    asset_conditioning: <used | unavailable | not_applicable>
    blocker_if_missing: <requires_desktop_visual_session | missing_imagegen_backend | none>
- vectorization_status: <not_applicable | downstream_optional | pending | complete>
  Use `downstream_optional` when output_mode is `raster-first-final` and the
  present pass intentionally stops at best visual PNG.
- raster_overlay_contract: <not_applicable | scaffold_prompt/scaffold_png/overlay_svg/overlay_png/overlay_map required>
  Required when output_mode is `raster-scaffold-overlay`; record that
  background geometry is raster-locked and exact text is native overlay.
- layout_discipline_check:
    venue: <ACL-EMNLP-double | NeurIPS-single | poster | other>
    typography_scale: <complies | exempt-with-reason>
    palette_pastel: <complies | exempt-with-reason>
    vertical_rhythm: <complies | exempt-with-reason>
    box_content_density: <complies | exempt-with-reason>
    callout_payoff_hierarchy: <complies | exempt-with-reason>
    auxiliary_strip_size: <complies | exempt-with-reason>
    exemption_reason: <required if any exempt>

## Provenance

- source_files: <paper sections, sketches, figures, notes, or result artifacts>
  List every source that constrains the figure content.
- claim_boundary: <what the figure may claim, what it only organizes, and what it must avoid implying>
  Separate evidence-backed statements from conceptual scaffolding.
