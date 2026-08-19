# Idea Evaluation Rubric

Use this rubric to keep generation broad and ranking explicit.

## Candidate Record

For each candidate capture:

- title and one-sentence question;
- falsifiable hypothesis and competing explanation;
- why either a positive or negative answer matters;
- contribution type: method, empirical finding, theory, diagnosis, benchmark,
  dataset, system, or evaluation;
- closest known work and claimed delta;
- minimum discriminating test;
- data, code, compute, time, and human-effort requirements;
- primary metric, positive threshold, informative negative outcome, and main
  confound;
- novelty, feasibility, impact, information value, and dependency risk.

## Filtering

Use `high / medium / low` judgments with one sentence of evidence rather than a
false-precision total score. Eliminate a candidate when any of these is true:

- the claimed delta is already covered by verified prior work;
- the answer would not change understanding or action;
- no fair baseline or discriminating observation exists;
- required data, rights, hardware, or infrastructure are unavailable;
- the cheapest credible test exceeds the stated budget without a smaller proxy;
- the contribution depends on hiding a known confound.

## Report Shape

1. Direction and assumptions
2. Landscape and open tensions
3. Generated candidates
4. Ranked survivors
5. Minimum pilot designs
6. Eliminated ideas and reasons
7. Recommended execution order
8. Evidence that would change the ranking

