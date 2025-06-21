\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{lesson}[2025/04/19 教案模板]
\LoadClass{article}

\RequirePackage{animate}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage[version=4]{mhchem}
\RequirePackage{chemfig}
\RequirePackage{etoolbox}
\RequirePackage{fancyhdr}
\RequirePackage{fontspec}
\RequirePackage[margin=3cm,left=2cm,right=2cm,a4paper]{geometry}
\RequirePackage{graphicx}
\RequirePackage{hyperref}
\RequirePackage{mathtools}
\RequirePackage{nameref}

\RequirePackage[T1]{fontenc}
\RequirePackage[most]{tcolorbox}
\RequirePackage{thmtools}
\RequirePackage{titlesec}
\RequirePackage{xcolor}
\RequirePackage{xeCJK}

\setmainfont{Liberation Serif}
\setsansfont{Liberation Sans}
\setmonofont{Source Code Pro}
\setCJKmainfont{FandolSong}
\setCJKsansfont{FandolHei}
\setCJKmonofont{Source Code Pro}
\newCJKfontfamily[song]\songfont{FandolSong}
\newCJKfontfamily[hei]\heifont{FandolHei}
\newCJKfontfamily[kai]\kaifont{FandolKai}
\newCJKfontfamily[fs]\fsfont{FandolFang}

\titleformat{\section}{\normalfont\CJKfamily{song}\Large\bfseries}{\thesection}{1em}{}

\titleformat{\subsection}{\normalfont\CJKfamily{fs}\large\bfseries}{\thesubsection}{1em}{}

% Define custom headers and footers
\fancypagestyle{lessonstyle}{
    \fancyhf{}
    \fancyhead[L]{\leftmark}
    \fancyhead[R]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
}

% 去掉默认的缩进设定
\makeatletter
\patchcmd{\@startsection}{\@afterindentfalse}{\@afterindenttrue}{}{}
\makeatother

% 设置段落缩进量和段间距
\setlength{\parindent}{2em}
\setlength{\parskip}{0.5em}

% 考试重点样式
\tcbset{
    theory/.style={
            colback=yellow!20,
            colframe=red!75!black,
            title=考试重点,
            fonttitle=\bfseries,
            coltitle=black,
            sharp corners=south,
            boxrule=0.8mm,
            arc=2mm,
            left=2mm,
            right=2mm,
            top=1mm,
            bottom=1mm
        }
}

\newcommand{\theory}[1]{%
    \begin{tcolorbox}[theory]
        #1
    \end{tcolorbox}
}

% 定义一个方程环境

\tcbset{
    equation/.style={
            colback=green!10,
            colframe=green!75!black,
            sharp corners,
            boxrule=0.5mm,
            left=2mm,
            right=2mm,
            top=1mm,
            bottom=1mm
        }
}

\newcommand{\equations}[1]{%
    \begin{tcolorbox}[equation]
        \begin{equation*}
            #1
        \end{equation*}
    \end{tcolorbox}
}

% 定义一个彩色定理环境（带编号）
\newtcbtheorem[number within=section]{mytheorem}{定理}
{colback=blue!5!white,colframe=blue!75!black,fonttitle=\bfseries}{th}

\newcommand{\theorem}[3]{
    \begin{mytheorem}{#1}{#2}
        #3
    \end{mytheorem}
}

% 可选：定义其他类型的定理

\newtcbtheorem[number within=section]{mydefinition}{定义}
{colback=green!5!white,colframe=green!75!black,fonttitle=\bfseries}{def}

\newcommand{\definition}[3]{
    \begin{mydefinition}{#1}{#2}
    #3
    \end{mydefinition}
}

\endinput