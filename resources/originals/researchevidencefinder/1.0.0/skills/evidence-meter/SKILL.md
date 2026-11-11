---
name: evidence-meter
description: "Give a consensus-style verdict across studies for a yes/no research question: how many studies say yes, no, possibly or mixed, weighted by study quality, with the key papers on each side. Use when the user wants a quick verdict on what the research agrees on."
---

# Evidence Meter


## Purpose
Show at a glance where the research lands, while being honest about quality and uncertainty.

## Steps
1. Frame the question as yes or no ("Does X improve Y?").
2. Gather relevant studies through search. Aim for reviews plus a spread of primary studies.
3. Classify each study: Yes, Possibly, Mixed or No, based on its main finding.
4. Weight by quality: a large meta-analysis counts for more than a small pilot study.
5. Give the overall verdict and the confidence.

## Output format
**Question:** ...
**Evidence meter:** Yes x studies, Possibly x, Mixed x, No x (from the studies reviewed)
**Quality-weighted verdict:** Likely yes / Uncertain / Likely no, with confidence high, moderate or low.
**Top studies behind the verdict:** 3 to 6 references with one-line findings.
**Why it may not be settled:** limits, gaps, conflicts.

## Rules
- The counts describe the studies you reviewed, not the whole literature. Say how many you reviewed and how you found them.
- A simple count can mislead; always explain the quality-weighted verdict.
- Never invent studies to fill a side of the meter.
