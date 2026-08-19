# Cross-Source Literature Pattern

## Source Records

### Reference manager

Capture title, authors, year, venue, DOI/arXiv ID, collection, tags,
annotations/highlights, attachment status, and item locator. Read-only search is
the default. Export or modify records only for an exact user-requested target.

### Note store

Capture note title/path or stable locator, tags/frontmatter, the user's summary,
linked paper identifiers, and relevant outgoing links. Label these as notes, not
paper evidence.

### Local paper library

Use user-authorized paths only. Prefer existing structured Markdown and
metadata. If the library is large, rank filenames/metadata first and deeply
inspect no more than the number needed for the current decision; 20 is a useful
default ceiling unless the user asks for more.

### Public scholarly search

Use structured scholarly indexes and official paper records where available.
Search arXiv and relevant proceedings for recent work, but do not download by
default. When the user explicitly requests downloads, use the owning paper
acquisition workflow, cap the requested batch, and verify the files.

## Graceful Degradation

For each requested source report one state:

- `searched` — queried successfully;
- `unavailable` — connector or authorized path does not exist;
- `not requested` — excluded by the user or selected mode;
- `blocked` — permission, privacy, authentication, or network issue prevented
  the search.

Continue with the remaining sources unless the missing source was the only
acceptable source named by the user.

