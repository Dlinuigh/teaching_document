\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tikz_figure}[2026/04/22 Standalone TikZ Figure Class]

% Standalone figure document for compiling single TikZ assets
\LoadClass[tikz,border=6pt]{standalone}

% Keep CJK support aligned with paper.cls, with a safe fallback
\RequirePackage{xeCJK}
\RequirePackage{fontspec}
\IfFontExistsTF{PingFang SC}{
  \setCJKmainfont{PingFang SC}
}{
  \setCJKmainfont{Songti SC}
}

\RequirePackage{amsmath}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\pgfplotsset{trig format plots=rad}

% TikZ libraries mirrored from paper.cls
\usetikzlibrary{angles,quotes}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{calc}
\usetikzlibrary{decorations}
\usetikzlibrary{decorations.markings}
\usetikzlibrary{decorations.pathmorphing}
\usetikzlibrary{fadings}
\usetikzlibrary{math}
\usetikzlibrary{patterns}
\usetikzlibrary{positioning}
\usetikzlibrary{shadows.blur}
\usetikzlibrary{shapes}
\usetikzlibrary{shapes.geometric}

\endinput
