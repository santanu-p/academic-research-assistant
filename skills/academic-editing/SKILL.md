---
name: academic-editing
description: Edit, proofread, translate, paraphrase, and shorten academic text while retaining technical meaning, evidence, citations, and author intent.
---

# Academic editing

Use this method for proofreading, structural editing, clarity, translation, paraphrase, or a strict word limit. Apply the [research contract](../../docs/RESEARCH-CONTRACT.md). Treat the draft as an argument with evidence, not merely a collection of sentences to make smoother.

## Define the editing contract

Determine audience, discipline, target variety of language, venue, word limit, desired edit depth, and whether tracked changes or a clean version is needed. Distinguish a proofreading request from authorization to change the argument. Identify protected material: quotations, equations, symbols, citations, figure references, proper names, numerical values, code, and markup. Preserve these unless the task includes checking or correcting them.

Read the complete relevant passage before editing individual sentences. Record its intended claim, evidence, and qualification in plain language. Flag ambiguity that could change a scientific conclusion. Resolve routine wording choices autonomously, but leave a clear query when resolving ambiguity would require inventing the author's intended result.

## Work from meaning to expression

First examine the argument: does each paragraph have a purpose, does the evidence support its topic sentence, and are transitions logically justified? Move or split material only when the requested edit depth allows it. Next improve sentence structure: put actors and actions where readers can find them, shorten unnecessary nominalizations, and separate multiple claims that need different evidence. Retain technical terms when they carry needed precision.

Then proofread agreement, articles, tense, punctuation, spelling, and consistency. There is no universal preferred sentence length, punctuation pattern, or level of formality. Choose language for the audience and genre. Context-sensitive naturalness may include varied rhythm, concrete subjects, and removal of empty emphasis; it must not disguise source borrowing, add unsupported anecdotes, or make claims about defeating authorship detectors.

Preserve the distinction between association and causation, absence of evidence and evidence of absence, hypothesis and established result, statistical and practical importance, and model prediction and observation. Do not silently strengthen “may,” “consistent with,” or “under these assumptions.” If a stronger formulation is justified by evidence, explain that substantive change separately.

## Apply the requested branch

For word reduction, count using the venue's stated convention when available. Rank content by its role in the argument. Remove duplication and expendable context first, then compress phrasing. Protect methods needed for interpretation, uncertainty, exclusions, limitations, and citation attribution. Provide the actual final count and counting convention; do not claim exact compliance from an estimate. The optional [prose metrics helper](../../tools/prose_metrics.py) can support counting once its available usage is inspected.

For translation, translate concepts and rhetorical function, not isolated words. Retain equations, citation keys, units, and names. Maintain a terminology glossary for repeated technical terms. Where a term lacks an equivalent, give a defensible translation with the original on first use. Report ambiguity or source defects rather than repairing them through invention.

For paraphrase, understand the source, set it aside, write a genuinely reorganized account, then compare meanings and retained technical phrases. Keep attribution where ideas require it. A paraphrase changes expression, not provenance. For grant or application text, preserve which achievements are completed, which are collaborative, and which are proposed; improve relevance without creating credentials or commitments.

## Deliver and verify

Return the edited passage in the requested format, a short account of meaningful changes, and unresolved author queries. When using tracked changes, ensure deletions and insertions are visible and accepted-text reading remains coherent. For TeX or other markup, compare protected tokens and compile through [build repair](../tex-build-repair/SKILL.md) when compilation is part of scope.

Perform a final semantic comparison against the original: every number, qualifier, causal claim, negation, citation relationship, and contribution statement should remain accurate. Read the clean text once without consulting edits to catch broken transitions. Separate language corrections from factual corrections and explain unverified concerns. Do not report improved readability as evidence of scientific validity.

