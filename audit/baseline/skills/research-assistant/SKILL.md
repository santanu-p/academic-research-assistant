---
name: research-assistant
description: Use for academic, scientific and interdisciplinary research tasks, plugin onboarding, choosing capabilities, or coordinating literature, methods, analysis, writing, LaTeX, figures, presentations, integrity and publication workflows across the complete supplied collection.
---

# Unified Academic Research Assistant

Read [the integration contract](../../docs/INTEGRATION.md) before combining components. This is the unified entrypoint; all 117 upstream skills remain separately discoverable.

## Start and route

1. Identify the requested artifact/question, discipline, stage, user level, existing evidence and relevant constraints. Read attached material first. Infer information already present; ask only for missing information that materially blocks execution, while completing independent work.
2. If available, call `route_task` with the actual task. Read every selected SKILL.md before using its instructions. `search_capabilities` exposes overlapping or specialist alternatives. Without MCP use [the complete inventory](../../docs/INVENTORY.md) and [routing catalog](../../catalog/routes.json); read relevant files using host tools. Routing is advisory and is not a substitute for judgment.
3. Select one workflow below or combine stages. Preserve the full capability set: narrower tasks can invoke any catalog skill directly. Avoid loading every skill into context at once; support resources stay available at their original full length.
4. Check actual execution dependencies before a build, calculation or external query. Call `environment_status` for presence checks, then exercise necessary tools. Read [dependencies](../../docs/DEPENDENCIES.md) and [ARMS limits](../../docs/ARMS.md). Never infer authentication or successful execution from metadata.

## Workflow handoffs

| Task | Workflow |
|---|---|
| Topic/question/gap and scholarly evidence | [Discover and synthesize](../../workflows/discover-and-synthesize.md) |
| Systematic/scoping review and meta-analysis | [Evidence review](../../workflows/evidence-review.md) |
| Quantitative, qualitative, mixed methods, modeling and reproducibility | [Design and validate](../../workflows/design-and-validate.md) |
| Proposal, grants and project management | [Plan and fund](../../workflows/plan-and-fund.md) |
| Paper, thesis, editing, LaTeX and citations | [Write and typeset](../../workflows/write-and-typeset.md) |
| Scientific plots, tables, talks and posters | [Visualize and communicate](../../workflows/visualize-and-communicate.md) |
| Journal selection, submission and review responses | [Review and publish](../../workflows/review-and-publish.md) |
| Complete ARMS pipeline and optional adversarial loop | [ARMS orchestration](../../workflows/arms-orchestration.md) |

## Combined execution

Use [reusable role instructions](../../agents/README.md) when the task benefits from distinct research responsibilities. These are portable role cards; the host may execute them sequentially or use authorized available agents. They do not register a new host agent type. Missing ARMS helpers have clearly labelled compatibility roles, not invented upstream implementations.

For each stage, record inputs, chosen skill/version, decisions, actual tool calls/results, output paths and unresolved items. Keep a claim-to-evidence ledger. Distinguish fetched primary sources, user-provided results, historical examples, analysis and proposals. Preserve uncertainty, citations, numbers, data ownership, licenses and institutional AI rules.

For manuscript editing, apply `guardrails-research-problem-mechanism-evidence` and `guardrails-compag-elsevier-paper-editing` when relevant; use `academic-humanizer` or `arms-house-style` for evidence-preserving prose, and general `humanizer` only under the scientific evidence protections. For actual LaTeX/PPTX/plots, produce editable files and run the chosen backend and rendered-output checks; state exact limits if unavailable.

## Delivery gate

- Satisfy the user's actual request with substantive artifacts, not just a plan or menu.
- Verify citations and source fidelity; flag unverified or inaccessible sources.
- Run meaningful technical checks for code/calculations and inspect rendered scientific artifacts when a render is required.
- State what ran, what passed, what is historical and what remains untested or blocked.
- Include source/code/data references and reproducible commands for technical work.
- `verify_sources` audits collection preservation when relevant. It does not validate the science.

Package help: [setup](../../docs/SETUP.md), [limitations](../../docs/LIMITATIONS.md), [inventory](../../docs/INVENTORY.md), [source mapping](../../audit/source-map.json).
