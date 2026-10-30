# Design and review for scientific figures and tables

## Decide what readers need to see

Establish the audience, intended message, data source, target medium and final physical size. Use a table when exact values, definitions or multiple attributes need lookup; use a figure to make a pattern, relationship or distribution visible. A conceptual diagram should identify its entities and relationships without suggesting quantitative evidence. Keep source data, transformations and editable plotting or table sources with the deliverable when available.

Select an encoding suited to the data and question:

- For paired observations, show the pairing where it matters. For distributions, consider individual observations, a histogram or density, or a box or violin plot; document binning or smoothing and disclose sample size. A summary alone can conceal heterogeneity.
- For trends, use an ordered coordinate and show gaps in observations instead of interpolating them silently. Explain smoothing, interpolation, normalization and logarithmic axes. Check that a log scale is appropriate for the data, including zero and negative values.
- For spatial grids, images and heatmaps, state axes and coordinate orientation, scale and units. Choose a sequential scale for ordered magnitude and a diverging scale only when a meaningful center exists; explain clipping or saturation. Preserve pixel geometry when physical aspect ratio matters.
- For multiple panels, align comparable scales when useful, identify panels consistently and explain any differences in scale or population. Avoid implying comparability where processing or denominators differ.

Use uncertainty only as supplied or computed by a justified method. Identify the estimate, interval type, level or construction, and independent unit or sample size where needed. Distinguish observational variation, uncertainty in an estimate and numerical error. Intervals, missing values and censoring should remain visible rather than being replaced by invented values. When uncertainty is unavailable, say so rather than drawing arbitrary error bars.

## Build useful tables

Give rows and columns unambiguous labels, units in headings when shared, and an ordering that serves the comparison. Align numeric entries by decimal place where the format allows; use consistent notation and precision justified by the source or analysis. Distinguish zero, unavailable, not applicable and values below detection with defined symbols. Explain abbreviations, emphasis, significance markers, denominators and uncertainty in a note. Check totals, rounding, category alignment and source values independently, including after sorting or transposition.

Use spacing and a small number of rules to group information. If a table is too wide at the intended size, shorten labels without losing meaning, split it by a coherent dimension, or change orientation or format before shrinking text. Repeat headings on multipage tables. For accessible digital tables, retain actual text and table structure with header associations where the delivery format supports them; an image of a table is a poor substitute for selectable data.

## Accessibility and export

Use direct labels where they improve interpretation and pair color with marker shape, line style, hatching or position. Check contrast against the background and inspect in grayscale or with a color-vision simulation when feasible. Avoid relying on a legend's color swatches as the only key. Provide concise alternative text or a nearby description that states the salient relationship and relevant caveats; provide the underlying values in a table or data file when appropriate. Do not claim accessibility compliance from a visual check alone.

Use PDF or SVG for suitable line art and text when the recipient accepts vector files; use PNG, TIFF or the requested raster format for image-based workflows. Confirm font embedding or portability and any venue-specific requirements. Raster pixel dimensions must support the final printed or displayed dimensions: required pixels equal inches at final size times the required pixels per inch. Resampling an undersized image adds no measured detail. Choose lossless formats for charts and text where practical. Preserve the requested format and do not treat conversion as proof of quality.

## Review the delivered artifact

Render or open the final file in a suitable viewer at the size at which it will be used, not only in the authoring canvas. Check text, mathematical glyphs, panel labels, legends, lines and uncertainty caps for clipping, overlap and sufficient contrast. Compare axes, units, transformations, category order and plotted or tabulated values against the source; confirm captions describe encodings and conditions. Inspect each page or panel, and check a print or slide preview if that is the target. Record what was checked and any missing data, inaccessible format or unavailable inspection backend.

The optional helpers in the [API reference](api.md) cover selected plots and file checks. Their scope does not include arbitrary spreadsheet, document, interactive or image formats, statistical validity, full accessibility, or visual overlap. Use native application inspection or a suitable renderer for those formats and report any unperformed checks.
