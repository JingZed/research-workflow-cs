# End-to-End Research Workflow

This guide describes the complete, domain-neutral route supported by the
package. It does not choose a discipline, topic, dataset, method, or venue.
Replace placeholders such as <topic>, <idea-id>, <paper-id>, <run-id>, and
<paper-dir> with values you choose.

The arrows below are handoffs, not automatic execution. Each Skill is a
directly triggerable leaf: explicitly request the next bounded action, inspect
its output, and then decide whether to continue.

## Lifecycle at a glance

~~~mermaid
flowchart LR
    A[Research root] --> B[Topic scope]
    B --> C[Literature intake]
    C --> D[Idea and hypothesis]
    D --> E[Experiment plan]
    E --> F[Run and analyze]
    F --> G[Paper story and drafts]
    G --> H[Finish and submit]
    H --> I[Presentation or delivery]
    F -. failure or revision .-> D
    G -. evidence gap .-> C
~~~

## 1. Prepare the root and topic

From the package root, preview and then apply the neutral Research root:

~~~bash
python workflow/scripts/init_research_workspace.py --root path/to/research
python workflow/scripts/init_research_workspace.py \
  --root path/to/research --apply
~~~

When you have a topic name, create only its topic skeleton:

~~~bash
python workflow/scripts/init_research_workspace.py \
  --root path/to/research --topic <topic>
python workflow/scripts/init_research_workspace.py \
  --root path/to/research --topic <topic> --apply
~~~

The root contains workflow/ and topics/. A topic contains synthesis/, ideas/,
and papers/. Optional operational directories such as infrastructure/,
deliverables/, and presentations/ are created only when a later task needs
them.

Before substantive work, read the package AGENTS.md, the nearest topic rules,
and the active resume artifacts if they already exist. Do not copy an old topic
or idea directory as a shortcut.

## 2. Establish scope and collect literature

Use the smallest relevant subset of the literature Skills:

- research-lit provides one optional cross-source view across the Research
  corpus, connected reference managers, connected or local note stores, local
  papers, and current scholarly web sources.
- paper-discovery-fetcher collects candidate papers and can create a topic
  profile and leads file.
- paper-inbox-triage prioritizes the reading queue.
- paper-pdf-fetcher acquires one selected paper.
- paper-metadata-normalizer writes paper metadata.
- paper-to-markdown converts a source PDF when structured text is needed.
- paper-summary-writer writes one requested summary, structure, questions, or
  notes artifact.
- figure-table-extractor and claim-evidence-mapper capture visual and
  claim-level evidence when needed.
- literature-corpus-maintainer keeps the topic corpus authoritative.
- literature-matrix-builder produces a matrix, map, or gap view.
- research-team-mapper is an optional public-source mapping branch.
- citation-library-maintainer maintains the shared bibliography.

Typical topic-level outputs live under:

~~~text
topics/<topic>/synthesis/
topics/<topic>/papers/<paper-id>/
~~~

Do not create every possible sidecar by default. Choose the artifact that
answers the current question and verify it before moving on.

## 3. Turn a candidate into a research direction

Use idea-creator when the task begins with a direction rather than an existing
candidate. Its generate mode produces and filters 8–12 ideas, discovery mode
adds a bounded landscape and overlap screen, and rerank mode incorporates named
pilot evidence. Use novelty-sanity-check for a fast local-only overlap screen
and novelty-check for a current multi-source closest-work investigation.

Use idea-backlog-manager to capture or rank selected candidates, promote one
idea, or activate work that is actually starting. Promotion and activation are
explicit actions; they do not happen merely because a candidate report or
backlog entry exists.

For an active idea, use as needed:

- hypothesis-framer for a testable hypothesis;
- reproduction-planner for a target-paper reproduction;
- baseline-checklist-builder for baselines and controls;
- experiment-spec-writer for the experiment contract;
- runbook-generator for a runnable procedure.

The idea-local resume files are:

~~~text
topics/<topic>/ideas/<idea-id>/notes/CURRENT.md
topics/<topic>/ideas/<idea-id>/notes/project-state.md
~~~

Keep CURRENT.md as the short navigation card and project-state.md as the
bounded scientific snapshot. Update them only when the underlying state
materially changes.

## 4. Run, monitor, and interpret experiments

Use run-experiment to launch a named run or to record an explicitly requested
log update. It owns run-local state such as status, stdout, stderr, and
optional retry or notebook artifacts.

Use the other execution Skills only when their evidence is present:

- experiment-watchdog reports material run-state transitions;
- result-aggregator summarizes raw runs;
- results-sufficiency-review gives a claims-driven SUFFICIENT, NEEDS MORE, or
  BLOCK assessment before writing, without acting as a promotion gate;
- figure-plot-builder builds paper-ready plots;
- failure-analysis-writer analyzes material failures;
- promote-run-outputs previews or applies an exact canonical replacement.

Routine technical retries remain in the same run as attempt-N. A canonical
replacement or other effectively irreversible action requires the Skill's
preview/apply boundary and the authority required by the project rules.

## 5. Build the paper story and artifacts

Once evidence is sufficient, use the writing Skills in the order that matches
the artifact you need:

1. paper-story-framer for the evidence-backed story or contribution.
2. paper-outline-builder for a drafting-ready outline.
3. intro-problem-framer, related-work-weaver, and method-results-drafter for
   manuscript sections.
4. abstract-title-polisher for the abstract, title, and pitch.
5. conceptual-figure-builder for a figure specification, exploration, build,
   or critique.
6. claim-reference-auditor and paper-style-auditor for bounded audits.
7. targeted-critic for one requested evidence, artifact, or paper critique.
8. research-review only when explicitly requested for a multi-round independent
   external critique; it is not the default review path.
9. reviewer-response-writer for a point-by-point response.

These Skills write to drafts/, the named paper directory, or the explicit
review location they own. They do not silently promote a candidate to a
canonical manuscript.

## 6. Finish, promote, and deliver

Use paper-finish-loop status mode for a read-only diagnosis of the current
writing bottleneck, or use it to build or check one paper package. Its
submission-check mode produces a submission checklist without implying that
submission has occurred.

Use promote-paper-version only when you explicitly want to preview or apply an
exact paper replacement. Keep the rollback archive that the Skill creates.

For a standalone deck, use paper-presentation-builder; it owns the selected
presentations/<deck-id>/ output root and its optional rendered artifacts.

Final user-facing packages belong under deliverables/<task-id>/, not in build
or scratch directories.

## 7. Resume and verify

At any point, resume from files rather than chat history:

1. read the nearest AGENTS.md;
2. read notes/CURRENT.md in full;
3. open the active artifact named there;
4. read only the relevant sections of notes/project-state.md;
5. run the focused validator after a material resume-state change:

~~~bash
python -B workflow/scripts/validate_research_workflow.py \
  --idea topics/<topic>/ideas/<idea-id>
~~~

For a Skill or package change, use the proportional checks:

~~~bash
python workflow/scripts/build_research_skills.py
python workflow/scripts/sync_agents_md.py
python workflow/scripts/lint_skill_catalog.py --all
python workflow/scripts/check_public_release.py
python -m unittest discover -s workflow/scripts -p 'test_*.py'
~~~

The release package is complete when the requested artifact exists at its
owned path, the focused checks pass, and any required authority or promotion
decision has been made. A passing check does not itself authorize publication,
canonical replacement, external sending, or deletion.

## Optional integrations and boundaries

Semantic Scholar and MinerU may require locally supplied credentials. The
package includes examples and helpers, never real keys. Connected reference
managers or note stores, PaperOrchestra, independent reviewer services, and
compute infrastructure are optional external dependencies and are not bundled.
If an optional dependency is unavailable, report the lost coverage explicitly;
keep the affected branch blocked or continue with a supported alternative only
when the scientific contract still holds.
