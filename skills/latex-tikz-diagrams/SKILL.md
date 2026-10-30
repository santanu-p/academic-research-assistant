---
name: latex-tikz-diagrams
description: Use when drawing or editing a diagram with TikZ in a LaTeX project.
---

# TikZ diagrams

Determine the diagram's purpose, required relationships, and output size before drawing. Inspect the document's engine, class, existing TikZ libraries and styles so the addition fits the project. Preserve the scientific or logical meaning of supplied sketches; mark an uncertain connection for clarification instead of inventing it.

Construct the diagram from named nodes, relative positioning and reusable styles where these improve maintainability. Specify arrow direction and labels explicitly. Keep text sizes readable at the final printed scale, distinguish line types as well as color when useful, and avoid relying on absolute coordinates for every element when content may change. Include only needed libraries and avoid overwriting shared style names.

For diagrams derived from data or a physical setup, identify the source of dimensions and units. Treat a schematic as schematic unless it is actually drawn to scale. If a figure is reused externally, keep its standalone source and required assets with the project and preserve any attribution.

Compile through the actual main document and engine, accounting for externalization or shell-escape settings already configured by the project; do not enable extra execution capabilities without authorization. Check the log, then inspect rendered affected pages for clipped bounding boxes, overlapping labels, arrowheads, contrast and layout at the intended scale. Report any unperformed build or page inspection.
