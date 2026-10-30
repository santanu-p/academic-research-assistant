---
name: research-assistant
description: Coordinate academic research tasks, select specialist methods and explain the available local tools and their limits.
---

# Academic Research Assistant

Use this entrypoint for a broad academic task, a capability question or a handoff between research stages. For a narrow request, load the relevant specialist instead of making the user complete unrelated stages.

Begin with the intended decision or artifact. Inspect the material already available and identify the research stage, audience, discipline, format, constraints and evidence gaps. Resolve tools from the actual host inventory. Ask about a missing choice only when its answer would materially change the work.

Read [the research contract](../../docs/RESEARCH-CONTRACT.md). If local MCP is connected, use route_task or search_capabilities to locate methods, then read their files with read_resource. Otherwise read [the catalog](../../catalog/skills.json) directly. A route is guidance, not an executed investigation.

## Choose a method

| Task | Methods |
|---|---|
| Clarify a problem, question, hypothesis or possible gap | research-question |
| Select a study, framework or instrument | methodology-design |
| Find sources and obtain lawful access | literature-search |
| Check reference identity, versions and corrections | source-verification |
| Explain a paper or capture structured evidence | paper-reading; evidence-extraction |
| Judge validity or synthesize a body of work | research-appraisal; literature-review |
| Conduct a protocol-led review or quantitative synthesis | systematic-review; meta-analysis |
| Analyze observations or interpret qualitative material | statistical-analysis; qualitative-analysis |
| Develop a mechanism, formal model or verification plan | scientific-reasoning; mathematical-modeling; research-validation |
| Draft, revise or respond to criticism | manuscript-writing; academic-editing; reviewer-response |
| Coordinate a substantial review loop | adversarial-revision; research-pipeline |
| Plan a project, proposal or governance materials | research-planning; research-proposals; research-integrity |
| Select an outlet and prepare a submission | journal-submission |
| Prepare degree work or a structured academic document | thesis-preparation; document-production |
| Typeset layout, mathematics, graphics or references | tex-layout; mathematics-notation; tex-figures-tables; citations-and-bibliographies |
| Repair a build or change document format | tex-build-repair; document-conversion |
| Create teaching or professional documents | teaching-materials; professional-documents |
| Communicate through figures, talks or public prose | scientific-visuals; presentations-posters; research-communication |

The table is a starting point; it does not enumerate the whole catalog. Search the catalog for the requested operation and read a narrower specialist when it fits:

- For prose in the author's voice, use `humanizer` for general writing or `academic-humanizer` for scholarly writing. Respect a request not to use them; retain citations, claims and uncertainty.
- For a particular evidence step, look for methods such as `citation-network-search`, `legal-open-access-search`, `reference-identity-verification`, `evidence-extraction-tables` and `evidence-strength-assessment`.
- For a particular TeX artifact or repair, search the `latex-*` methods as well as the broader TeX methods. Choose the requested artifact, such as a thesis, Beamer slides, poster, PGFPlots chart, TikZ diagram, multilingual text or build repair.
- For a detailed research handoff, look for methods such as `research-workflow-coordination`, `research-brief-development`, `research-proposal-development`, `scientific-peer-review` and `reviewer-response-workflow`.

Confirm suggestions against the whole request, especially exclusions and conflicts. A keyword match is a candidate, not proof that a skill or external tool is suitable.

## Compose the work

Use only methods that contribute to the requested result. An early question may need evidence exploration before a design is defensible. A synthesis may require extraction/appraisal but no new experiment. A theoretical project may need a derivation and counterexamples rather than participants or a performance benchmark.

For a substantial task, make the dependencies visible: what evidence is available, what must be learned, what can proceed independently and what would change the conclusion. Preserve unresolved scientific issues through writing; do not silently turn them into minor presentation concerns. Keep completed, proposed and unverified work distinct.

The package's Node MCP server performs read-only discovery, routing, text access, environment reporting and local consistency checks. Optional Python helpers calculate advisory prose measures, produce figures, inspect artifacts and coordinate explicitly configured review commands. Databases, converters, compilers, model providers and authoring apps must actually be available to execute their operations.

Finish with the requested artifact, supporting provenance/reproduction details and an accurate verification statement. Identify consequential missing evidence or unavailable execution clearly. Do not claim a result was published, approved, replicated or installed in another host because its local files exist.
