# Writer-Facing Outline Pattern

Use this pattern when `drafts/outline.md` must guide real drafting rather than merely name sections.

## Contents

- [What A Strong Outline Must Contain](#what-a-strong-outline-must-contain)
- [Choose Planning Depth](#choose-planning-depth)
- [Recommended Structure](#recommended-structure-inside-draftsoutlinemd)
- [Section And Subsection Contracts](#required-section-template)
- [Paragraph Function Contracts](#paragraph-function-contracts)
- [Key Sentence-Function Maps](#key-sentence-function-maps)
- [Spine And Section Archetypes](#spine-sentence-rule)
- [Results Arc And Drift Checks](#results-arc-pattern)
- [Good Enough Test](#good-enough-test)

## What A Strong Outline Must Contain

At minimum, the outline should make five things explicit:

1. the paper's single spine sentence
2. what each top-level section must accomplish
3. what each subsection contributes to that section's job
4. which evidence artifact owns each major claim
5. how the paper is most likely to drift or overclaim while drafting

If the outline cannot answer these five questions, it is still a section list, not a drafting plan.

## Choose Planning Depth

Use **structural depth** while the story is still being selected or when the
user requests only a compact plan. Stop at the spine, evidence map, section
contracts, hero visual, and page budget.

Use **drafting-ready depth** for a stable full-paper story or when another
writer should be able to draft without replanning. Add:

1. one function contract for every planned paragraph;
2. the logical handoff between adjacent paragraphs;
3. sentence-function maps for the abstract, Introduction, contribution
   paragraph, Discussion synthesis, Conclusion, and claim-sensitive passages.

When the user explicitly asks for every sentence's logic, extend the
sentence-function map across every planned paragraph. For technical prose,
sentence-or-move slots are acceptable: they preserve the argument sequence
without pretending the final sentence count is already known.

## Recommended Structure Inside `drafts/outline.md`

1. Core claim
2. Fallback weaker claim
3. One-sentence paper spine
4. Claim-evidence matrix
5. Hero figure or table
6. Section plan
7. Page or emphasis budget
8. Risks, drift modes, and unsupported side claims

## Required Section Template

For each top-level section, record all of the following:

- section purpose: what this section must do for the paper
- why it matters: why the reader needs this section now
- how to write it: the intended rhetorical mode for the section
- subsection roles: one short line per subsection describing its job
- evidence owner: which result rows, figures, or tables anchor the section
- main takeaway: what the reader should believe after finishing it
- interpretation boundary: what this section must not accidentally claim
- paper-facing boundary wording: the positive scope phrase a downstream writer
  should use instead of a defensive `not X` sentence
- drift risk: how this section is most likely to become vague, hypey, repetitive, or overclaimed

If a section cannot be described with this template, the outline is not ready for drafting.

## Writer-Facing Section Plan

Do not let a section remain in the outline if its purpose, subsection roles, and evidence owner are still unclear.

## Paragraph Function Contracts

At drafting-ready depth, plan every paragraph with this compact contract:

### Paragraph N: `<primary job>`

- **Role:** motivate, define, contrast, specify, report, interpret, synthesize,
  delimit, or transition.
- **Entry:** the question or conclusion inherited from the preceding paragraph.
- **Ordered moves:** the claims, evidence, definitions, or comparisons in the
  order the reader needs them.
- **Evidence and citations:** the artifact, result, or literature obligation
  that owns each load-bearing move.
- **Landing:** the one conclusion the paragraph must establish.
- **Handoff:** why the next paragraph is now needed.
- **Scope or drift risk:** the paper-specific misreading the paragraph should
  prevent through positive scope wording.

Give each paragraph one primary job. Several moves may serve that job, but
unrelated jobs require separate paragraphs. Do not use the paragraph plan to
repeat the same claim under several labels.

## Key Sentence-Function Maps

Use sentence-function maps for compact or rhetorically load-bearing passages.
At minimum in drafting-ready mode, map the abstract, the Introduction's opening
and gap-to-approach transition, the contribution paragraph, the Discussion's
main synthesis, the Conclusion, and any paragraph whose wording controls the
paper's claim scope.

Use an ordered table or list:

| Slot | Function | Required content or evidence | Logical relation |
|---|---|---|---|
| 1 | orient, motivate, define, or state the local question | paper-specific content | establishes the starting point |
| 2 | narrow, explain, contrast, or support | paper-specific evidence or comparison | answers or complicates the prior slot |
| 3 | report, interpret, delimit, or hand off | paper-specific result and scope | lands the paragraph or prepares the next one |

Add or remove slots according to the argument. Do not treat this three-row
illustration, a seven-sentence abstract, or any other fixed sequence as a
template. A slot is an argumentative obligation, not immutable surface form:
the final writer may merge or split slots while preserving their functions.

For technical paragraphs, prefer an ordered move sequence such as:

1. define the object;
2. explain why it is needed;
3. specify the implementation or comparison;
4. report the relevant observation;
5. interpret it at the supported scope;
6. create the transition.

Keep only the moves that the paragraph actually needs. If every planned
sentence merely lists a method detail or result, the paragraph still lacks an
argument.

## Subsection Role Pattern

Subsections should not just inherit the parent title. Each one should have a concrete role such as:

- define the task or operationalization
- state the repaired evaluation protocol
- establish the main empirical effect
- provide controls and baselines
- interpret an extension without overclaiming
- turn a negative result into a bounded takeaway

If two adjacent subsections do not have distinct jobs, the section is probably still under-designed.

## Spine Sentence Rule

Write one sentence that compresses the full paper arc:

- what phenomenon is established
- under which evaluation conditions
- what internal readout or mechanism-level result survives
- what contextual or intervention boundary keeps the claim bounded
- the positive paper-facing phrase for that boundary

Every major section should serve this sentence. If a section does not strengthen, qualify, or defend it, demote or remove that section.

## Section Archetypes

Use the following archetypes as defaults when building a paper plan.

### Introduction

- purpose: define the paper's problem, stakes, framing, and contribution ladder
- how to write it: problem-first, not literature-first
- common subsection jobs:
  - establish the phenomenon or failure mode
  - explain why it matters for evaluation or interpretation
  - introduce the paper's framing and method distinction
  - compress the full paper into a contribution paragraph
- drift risk:
  - becoming a broad field essay
  - jumping to methods before the problem is clear
  - promising stronger claims than later sections can support

### Related Work

- purpose: position the paper against the most relevant prior lines, not summarize a field
- how to write it: grouped comparison with a clear “what we add” at the end of each cluster
- common subsection jobs:
  - behavioral or task-level prior work
  - prompt/context/self-consistency prior work
  - probing/intervention/mechanistic prior work
- drift risk:
  - turning into citation laundry
  - listing papers without a positioning argument

### Task Framing And Setup

- purpose: make the task, prompt regimes, representations, and evaluation pipeline operationally clear
- how to write it: define the benchmark and protocol so the reviewer can reconstruct the logic without code
- common subsection jobs:
  - benchmark operationalization
  - prompt regimes or task variants
  - representation / feature construction
  - leakage-controlled evaluation
- drift risk:
  - describing machinery without saying what is actually predicted
  - underexplaining the evaluation protocol and leakage repair

### Main Results

- purpose: establish the core empirical phenomenon under the repaired protocol
- how to write it: phenomenon first, then readout, then controls
- common subsection jobs:
  - behavioral effect under repaired evaluation
  - activation-only readout
  - controls and baselines
  - short takeaway subsection if needed
- drift risk:
  - mixing behavior and interpretation too early
  - overstating decodability as mechanism or control

### Supporting Extension

- purpose: show what changes when the task condition changes, without pretending it is the same semantic regime
- how to write it: descriptive comparison plus interpretation boundary
- common subsection jobs:
  - behavioral effect under altered context or conditioning
  - readout under altered regime
  - explicit interpretation of what the extension does and does not mean
- drift risk:
  - framing conditional improvement as intrinsic improvement
  - treating non-equivalent task regimes as directly commensurate

### Intervention Or Stress Test

- purpose: test whether a readable signal also behaves like a reliable control axis
- how to write it: boundary-setting, not victory-lap causal language
- common subsection jobs:
  - why intervention is treated as a stress test
  - steering result
  - patching / ablation result
  - takeaway that separates decodability from controllability
- drift risk:
  - implying causal proof from weak or unstable manipulations
  - hiding negative or mixed results that are actually part of the conclusion

### Discussion

- purpose: unify the interpretation and explain what the results change about how the problem should be viewed
- how to write it: synthesis, not results repetition
- common subsection jobs:
  - theoretical reframing
  - relation between readout and controllability
  - implications for evaluation or method
- drift risk:
  - repeating section summaries
  - escalating into claims broader than the benchmark supports

### Limitations

- purpose: preempt the strongest reviewer objections without collapsing the paper's own contribution
- how to write it: specific, bounded, non-defensive
- common subsection jobs:
  - benchmark specificity
  - task non-equivalence
  - probing / mechanism caveat
  - intervention limitation
  - statistical / selection caveat
- drift risk:
  - vague generic limitation lists
  - apologizing for the entire paper

### Conclusion

- purpose: restate the paper's arc in its final, most disciplined form
- how to write it: compressed synthesis, not a table of contents recap
- common subsection jobs:
  - restate the repaired phenomenon
  - restate the readout result
  - restate the context boundary
  - restate the controllability boundary
- drift risk:
  - adding new claims
  - ending on generic alignment rhetoric instead of the paper's actual message

## Results Arc Pattern

When the paper has multiple empirical sections, prefer this order:

1. main result section: establish the phenomenon under the repaired protocol
2. supporting extension section: show how the phenomenon looks under changed task conditions
3. stress-test section: test whether the readable signal behaves like a controllable axis

This order is often stronger than a flat list of unrelated experiment families because it separates:

- what is established
- what is condition-dependent
- what remains bounded or negative

If the paper contains all three arcs, do not let the extension or stress test overshadow the repaired main result.

## Drift Checks

Before considering the outline complete, check for these common failures:

- the introduction is doing literature review instead of problem framing
- related work is a laundry list instead of a positioning argument
- setup describes machinery but not operationalization
- main results mix behavior, readout, and interpretation too early
- context sections are framed as performance improvement instead of changed task conditions
- intervention sections imply causal control when the evidence only supports a bounded stress test
- discussion repeats results instead of unifying the interpretation

## Section Failure-Mode Checklist

Use this checklist when a section still feels weak:

- Does the section have a job, or only a title?
- Does the section answer why it is needed at this point in the paper?
- Does each subsection have a distinct role?
- Is the main takeaway stated in one or two lines?
- Is the strongest evidence artifact named explicitly?
- Is the “what not to claim” boundary written down?
- Is the positive paper-facing wording for that boundary written down?
- Is the likely overclaim or rhetorical drift mode named?
- Does this section clearly serve the paper spine sentence?

## Good Enough Test

`drafts/outline.md` is strong enough when a different writing skill can draft from it without first re-planning:

- the section order feels inevitable rather than arbitrary
- each section has a visible job
- each section states how it should be written, not just what it covers
- at drafting-ready depth, each paragraph has one job, a landing, and a handoff
- key sentence-function maps expose the logic of load-bearing passages
- an explicit request for every sentence's logic is answered across all
  planned paragraphs, using move slots where exact sentence counts remain open
- each section has a named main takeaway
- each claim has a visible evidence owner
- each risky section has an explicit interpretation boundary
- each risky section has an explicit drift risk
- the page budget already tells you what can be compressed under venue pressure
