# Writing Evidence and Style Rules

Apply these rules whenever a Skill creates or edits paper-facing prose.

## Read the Evidence First

Before writing a claim, inspect the sources that govern it:

- `experiments/results/summary.md` for measured results;
- `claim-evidence-map.md` when one exists;
- `<paper-dir>/INVARIANTS.md` for paper-wide claim boundaries;
- the current literature corpus, matrix, summaries, and `refs.bib` for
  prior-work claims.

If a required source is missing, state the limitation. Do not fill the gap from
memory.

## Check Claim-Facing Edits Directly

For edits to a title, abstract, contribution paragraph, novelty claim,
headline result, discussion interpretation, or conclusion:

1. write down in the current task the 3–5 claims the existing text makes;
2. attach each claim to its comparison, metric, condition, source, figure, or
   table;
3. make the edit;
4. compare the revised text with the same evidence and invariants;
5. fix any unsupported widening or missing evidence anchor before handoff.

This is an in-task comparison, not a new project ledger. Report the result
briefly when it materially affected the edit.

## Paper-Local Invariants

`INVARIANTS.md` belongs to one named paper candidate. Keep it small and
relationship-level:

```text
Status and candidate
Invariants
Forbidden practices
Reason for any approved change
```

An invariant may constrain scope, evaluation logic, evidence roles, or the
relationship among contributions. Update it only when new evidence or an
explicit scientific decision changes the paper’s claim structure.

Internal directives in `INVARIANTS.md` are not manuscript prose. Translate them
into clear, positive paper language.

## Plain Academic Language

- State the problem, comparison, result, and implication directly.
- Prefer common field vocabulary over invented labels and noun stacks.
- Use transitions only when they express a real logical relationship.
- Make each paragraph’s first sentence say what the paragraph establishes.
- Keep one primary job per abstract sentence.
- Explain internal protocol terms in ordinary language before using shorthand.
- Keep claims specific to the tested model, dataset, condition, or metric when
  that boundary matters.

## Express Scope Positively

Describe what the evidence does:

- `serves as a boundary test`
- `measures condition-dependent recoverability`
- `provides a label-proximal upper bound`
- `supports the claim in the tested setting`

Avoid defining the paper through defensive boilerplate such as “we do not
claim,” “not a full study,” or “should not be interpreted as.” These phrases
often make correct boundaries harder to understand.

Concrete negative findings remain valid scientific statements. Report failed
controls, null effects, ruled-out explanations, and measured limitations
plainly when the evidence supports them.

## Citation and Number Integrity

- Use only numbers present in current evidence artifacts.
- Make comparison targets and conditions recoverable from the sentence.
- Use only citation keys present in `refs.bib`.
- Verify that a cited source supports the associated claim.
- Do not use “state of the art” or equivalent superiority language without a
  direct named comparison on the relevant benchmark.

## Review and Editing

A language or scientific review is read-only by default. It reports findings
and proposed fixes. Manuscript edits begin only after the user approves them.
