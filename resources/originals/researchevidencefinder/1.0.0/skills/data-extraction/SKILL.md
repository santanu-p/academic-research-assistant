---
name: data-extraction
description: "Extract structured data from studies into evidence tables: authors, year, country, design, sample, variables, measures, results, effect sizes and quality, ready for reviews, spreadsheets or meta-analysis. Use when the user wants findings organized."
---

# Data Extraction


## Standard extraction fields
| Field | Example |
|---|---|
| Reference | Author, year |
| Country and setting | Schools in Finland |
| Design | Cluster RCT |
| Sample | 1,240 students, ages 12 to 14 |
| Intervention or exposure | Daily 20-minute reading program |
| Comparison | Usual teaching |
| Outcome and measure | Reading score, standardized test |
| Result | +0.18 SD (95% CI 0.05 to 0.31) |
| Follow-up | 1 school year |
| Quality | Moderate risk of bias |
| Notes | Funded by program developer |

## Steps
1. Agree on the fields with the user (add or remove to fit the question).
2. Extract only what the paper reports. Write "not reported" instead of guessing.
3. Keep units and statistics exactly as reported.
4. Output as a Markdown table or CSV-style rows the user can paste into a spreadsheet.

## Tips
- For a meta-analysis, capture means, standard deviations and group sizes, or the effect size with its standard error or confidence interval.
- For qualitative studies, extract themes with a short supporting description.
