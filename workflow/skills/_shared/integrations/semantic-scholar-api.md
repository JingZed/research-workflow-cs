# Semantic Scholar API Integration Notes

Use this reference when Semantic Scholar is part of the acquisition path.

## What It Is Good For

- Searching papers and retrieving structured metadata.
- Looking up paper details after you already know a paper ID, title, DOI, or arXiv ID.
- Returning PDF links when an open-access PDF URL is available.
- Acting as a metadata and availability oracle before you try direct downloads from arXiv or publisher pages.

## Local Configuration

- Prefer the `SEMANTIC_SCHOLAR_API_KEY` environment variable. A local,
  untracked `workflow/api_tokens.env` may be used when the workspace explicitly
  supports it.
- Do not copy the raw key into notes, reports, or committed documentation.
- Send the key in the request header as `x-api-key`.

## Rate Limiting

- Configure throttling for the quota attached to the current API key and
  verify the provider's current policy before a large batch.
- Keep a conservative serial default, honor `429` responses, and use explicit
  backoff instead of parallel bursts.

## What It Does Not Guarantee

- It does not guarantee a downloadable PDF for every paper.
- An API key improves authentication and rate limits, but it does not unlock paywalled PDFs by itself.
- For non-open papers, treat Semantic Scholar as a metadata and outbound-link source, not as a guaranteed full-text provider.

## Practical Acquisition Order

1. Resolve the paper to a stable identifier and metadata record.
2. Ask Semantic Scholar for availability metadata and any open PDF URL.
3. If an open PDF URL exists, try that first.
4. If no open PDF exists, fall back to arXiv, publisher landing pages, author copies, or user-provided files.
5. Record the outcome in `download-report.md`, including blockers and the exact source used.

## Operational Notes

- Prefer Semantic Scholar for metadata resolution and OA availability checks, not as the only acquisition path.
- If a Semantic Scholar record points to a publisher page without a direct OA PDF, continue with the normal fallback chain.
- For repeatable scripts, centralize the header construction so the `x-api-key` and throttling logic are not duplicated ad hoc.
- The local helper script for this workspace is:
  - `workflow/scripts/semantic_scholar_client.py`
  - It centralizes `x-api-key` auth and exposes a configurable inter-request
    delay.
