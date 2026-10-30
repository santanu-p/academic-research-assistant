---
name: latex-algorithms-and-code
description: Use when typesetting an algorithm, pseudocode, or source-code listing in a LaTeX document.
---

# Algorithms and code in LaTeX

Identify the intended audience, document class, publisher template, selected engine, existing packages and whether the user needs pseudocode, executable code, or both. Read the supplied method or implementation before typesetting. Preserve the algorithm's inputs, state, order of operations, stopping conditions and output; do not turn an illustrative example into a claim that code was executed.

## Select and prepare

1. Inspect the preamble and source for an established algorithm or listing package. Use the existing conventions when they meet the request. If a new package is needed, check the actual template and build environment; avoid loading conflicting algorithm environments or silently changing the engine.
2. Choose a representation that serves the task: structured pseudocode for method logic, a listing for actual implementation, or an independently described procedure when a package is unavailable. Record any language, syntax-highlighting, shell-escape, or external-tool requirement. Do not enable shell escape or execute untrusted code solely to render a listing without the appropriate authorization.
3. Specify input and output, initialization, branching, iteration, exceptional cases, and termination. Make variable names consistent with the surrounding paper and distinguish a mathematical estimate from an observed result. If the source omits a material step, flag it instead of inventing an implementation.

## Package choices and implementation

For structured pseudocode, `algpseudocode` supplies an `algorithmic` environment; an `algorithm` float can add a caption and reference when the document class permits it. `algorithm2e` is a separate approach with its own float and keyword system. Choose one approach compatible with the class rather than loading competing definitions of the same float. Some publisher classes provide their own algorithm environment or disallow a package: follow the class documentation first. Consult [algorithmicx](https://ctan.org/pkg/algorithmicx) and [algorithm2e](https://ctan.org/pkg/algorithm2e) for supported commands and current compatibility.

For actual source code, `listings` can typeset a file or verbatim block with language settings and line numbers without requiring an external syntax highlighter. Check the installed version's support for the language and character encoding; compile and inspect non-ASCII text rather than assuming it survives unchanged. `minted` uses Pygments-based highlighting and has an external executable and distribution-specific configuration. Current minted 3 uses `latexminted`; whether restricted shell escape is sufficient depends on the installed TeX distribution and configuration. Older versions have different dependencies. Check the [minted manual](https://tug.ctan.org/macros/latex/contrib/minted/minted.pdf) for the installed version, and do not enable unrestricted shell escape merely to obtain highlighting. Use a simpler listing if the required dependencies or permissions are unavailable.

The following independent fragment illustrates the `algorithm` and `algpseudocode` combination in a compatible class; it is not a complete document or a claim of executed code:

~~~tex
% Preamble: \usepackage{algorithm} and \usepackage{algpseudocode}
\begin{algorithm}
  \caption{Count values above a threshold}\label{alg:count-above}
  \begin{algorithmic}[1]
    \Require Sequence $x$, threshold $t$
    \State $c \gets 0$
    \For{each value $v$ in $x$}
      \If{$v > t$}
        \State $c \gets c + 1$
      \EndIf
    \EndFor
    \State \Return $c$
  \end{algorithmic}
\end{algorithm}
~~~

For a separate editable source file, `\lstinputlisting[language=Python,caption={...},label={lst:sample}]{path/to/file.py}` reads that file with `listings`; replace the path and caption with real project inputs. Preserve the relative path in the delivery and verify that the file is present. For a short inline literal, `\verb|x_1|` can preserve special characters, but verbatim commands are not suitable in every macro argument. Test the actual context and use an appropriate escaped text representation where necessary. Avoid copying untrusted file content into commands or activating executable escape features in a listing.

## Integrate and verify

Place captions and stable labels where the chosen environment defines its counter. Preserve references when moving or splitting an algorithm. Check line numbering and line wrapping, indentation, special characters, and whether floating behavior obeys the venue's requirements. For supplied code, compare the rendered listing against the source; use a file reference when appropriate so the displayed version does not silently drift.

Run the project's actual build, including any explicitly authorized highlighting step. Inspect the log and render every affected page for clipping, readability, caption placement and cross-references. If compilation, fonts, dependencies, external tools or visual inspection are unavailable, deliver editable source with the precise limitation. A rendered listing does not demonstrate that the algorithm is correct or has been run.
