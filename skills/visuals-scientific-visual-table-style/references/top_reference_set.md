# Canonical OpenAI Quantitative Visual Reference Set

This is the default global few-shot set. Use Tier-1/current OpenAI references for visual language and lower-tier references only for specialized scientific form. Direct assets remain at their original hosts; this package stores links and metadata, not copied images.

| Rank | Visual | Type | Design lesson | Link | Direct asset |
|---:|---|---|---|---|---|
| 1 | Jalapeño widens the lead at previous-best TBT | Pareto-frontier comparison chart | Canonical sparse frontier chart: one decisive claim, restrained competitors, direct operating-point comparison, and a shareable exact chart anchor. | [source](https://openai.com/index/jalapeno-first-results/#chart-31bFDtnrbeUgGQ7fLMZRX4) | — |
| 2 | Agents’ Last Exam | Score–latency / model comparison | Makes capability and latency jointly legible in a compact frontier-style comparator. | [source](https://openai.com/index/gpt-5-6/#efficient-by-default-maximum-performance-on-demand) | — |
| 3 | Artificial Analysis Intelligence Index v4.1 | Score–cost–time comparison | Shows quality, monetary cost, and elapsed time together without dashboard clutter. | [source](https://openai.com/index/gpt-5-6/#efficient-by-default-maximum-performance-on-demand) | — |
| 4 | Professional | Professional benchmark table | Canonical launch-table style: grouped rows, compact model columns, clear metric direction, and sparse bolding. | [source](https://openai.com/index/gpt-5-6/#evaluations) | — |
| 5 | Append-only context | Context-management diagram | Near-monochrome structure, one accent, exact alignment, and immediate conceptual legibility. | [source](https://openai.com/index/gpt-5-6-frontier-intelligence-efficiency/#avoid-context-bloat) | [asset](https://images.ctfassets.net/kftzwdyauwt9/4Yc2D5KqZejneZPTlOtA39/9799e64403c51e214ca4c53d9c8b40ed/Append-only_context_light_desktop.svg?w=3840&q=80) |
| 6 | Figure 2: HealthBench score versus inference cost | Performance–cost frontier scatter | One of the strongest OpenAI cost-frontier references: log-cost axis, direct model labels, and connected reasoning-effort settings. | [source](https://arxiv.org/html/2505.08775v1/figures/cost_2.png) | [asset](https://arxiv.org/html/2505.08775v1/figures/cost_2.png) |
| 7 | Figure 7: worst-at-k performance up to k=16 | Reliability line chart | A simple family of monotonic curves that communicates reliability degradation immediately. | [source](https://arxiv.org/html/2505.08775v1/figures/worst.png) | [asset](https://arxiv.org/html/2505.08775v1/figures/worst.png) |
| 8 | Chain-of-thought monitorability versus pretraining scale | Scatter / trend chart | A contemporary sparse scatter with fitted trend, model-family labeling, and uncertainty context. | [source](https://openai.com/index/chain-of-thought-monitorability/#effect-of-pretraining-scale) | — |
| 9 | SEC-Bench Pro | Cost–performance chart | Canonical cyber capability frontier against API cost. | [source](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6-preview/assets/images/image21.png) | [asset](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6-preview/assets/images/image21.png) |
| 10 | Needle-in-a-haystack retrieval across context length and position | Heatmap | One of OpenAI’s strongest matrix visuals: sparse labels, perceptually ordered values, and immediate failure-region visibility. | [source](https://openai.com/index/gpt-4-1/#evaluations) | — |
| 11 | o1 performance with train-time and test-time compute | Scaling curves | Canonical OpenAI reasoning figure: two simple curves that make the scaling thesis visible in seconds. | [source](https://openai.com/index/learning-to-reason-with-llms/#evaluations) | — |
| 12 | Test-time compute scaling | Scaling curve | A clean monotonic scaling plot with each point representing a full evaluation run. | [source](https://openai.com/index/browsecomp/#test-time-compute-scaling) | — |
| 13 | Deployment simulation: rate of undesired behavior | Bar chart with uncertainty | A model-card bar/interval chart with a zero-oriented axis, concise title, and confidence intervals. | [source](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image12.png) | [asset](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image12.png) |
| 14 | First-person fairness evaluations | Grouped bar chart with intervals | An excellent contemporary grouped bar and confidence-interval reference with careful subgroup structure. | [source](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image29.png) | [asset](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image29.png) |
| 15 | Chain-of-thought controllability versus response length | Line / trend chart | A clean relationship plot with model separation and minimal annotation. | [source](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image42.png) | [asset](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6/assets/images/image42.png) |
| 16 | Figure 4: reasoning effort by price bucket | Grouped bar / line chart | A strong reference for showing a compute setting across economically meaningful task strata. | [source](https://arxiv.org/html/2502.12115v3/x4.png) | [asset](https://arxiv.org/html/2502.12115v3/x4.png) |
| 17 | Figure 1: predictable scaling of final loss | Scaling-law plot | A landmark plot tying small-run predictions to the final training run with simple log axes and a clear extrapolation. | [source](https://cdn.openai.com/papers/gpt-4.pdf#page=3) | — |
| 18 | Model deliverables judged better, as good as, or worse than expert work | Horizontal stacked bar chart | A canonical part-to-whole comparison with neutral outcome categories and direct percentages. | [source](https://openai.com/index/gdpval/#early-results) | — |
| 19 | Accuracy versus stated confidence | Calibration plot | A strong reliability diagram with an ideal diagonal and concise confidence bins. | [source](https://openai.com/index/introducing-simpleqa/#results) | — |
| 20 | Figure 6: JudgeEval F1 versus average cost | Cost–quality scatter | A compact cost/quality plot with interpretable operating points for evaluator design. | [source](https://arxiv.org/pdf/2504.01848#page=17) | — |

## Retrieval rule

For a new visual, select 2–3 references listed in this file for global visual language and 3–5 form-matched entries from `openai_visual_reference_library.jsonl`. Avoid selecting multiple near-duplicate examples from one publication unless consistency across a visual family is the object of study.

## Default anchors by form

- Pareto frontier: ranks 1, 6, and 9.
- Current benchmark comparison: ranks 2–4.
- Technical diagram: rank 5.
- Reliability/scaling: ranks 7, 11, and 12.
- Scatter/trend: ranks 8 and 15.
- Uncertainty/grouped comparison: ranks 13 and 14.
- Heatmap: rank 10.
- Calibration: rank 19.
- Economic/outcome composition: ranks 16 and 18.
- Cost–quality evaluator comparison: rank 20.
