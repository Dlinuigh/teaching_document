\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{paper}[2026/04/10 Paper for Teaching]

\LoadClass[12pt,a4paper]{article}

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
\usetikzlibrary{shapes.geometric}

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

% ========== 内容盒子 ==========
\newtcolorbox{formulanotebox}[1][]{
  colback=blue!8,
  colframe=blue!75!black,
  boxrule=1pt,
  arc=2.2mm,
  enhanced,
  before skip=10pt, after skip=10pt,
  title={\strut\textcolor{white}{\bfseries 公式注意事项}},
  fonttitle=\bfseries,
  coltitle=white,
  attach boxed title to top left={yshift=-2mm, xshift=2mm},
  boxed title style={
    enhanced,
    size=small,
    colframe=blue!75!black,
    top=0mm,
    bottom=0mm,
    left=6mm,
    right=6mm,
    arc=1.5mm,
    boxrule=0pt,
    interior style={
      left color=blue!80!black,
      right color=cyan!80!blue,
      middle color=cyan!80!blue
    }
  },
  #1
}

\newtcolorbox{keypointbox}[1][]{
  colback=teal!8,
  colframe=teal!65!black,
  boxrule=1pt,
  arc=2.2mm,
  enhanced,
  before skip=10pt, after skip=10pt,
  title={\strut\textcolor{white}{\bfseries 重点知识点}},
  fonttitle=\bfseries,
  coltitle=white,
  attach boxed title to top left={yshift=-2mm, xshift=2mm},
  boxed title style={
    enhanced,
    size=small,
    colframe=teal!65!black,
    top=0mm,
    bottom=0mm,
    left=6mm,
    right=6mm,
    arc=1.5mm,
    boxrule=0pt,
    interior style={
      left color=teal!70!black,
      right color=cyan!70!blue,
      middle color=cyan!70!blue
    }
  },
  #1
}

\newtcolorbox{casetypebox}[1][]{
  colback=orange!8,
  colframe=orange!75!black,
  boxrule=1pt,
  arc=2.2mm,
  enhanced,
  before skip=10pt, after skip=10pt,
  title={\strut\textcolor{white}{\bfseries 常见题型}},
  fonttitle=\bfseries,
  coltitle=white,
  attach boxed title to top left={yshift=-2mm, xshift=2mm},
  boxed title style={
    enhanced,
    size=small,
    colframe=orange!75!black,
    top=0mm,
    bottom=0mm,
    left=6mm,
    right=6mm,
    arc=1.5mm,
    boxrule=0pt,
    interior style={
      left color=orange!80!black,
      right color=yellow!80!orange,
      middle color=yellow!80!orange
    }
  },
  #1
}

\endinput