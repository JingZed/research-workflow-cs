---
name: research-review
description: "Run a multi-round independent external critique of a research idea, evidence package, or manuscript. Explicit-only: use only when the user explicitly invokes $research-review or clearly requests a deep external or multi-round review; ordinary review requests belong to targeted-critic."
---

# Deep Research Review

## Role

Conduct a bounded dialogue with an independent reviewer capability, challenge
both the work and the review, and turn the exchange into actionable scientific
advice. This is deeper than a single `targeted-critic` pass and remains
read-only unless the user separately requests edits.

## Consume

- The exact idea, evidence bundle, paper candidate, or section to review.
- Current claims, method, results, limitations, invariants, and known concerns.
- The user's questions, target audience or venue, compute/time constraints, and
  requested reviewer perspective.
- Optional prior external-review session locator for an explicit continuation.

## Produce

- An in-session review by default.
- Optional `<target-dir>/deep-review.md` when the user requests a durable,
  self-contained review.

## Workflow

1. Confirm the target, review question, reviewer perspective, and whether this
   is a new or continuing review. Read only current relevant artifacts.
2. Build a self-contained briefing: central question, claimed contributions,
   method, strongest evidence, negative or missing evidence, known weaknesses,
   constraints, and exact questions. Do not hide unfavorable facts.
3. Use an available independent model, agent, or reviewer service. Follow a
   user-named provider/model when available; otherwise choose an authorized
   option and identify it. If no independent reviewer capability exists, stop
   rather than presenting self-review as external review.
4. **Round 1 — broad critique:** request logical gaps, prior-work risk, missing
   evidence, methodological threats, narrative weaknesses, and the strongest
   rejection case.
5. **Round 2 — evidence challenge:** answer criticisms with exact evidence,
   contest unsupported reviewer assumptions, and ask for the minimum evidence
   that would resolve each material concern.
6. **Round 3 — decision package:** request a prioritized experiment package,
   claim-to-evidence matrix, permissible claims under plausible outcomes,
   framing options, and an optional mock review or score when useful.
7. Default to at most three rounds. Continue further only when the user asks or
   one unresolved question cannot be answered without a focused follow-up.
8. Synthesize agreements and disagreements yourself. External reviewer text is
   advice, not source evidence and not an automatic verdict.
9. Report material concerns, responses, remaining uncertainty, minimum fixes,
   estimated experiment cost, claim boundaries, and the next scientific
   decision. Preserve a non-secret session locator only when the user wants
   resumability and the provider supports it.

## Quality Bar

- The reviewer receives enough context to critique the actual work.
- Every material criticism is accepted, rebutted, or left explicitly unresolved
  with evidence.
- The final package prioritizes acceptance lift or scientific information per
  unit of cost rather than producing a generic wish list.
- Claims matrices distinguish what the current evidence supports from what
  additional outcomes would support.

## Boundaries

- Do not trigger implicitly after writing, experiments, or ordinary review
  requests.
- Do not edit the reviewed artifact, launch experiments, or update resume state
  unless separately requested.
- Do not create review loops, gate states, approval records, or reviewer votes.
- Do not send private text to an external reviewer without the applicable
  disclosure authorization.

## Open References Only As Needed

- Read `references/review-rounds.md` for briefing and follow-up prompts.
- Read `../../_shared/execution-authority.md` before transmitting private
  material or using a paid reviewer service.
- Read `../../_shared/artifact-contract.md` when durable report ownership is
  unclear.
