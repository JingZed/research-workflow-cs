# Language Policy

Use these defaults unless the user asks for a different language.

## By Workspace

- Topic-level `notes/`, `synthesis/`, and `ideas/` working notes default to
  Chinese.
- `<topic-root>/papers/*/summary.md`, `structure.md`,
  `claim-evidence-map.md`, `reading-questions.md`, and `notes.md` default to
  Chinese because they are reading and synthesis artifacts rather than
  manuscript text.
- `<topic-root>/papers/*/paper.md` keeps the source paper's original language
  as much as practical because it is a conversion artifact, not a rewritten
  note.
- `drafts/`, paper-facing figure specs, submission materials, and reviewer responses default to English.
- `workspace/` engineering READMEs, run registries, code comments, and paper-facing result interfaces default to English.

## Working Language

- Write triage notes, idea management notes, reading notes, and planning artifacts in Chinese.
- Preserve original paper titles, method names, metric names, dataset names, and citation strings exactly.
- Quote source text only when the exact wording matters.
- Prefer Chinese section headings in working artifacts; keep English only for technical names that the field normally uses.

## Manuscript Language

- Write `drafts/` contents, figure captions intended for paper use, submission materials, and reviewer responses in English.
- Keep paper prose precise and specific; avoid vague adjectives such as "novel", "effective", or "significant" unless backed by evidence.
- When a manuscript sentence relies on a number, keep the number and the experimental condition in the same local context.
- Treat paper-facing translations such as `translation-zh.md` as manuscript
  artifacts. Apply the same evidence and plain-language scope checks as the
  English source, while preserving field-standard English technical terms when
  appropriate.

## Mixed-Language Hygiene

- Do not translate technical names if the English form is the community standard.
- Do not mix English section headings with Chinese body text inside the same working artifact unless the file is intentionally bilingual.
- When moving from a Chinese planning artifact into an English manuscript artifact, restate the claim cleanly instead of translating line by line.
- When discussing external papers, do not imply the user authored them. Prefer phrases such as `当前文献集`, `当前种子论文集`, or `所选论文` over ambiguous second-person wording.
- If the language is ambiguous, ask for clarification only when it would materially change the output.
