---
name: paper-pdf-fetcher
description: "Download a selected paper PDF into the local workspace. Use when Codex needs to fetch `source.pdf` for a paper selected from `reading-queue.md`, `paper-leads.jsonl`, an arXiv ID, DOI, or a direct paper URL. Prefer open-access sources first, and use Semantic Scholar for metadata and open PDF availability checks when helpful."
---

# Paper PDF Fetcher

## Overview
Fetch one paper into the canonical local `source.pdf` slot and record how the acquisition succeeded or failed.

## Consume
- One selected paper from `<topic-root>/synthesis/reading-queue.md`,
  `<topic-root>/synthesis/paper-leads.jsonl`, or a direct identifier such as
  arXiv ID, DOI, or Semantic Scholar paper URL.
- Optional existing `<topic-root>/papers/<paper-id>/meta.yaml` or title string
  for identifier resolution.
- Optional PaperHunter `downloaded_papers/` file when PaperHunter has already
  fetched an open PDF and the selected lead records its downloaded filename.
- Optional Semantic Scholar API key or other source-specific credentials when the user has them.

## Produce
- `<topic-root>/papers/<paper-id>/source.pdf`
- `<topic-root>/papers/<paper-id>/download-report.md`
- `<topic-root>/papers/<paper-id>/manual-fetch-needed.md` when automated
  acquisition fails for a paper that is still worth reading

## Workflow
1. Resolve `<topic-root>` using the shared artifact contract before any
   acquisition write. Stop for an explicit root if resolution fails.
2. Resolve the paper to the strongest stable identifier available before attempting any download.
3. Prefer open-access PDF URLs from Semantic Scholar, arXiv, or other direct sources; use publisher landing pages only as fallback discovery, not as a guarantee of downloadable full text.
4. Create the dedicated paper workspace at
   `<topic-root>/papers/<paper-id>/` before saving any file. Use the canonical
   paper identifier (arXiv ID, DOI slug, or ACL anthology ID) as the folder
   name. All subsequent files for this paper live inside this folder.
5. If the selected lead came from PaperHunter and already has a matching file
   under PaperHunter `downloaded_papers/`, copy that file into the canonical
   paper workspace instead of redownloading, then record the original filename
   in `download-report.md`.
6. Save the fetched or imported file as `source.pdf` in the paper workspace and verify that it is a real PDF, not an HTML error page.
7. Write `download-report.md` with the exact source used, fallback attempts, and any blockers or licensing limits if acquisition failed.
8. If the paper is still judged worth reading but automated acquisition fails, append a concrete entry to `manual-fetch-needed.md` with the paper title, stable identifier, best landing page, failure reason, and a direct note that the user should provide the PDF manually.

## Preferred Local Script

- Use `workflow/scripts/fetch_paper_pdf.py` from the Research workspace root
  when you want a repeatable acquisition path.
- It already:
  - resolves metadata via Semantic Scholar first
  - uses the approved `x-api-key`
  - respects the local `1 request/second` throttling rule
  - prefers `openAccessPdf` and arXiv fallbacks before publisher links
- Use `workflow/scripts/arxiv_fetch.py` from the Research workspace root when
  the identifier is already a clean arXiv ID and you want a lightweight direct
  fallback path.

## Quality Bar
- Preserve source provenance for the downloaded PDF.
- Verify file type before declaring success.
- Make blocked or paywalled acquisitions explicit instead of silently failing.
- When acquisition is blocked, leave the user with one concrete next action instead of a vague failure message.

## Boundaries
- Do not parse the paper body or summarize content inside this skill.
- Do not assume a Semantic Scholar API key unlocks non-open PDFs.
- Do not overwrite unrelated local PDFs without an explicit mapping to the selected paper.
- Do not silently abandon a paper that the triage step has already judged worth reading.

## Open References Only As Needed
- Review `../../_shared/artifact-contract.md` when file ownership, canonical paths, or derived artifact names are unclear.
- Review `../../_shared/language-policy.md` when the task mixes Chinese working notes with English manuscript text.
- Review `../../_shared/integrations/semantic-scholar-api.md` when you want to use Semantic Scholar to resolve metadata or open PDF availability.
- Use `workflow/scripts/arxiv_fetch.py` from the Research workspace root when
  you need an arXiv-specific fallback after the Semantic Scholar path fails or
  is unnecessary.
