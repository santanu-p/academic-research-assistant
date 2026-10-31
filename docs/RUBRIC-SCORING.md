# Evidence-tracked rubric arithmetic

`tools/rubric_score.py` calculates a weighted summary from scores that a reviewer has already assigned under a supplied rubric. It never selects criteria, assigns scores, reads a manuscript, checks references, or decides whether evidence supports a rating.

Start from [`examples/rubric-review.json`](../examples/rubric-review.json), replacing every placeholder. Keep the rubric's actual wording and weights supplied by the user or other authorized source; do not add criteria or weights that were not requested.

```sh
python -X utf8 -B tools/rubric_score.py review.json
python -X utf8 -B tools/rubric_score.py review.json --output review-score.json
```

The input is UTF-8 JSON with a title, a numeric scale, and 1–200 criteria. Each criterion has a unique `id`, a `label`, a positive `weight`, and `score`. A scored criterion also requires a nonempty `evidence` note and `rationale`. Use `null` for `score` when the criterion cannot be assessed, and optionally explain why with `not_assessed_reason`. Scores are inclusive of the declared minimum and maximum. Numeric values may have up to six fractional decimal places and must be within ±1,000,000. Unknown fields, duplicate IDs, non-finite values, and malformed scales are rejected. Output paths must be new; existing files are never overwritten.

The weighted mean uses only criteria with assigned scores. The report always states the share of total rubric weight assessed. A partial mean is explicitly labeled and `complete_weighted_mean` remains null until every criterion is scored; an unassessed criterion is never silently treated as zero. Reported numeric results are rounded to six fractional decimal places. `scale_position_percent_of_scored_criteria` linearly maps the declared scale minimum to 0 and maximum to 100 for the scored-criteria mean; `complete_scale_position_percent` is set only when all criteria are scored. These values are positions on the supplied scale, not probabilities, quality guarantees, or acceptance predictions.

The tool records caller-supplied evidence notes and rationales without checking their truth or adequacy. A complete arithmetic result does not establish that the rubric is valid or that reviewers agree. Reviewers should retain manuscript version, rubric provenance, and any disagreements in their own review record. Reports can contain confidential review material; store them according to the applicable access rules.
