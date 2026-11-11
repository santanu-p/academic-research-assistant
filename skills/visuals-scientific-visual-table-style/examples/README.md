# Examples

Run the smoke-test generator:

```bash
python example_openai_visuals.py --out /tmp/openai_visual_examples
```

It creates:

- a direct-labeled horizontal comparison;
- a worst-of-k reliability curve;
- a cost–performance Pareto frontier.

The data are synthetic. The examples exist to test the theme, direct labeling,
axis rules, programmatic audit, and SVG/PNG export. Inspect every generated
image at final size; successful code execution is not a substitute for visual
review.
