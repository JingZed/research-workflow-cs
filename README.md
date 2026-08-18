# Research Workflow Skills

This package contains a materialized, portable snapshot of a lightweight
research workflow: 39 leaf Skills, shared artifact contracts, deterministic
helpers, catalog generation, architecture checks, and unit tests.

The project is released under the MIT License. See `LICENSE`. Included
third-party material and its preserved license are documented in
`THIRD_PARTY_NOTICES.md` and `LICENSES/`.

## What Is Included

- `workflow/skills/`: 39 research ideation, experiment execution, paper
  writing, and standalone Skills.
- `workflow/skills/_shared/`: artifact, authority, language, engineering, and
  template contracts used by the Skills.
- `workflow/scripts/build_research_skills.py`: validates Skill architecture and
  regenerates the catalog, output-owner map, and OpenAI agent metadata.
- `workflow/scripts/lint_skill_catalog.py`: checks catalog drift, references,
  retired routing surfaces, and stale workflow artifacts.
- `workflow/scripts/validate_research_workflow.py`: validates the bounded
  `notes/CURRENT.md` and `notes/project-state.md` contracts for one idea.
- `workflow/scripts/check_public_release.py`: checks portability, secret
  hygiene, materialized layout, generated metadata, and Python syntax.
- Unit tests colocated under `workflow/scripts/test_*.py`.

Private topics, experiment outputs, credentials, CCB state, infrastructure
inventory, archives, backups, and vendored PaperOrchestra code are not part of
this package.

## Quick Validation

Use Python 3.11 or newer. From the package root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python workflow/scripts/check_public_release.py
python -m unittest discover -s workflow/scripts -p 'test_*.py'
```

After changing a Skill, regenerate and verify derived metadata:

```bash
python workflow/scripts/build_research_skills.py
python workflow/scripts/sync_agents_md.py
python workflow/scripts/lint_skill_catalog.py --all
python workflow/scripts/check_public_release.py
python -m unittest discover -s workflow/scripts -p 'test_*.py'
```

Generated catalog paths remain relative in a materialized checkout. The
personal source layout may use symlink projections, but this distribution does
not require or contain them.

## Architecture Guardrails

- At most 40 Research Skills.
- Each Skill is a directly triggerable leaf capability with a distinct output
  or tool integration.
- Router, entry, standalone gate, handoff, generic state-maintenance, and
  retired meta-workflow Skills are rejected.
- `## Produce` paths define artifact ownership; duplicate owners are rejected
  except for the two explicitly shared resume artifacts.
- Skill and reference files have individual and aggregate size budgets.
- Explicit-only trigger wording and
  `policy.allow_implicit_invocation: false` must agree in both directions.
- The release tree must contain no symlinks, personal absolute paths,
  credential files, cache files, or catalog paths that escape the checkout.

## Optional Integrations

- Semantic Scholar helpers require `SEMANTIC_SCHOLAR_API_KEY`; keep it in the
  environment or an explicitly untracked local token file.
- PaperOrchestra is an optional backend and is not bundled. The corresponding
  Skill must remain dormant when no separate installation and local policy are
  available.
- `arxiv_fetch.py` retains its upstream MIT attribution. See
  `THIRD_PARTY_NOTICES.md` and
  `LICENSES/Auto-claude-code-research-in-sleep-MIT.txt`.

## Safety Boundary

The workflow distinguishes read-only inspection, routine reversible work,
noncanonical experiments, decisions that require user authority, and
destructive or public actions. Read `workflow/skills/_shared/execution-authority.md`
before launching compute, promoting canonical outputs, publishing, deleting,
or sending material externally.
