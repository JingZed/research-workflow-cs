# Research Workflow Skills

This package contains a materialized, portable snapshot of a lightweight
research workflow: directly triggerable leaf Skills, shared artifact contracts, deterministic
helpers, catalog generation, architecture checks, and unit tests.

Read [WORKFLOW.md](WORKFLOW.md) for the complete stage-by-stage route,
including inputs, outputs, resume points, and verification commands.

The project is released under the MIT License. See `LICENSE`. Included
third-party material and its preserved license are documented in
`THIRD_PARTY_NOTICES.md` and `LICENSES/`.

## What Is Included

- `workflow/skills/`: research ideation, experiment execution, paper
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
- `WORKFLOW.md`: the complete domain-neutral workflow guide from workspace
  initialization through experiments, writing, finishing, and delivery.
- Unit tests colocated under `workflow/scripts/test_*.py`.

Private topics, experiment outputs, credentials, CCB state, infrastructure
inventory, archives, backups, and vendored PaperOrchestra code are not part of
this package.

## Create a Research Workspace

The package does not assume a discipline, topic, dataset, method, or venue.
Initialize the neutral Research root first, then create a topic only when you
have a name to supply yourself:

```bash
python workflow/scripts/init_research_workspace.py --root path/to/research
python workflow/scripts/init_research_workspace.py --root path/to/research --apply

python workflow/scripts/init_research_workspace.py \
  --root path/to/research --topic your-topic
python workflow/scripts/init_research_workspace.py \
  --root path/to/research --topic your-topic --apply
```

Without `--apply`, the command is preview-only. Root mode creates or preserves
`workflow/` and `topics/`; topic mode creates only
`topics/<your-topic>/{synthesis,ideas,papers}` and its empty
`ideas/registry.yaml`. It does not invent a topic profile, discipline, data
schema, hypothesis, experiment, or manuscript. Existing `workflow/skills/`
projections are preserved and never overwritten. Optional operational folders
such as `infrastructure/`, `deliverables/`, and `presentations/` are created
only when a later task actually needs them.

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

- No fixed Research Skill-count cap; useful capabilities are retained when
  they have a distinct trigger, output, or integration.
- Each Skill is a directly triggerable leaf capability with a distinct output
  or tool integration.
- Router, entry, standalone gate, handoff, generic state-maintenance, and
  retired meta-workflow Skills are rejected.
- `## Produce` paths define artifact ownership; duplicate owners are rejected
  except for the two explicitly shared resume artifacts.
- Skill, description, and reference files have individual maintainability
  limits; catalog-wide counts and aggregate bytes are not capped.
- Explicit-only trigger wording and
  `policy.allow_implicit_invocation: false` must agree in both directions.
- The release tree must contain no symlinks, personal absolute paths,
  credential files, cache files, or catalog paths that escape the checkout.

## Optional Integrations

- `research-lit` can use a connected reference manager such as Zotero and a
  connected or authorized local note store. These integrations are optional;
  the report states which sources were unavailable instead of claiming they
  were searched.
- Semantic Scholar helpers require `SEMANTIC_SCHOLAR_API_KEY`; keep it in the
  environment or an explicitly untracked local token file.
- MinerU conversion requires `MINERU_API_TOKEN` when the configured MinerU
  route asks for authentication. Use the token setup below; do not put a real
  token in this repository.
- PaperOrchestra is an optional backend and is not bundled. The corresponding
  Skill must remain dormant when no separate installation and local policy are
  available.
- `research-review` is explicit-only and needs an authorized independent model,
  agent, or reviewer service. If none is available, it stops rather than
  presenting self-review as an external review.
- `arxiv_fetch.py` retains its upstream MIT attribution. See
  `THIRD_PARTY_NOTICES.md` and
  `LICENSES/Auto-claude-code-research-in-sleep-MIT.txt`.

## API Token Setup

The release contains no credentials. To configure optional authenticated
integrations in a local checkout:

```bash
cp workflow/api_tokens.env.example workflow/api_tokens.env
chmod 600 workflow/api_tokens.env
```

Edit `workflow/api_tokens.env` and replace the placeholders with one
`KEY=value` entry per line. The supported entries are:

- `SEMANTIC_SCHOLAR_API_KEY` — used by the Semantic Scholar metadata helper.
- `MINERU_API_TOKEN` — used by the MinerU conversion route when authentication
  is required.

Environment variables with the same names may be used instead of the local
file. The local file is ignored by Git and must never be committed or copied
into a report. If a required key is unavailable, the helper or Skill stops and
reports the missing-key blocker explicitly; it does not silently substitute a
credential.

## Safety Boundary

The workflow distinguishes read-only inspection, routine reversible work,
noncanonical experiments, decisions that require user authority, and
destructive or public actions. Read `workflow/skills/_shared/execution-authority.md`
before launching compute, promoting canonical outputs, publishing, deleting,
or sending material externally.
