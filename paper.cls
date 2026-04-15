\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{paper}[2026/04/10 Paper for Teaching]

\LoadClass[12pt,twocolumn,a4paper]{article}

% ========== 加载宏包 ==========
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper,margin=1in]{geometry}
\RequirePackage{amsmath}
\RequirePackage{caption}
\RequirePackage{chemfig}
\RequirePackage{colortbl}
\RequirePackage{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}
\RequirePackage{hhline}
\RequirePackage{lastpage}
\RequirePackage{multicol}
\RequirePackage{parskip}
\RequirePackage{siunitx}
\RequirePackage{seqsplit}
\RequirePackage{setspace}
\RequirePackage{soul}
\RequirePackage{tabularx}
\RequirePackage{tabulary}
\RequirePackage{titlesec}
\RequirePackage[table]{xcolor}
\RequirePackage{xeCJK}
\setCJKmainfont{PingFang SC}
\RequirePackage[most]{tcolorbox}
\RequirePackage{ulem}
\RequirePackage[version=4]{mhchem}
\RequirePackage{pgfplots}
\RequirePackage[siunitx, RPvoltages]{circuitikz}
\RequirePackage{adjustbox}

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

% ========== 全局设置 ==========
% \setlength{\parskip}{0.5em}
\raggedbottom
\pgfplotsset{compat=1.18}
\pgfplotsset{trig format plots=rad}
\usetikzlibrary{math, arrows.meta}
\setlength{\columnseprule}{0.4pt}
\rowcolors{2}{white}{blue!10}
\renewcommand{\arraystretch}{1.5}

% ========== 页眉页脚 ==========
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[C]{高中物理手册}
\fancyhead[R]{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\headheight}{14.5pt}

\endinput