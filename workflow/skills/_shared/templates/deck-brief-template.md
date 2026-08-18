# Deck Brief Template

## Identity

- deck_id: <stable deck id>
  Use this id for the presentation directory and exported PPTX.
- source_files: <paper, PDF, manuscript, notes, figures, or URLs>
  List the sources that constrain the deck content.
- audience: <reviewers | conference peers | thesis committee | lab meeting | class | other>
  Define the audience so depth and terminology stay calibrated.
- language: <English | Chinese | bilingual with rule>
  Fix visible slide text and speaker-note language before drafting.

## Delivery Contract

- duration: <target talk duration in minutes>
  Use duration to set slide budget and speaker-note depth.
- slide_count_target: <target main-slide count plus optional backup count>
  Keep the deck within the delivery window.
- depth_level: <high-level | technical peer | expert | mixed>
  Specify how much method and evidence detail each slide should carry.
- template_ref: <path to reference deck/template or "none">
  Record style inputs without copying them blindly.

## Claim Contract

- must_cover_claims: <ordered list of claims that must appear>
  These claims form the deck spine and should map to storyboard rows.
- must_avoid_claims: <claims, terms, or implications to avoid>
  Use this to prevent overclaiming, anonymity leaks, or workflow leakage.

## Output

- output_mode: <standalone | idea-integrated>
  Choose standalone unless the user explicitly asks to write inside an idea workspace.
- output_root: <cwd-relative path | absolute path | idea-root>
  Record the root that `presentations/<deck-id>/` is relative to.
- final_artifact_format: <storyboard only | PPTX | PDF export | PPTX plus speaker notes | other>
  Name the requested deliverable so build and QA gates are clear.
