% paper.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{paper}[2026/04/10 Paper for Teaching]

\LoadClass[12pt,twocolumn,a4paper]{article}

% ========== 加载宏包 ==========
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper,margin=1in]{geometry}
\RequirePackage{amsmath}
\RequirePackage{colortbl}
\RequirePackage{chemfig}
\RequirePackage[version=4]{mhchem}
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}
\RequirePackage{hhline}
\RequirePackage{lastpage}
\RequirePackage{multicol}
\RequirePackage{parskip}
\RequirePackage{seqsplit}
\RequirePackage{setspace}
\RequirePackage{tabularx}
\RequirePackage{tabulary}
\RequirePackage{titlesec}
\RequirePackage[table]{xcolor}
\RequirePackage{xeCJK}

\RequirePackage[T1]{fontenc}
\RequirePackage[most]{tcolorbox}
\RequirePackage{thmtools}
\RequirePackage{titlesec}
\RequirePackage{xcolor}
\RequirePackage{xeCJK}
\RequirePackage{soul}
\RequirePackage{enumitem}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\RequirePackage{caption}
\RequirePackage[siunitx, RPvoltages]{circuitikz}
\RequirePackage{adjustbox}

\usetikzlibrary{calc}
\usetikzlibrary{fadings}
\usetikzlibrary{patterns}
\usetikzlibrary{shadows.blur}
\usetikzlibrary{shapes}
\usetikzlibrary{decorations}
\usetikzlibrary{decorations.pathmorphing}
\usetikzlibrary{decorations.markings}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{positioning}
\usetikzlibrary{angles,quotes}
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper,margin=1in]{geometry}
\RequirePackage{amsmath}
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}
\RequirePackage{lastpage}
\RequirePackage{multicol}
\RequirePackage{parskip}
\RequirePackage{titlesec}
\RequirePackage[table]{xcolor}
\RequirePackage{xeCJK}
\RequirePackage[most]{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\RequirePackage{caption}
\RequirePackage[siunitx, RPvoltages]{circuitikz}
\RequirePackage{tabularx}
\RequirePackage{adjustbox}
\RequirePackage{ulem}
\RequirePackage{paralist}

% ========== 全局设置 ==========
\setlength{\parskip}{0.5em}
\setlist{itemsep=2pt, topsep=4pt}
\raggedbottom
\pgfplotsset{compat=1.18}
\pgfplotsset{trig format plots=rad}
\usetikzlibrary{math, arrows.meta}
\setlength{\columnseprule}{0.4pt}
\rowcolors{2}{white}{blue!10}
\renewcommand{\arraystretch}{1.5}

% ========== 颜色定义 ==========
\definecolor{keypoint-color}{RGB}{230, 240, 255}
\definecolor{formula-color}{RGB}{255, 245, 230}
\definecolor{definition-color}{RGB}{230, 255, 240}
\definecolor{problem-color}{RGB}{255, 240, 245}
\definecolor{example-color}{RGB}{245, 230, 255}
\definecolor{solution-color}{RGB}{240, 255, 245}

\newenvironment{formulatab}[1]{%
  \begin{tabularx}{\columnwidth}{XX}
    \rowcolor{blue!30}
    \multicolumn{2}{l}{\parbox[c][2.5\ht\strutbox][c]{0.9\columnwidth}{\Large #1}} \\
}{%
  \end{tabularx}%
}

% ========== 页眉页脚 ==========
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[C]{高中物理手册}
\fancyhead[R]{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

\endinput