"""
Algorithm Explorer — Complete Master Monograph Builder
Constructs the unified, fully self-contained `Algorithm_Explorer_Report.tex`.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

with open(PROJECT_ROOT / "src" / "algorithms" / "search.py", "r", encoding="utf-8") as f:
    SEARCH_PY_CODE = f.read()

with open(PROJECT_ROOT / "src" / "algorithms" / "sorting.py", "r", encoding="utf-8") as f:
    SORTING_PY_CODE = f.read()

def generate_report():
    out_path = PROJECT_ROOT / "Algorithm_Explorer_Report.tex"

    doc = []

    # =========================================================================
    # PREAMBLE & PACKAGES
    # =========================================================================
    doc.append(r"""\documentclass[11pt,a4paper,oneside]{report}

% ------------------------------------------------------------------------------
% Document Geometry & Page Margins
% ------------------------------------------------------------------------------
\usepackage[a4paper, top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}

% ------------------------------------------------------------------------------
% Typography & Mathematical Fonts
% ------------------------------------------------------------------------------
\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathptmx}
\usepackage{setspace}
\onehalfspacing

% ------------------------------------------------------------------------------
% Academic Color Scheme
% ------------------------------------------------------------------------------
\usepackage{xcolor}
\definecolor{primaryblue}{RGB}{0, 45, 98}
\definecolor{secondarynavy}{RGB}{24, 76, 120}
\definecolor{darkgray}{RGB}{50, 50, 50}
\definecolor{lightgray}{RGB}{245, 245, 245}
\definecolor{codebackground}{RGB}{248, 249, 250}
\definecolor{codegreen}{RGB}{34, 139, 34}
\definecolor{codegray}{RGB}{128, 128, 128}

% ------------------------------------------------------------------------------
% Graphics, Tables, & Figures
% ------------------------------------------------------------------------------
\usepackage{graphicx}
\graphicspath{{figures/}{latex/figures/}{./}}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}

% ------------------------------------------------------------------------------
% TikZ Vector Flowchart Drawing Support
% ------------------------------------------------------------------------------
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}
\tikzset{
    startstop/.style = {rectangle, rounded corners, minimum width=2.4cm, minimum height=0.7cm, text centered, draw=darkgray, fill=primaryblue!10, font=\small\bfseries},
    process/.style   = {rectangle, minimum width=2.6cm, minimum height=0.7cm, text centered, draw=darkgray, fill=secondarynavy!10, font=\small},
    decision/.style  = {diamond, minimum width=2.6cm, minimum height=0.8cm, text centered, draw=darkgray, fill=codebackground, aspect=2, font=\small},
    arrow/.style     = {thick, ->, >=stealth, color=darkgray}
}

% ------------------------------------------------------------------------------
% Running Headers & Footers
% ------------------------------------------------------------------------------
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{darkgray}Algorithm Explorer: Analytical \& Experimental Complexity}
\fancyhead[R]{\small\color{darkgray}\leftmark}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.0pt}

% ------------------------------------------------------------------------------
% Python Syntax Highlighting (Listings)
% ------------------------------------------------------------------------------
\usepackage{listings}
\lstset{
    language=Python,
    backgroundcolor=\color{codebackground},
    basicstyle=\ttfamily\footnotesize\color{black},
    keywordstyle=\bfseries\color{primaryblue},
    stringstyle=\color{codegreen},
    commentstyle=\itshape\color{codegray},
    numbers=left,
    numberstyle=\tiny\color{codegray},
    stepnumber=1,
    numbersep=8pt,
    tabsize=4,
    showspaces=false,
    showstringspaces=false,
    breaklines=true,
    breakatwhitespace=true,
    frame=single,
    rulecolor=\color{lightgray},
    captionpos=b
}

% ------------------------------------------------------------------------------
% Mathematical Theorem & Definition Environments
% ------------------------------------------------------------------------------
\theoremstyle{definition}
\newtheorem{definition}{Definition}[chapter]
\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{example}{Example}[chapter]
\newtheorem{property}{Property}[chapter]

% ------------------------------------------------------------------------------
% Hyperlinks & PDF Metadata
% ------------------------------------------------------------------------------
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=primaryblue,
    citecolor=secondarynavy,
    urlcolor=primaryblue,
    bookmarksnumbered=true,
    pdfstartview={FitH}
}

% ------------------------------------------------------------------------------
% Section & Chapter Title Formatting
% ------------------------------------------------------------------------------
\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries\color{primaryblue}}{\chaptertitlename\ \thechapter}{18pt}{\Huge}
\titleformat{\section}
  {\normalfont\Large\bfseries\color{secondarynavy}}{\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{darkgray}}{\thesubsection}{1em}{}

% ------------------------------------------------------------------------------
% Document Macros
% ------------------------------------------------------------------------------
\newcommand{\DocUniversity}{Department of Computer Science \& Information Technology}
\newcommand{\DocFaculty}{Faculty of Science and Technology}
\newcommand{\DocCourse}{Discrete Mathematics \& Algorithm Analysis (MSc IT)}
\newcommand{\DocCourseCode}{MIT-DM-301}
\newcommand{\DocTitle}{Algorithm Explorer: An Analytical and Experimental Study of Algorithms, Growth of Functions and Computational Complexity}
\newcommand{\DocShortTitle}{Algorithm Explorer}
\newcommand{\DocSubtitle}{A Rigorous Analytical and Empirical Investigation of Searching and Sorting Algorithms Grounded in Kenneth H. Rosen, Discrete Mathematics (8th Edition), Chapter 3}
\newcommand{\DocAuthor}{Student Researcher / Candidate}
\newcommand{\DocRollNumber}{202612120}
\newcommand{\DocSupervisor}{Course Instructor / Evaluator}
\newcommand{\DocAcademicYear}{2026--2027}
\newcommand{\DocSubmissionDate}{November 2026}
\newcommand{\DocDashboardTitle}{Algorithm Explorer: Interactive Algorithm Analysis \& Complexity Visualization}
\newcommand{\DocDashboardURL}{https://github.com/academic-research/algorithm-explorer}
\newcommand{\DocDashboardStatus}{Milestone M6 Completed --- Standalone Web Application Ready for Local Serving and GitHub Pages Deployment}

\begin{document}
""")

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% COVER PAGE
% ==============================================================================
\begin{titlepage}
    \centering
    \vspace*{1.0cm}
    
    {\scshape\Large \DocUniversity \par}
    \vspace{0.3cm}
    {\scshape\large \DocFaculty \par}
    \vspace{0.3cm}
    {\large \DocCourse\ (\DocCourseCode) \par}
    
    \vspace{1.5cm}
    \rule{\linewidth}{1.2pt}\\[0.4cm]
    {\huge\bfseries\color{primaryblue} \DocTitle \par}
    \vspace{0.3cm}
    {\large\itshape \DocSubtitle \par}
    \rule{\linewidth}{1.2pt}
    
    \vspace{2.0cm}
    
    \begin{minipage}{0.48\textwidth}
        \begin{flushleft} \large
            \emph{Prepared by:}\\
            \textbf{\DocAuthor}\\
            Enrollment ID: \texttt{\DocRollNumber}
        \end{flushleft}
    \end{minipage}
    ~
    \begin{minipage}{0.48\textwidth}
        \begin{flushright} \large
            \emph{Academic Evaluator:}\\
            \textbf{\DocSupervisor}\\
            Academic Year: \DocAcademicYear
        \end{flushright}
    \end{minipage}
    
    \vfill
    
    {\large Academic Term Project Report Grounded in\\
    Kenneth H. Rosen, \emph{Discrete Mathematics and Its Applications} (8th Edition), Chapter 3\par}
    \vspace{0.5cm}
    {\large \DocSubmissionDate \par}
\end{titlepage}
""")

    # =========================================================================
    # ABSTRACT & FRONT MATTER
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% ABSTRACT & FRONT MATTER
% ==============================================================================
\pagenumbering{roman}
\setcounter{page}{2}

\begin{abstract}
\noindent
This academic monograph presents a comprehensive analytical and empirical investigation into computational complexity, asymptotic growth, and algorithmic scaling. Grounded in Chapter 3 of Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (8th Edition), the study addresses the four fundamental topics established in the university curriculum: (1) \emph{What is an Algorithm?}, (2) \emph{Types and Classifications of Algorithms}, (3) \emph{The Growth of Functions}, and (4) \emph{The Complexity of Algorithms}. 

To bridge pure discrete mathematical proofs with observable computational performance, we investigate four canonical case-study algorithms: Linear Search, Binary Search, Bubble Sort (textbook fixed-pass formulation), and Insertion Sort. We derive exact closed-form operation-count formulas $T(n)$ for best-, average-, and worst-case scenarios, proving formal asymptotic classifications within $\mathcal{O}$, $\Omega$, and $\Theta$ using explicit mathematical witness pairs $(C, k)$. 

To evaluate theoretical models empirically, we constructed an isolated microbenchmarking harness executing across calibrated input scales ($n \in [100, 100\,000]$ for searching and $n \in [100, 3\,000]$ for sorting) and three fundamental topological permutations (sorted, random, and reverse-sorted). Our benchmarking methodology strictly isolates high-resolution execution timing ($\pm 100\text{ ns}$) from instrumented operation counters, incorporating statistical replication ($k = 30$ iterations), fresh input copies for in-place sorts, and sub-microsecond batch timing calibration.

The empirical results confirm that discrete operation-count formulas predict real-world algorithm behavior with \textbf{0.00\% discrepancy}. At scale ($n = 100\,000$), Binary Search delivers an empirical speedup of approximately $\mathbf{1\,946\times}$ over Linear Search for unsuccessful queries ($1.96\ \mu\text{s}$ vs. $3.82\text{ ms}$), confirming the immense power of logarithmic interval halving. Furthermore, we mathematically and empirically prove the \textbf{Inversion Equivalence Theorem}, demonstrating that Bubble Sort adjacent swaps and Insertion Sort right shifts are strictly identical ($2\,296\,691$ operations at $n = 3\,000$) on identical random permutations. Finally, we demonstrate that Insertion Sort achieves adaptive linear time $\Theta(n)$ ($0.32\text{ ms}$) on pre-sorted arrays, outperforming fixed-pass Bubble Sort ($246.25\text{ ms}$) by a factor of $\mathbf{769\times}$. All datasets, code listings, execution traces, and publication-quality figures are fully reproducible.
\end{abstract}

\vspace{0.5cm}
\noindent\textbf{Keywords}: Discrete Mathematics, Algorithm Analysis, Kenneth H. Rosen, Asymptotic Growth, Big-$\mathcal{O}$ Notation, Computational Complexity, Linear Search, Binary Search, Bubble Sort, Insertion Sort, Inversion Dynamics, Empirical Telemetry.

\clearpage

\tableofcontents
\clearpage

\listoffigures
\clearpage

\listoftables
\clearpage

\pagenumbering{arabic}
\setcounter{page}{1}
""")

    # =========================================================================
    # CHAPTER 1 — INTRODUCTION
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 1: INTRODUCTION
% ==============================================================================
\chapter{Introduction and Theoretical Framework}
\label{chap:introduction}

\section{Background of Algorithms}
The study of algorithms constitutes the foundational bedrock of computer science and discrete mathematics. The term originates historically from the Latinized surname of the ninth-century Persian mathematician Muhammad ibn M\=us\=a al-Khw\=arizm\=i, whose treatises introduced systematic procedural rules for solving algebraic and arithmetic problems. In contemporary mathematics, algorithms are conceptualized not merely as machine code or platform-dependent scripts, but as formal abstract objects governed by rigorous logical, combinatoric, and asymptotic principles.

\section{Role of Algorithms in Computer Science}
In modern computing, algorithms provide the computational mechanics by which data structures are manipulated, optimization problems are solved, and information is processed. Whether routing internet packets, indexing billions of web pages, training neural network weights, or executing secure cryptographic protocols, the efficiency and correctness of the underlying algorithm dictate the physical feasibility of computational tasks. A poorly designed algorithm running on supercomputing hardware will routinely be outperformed by an optimal algorithm running on modest hardware once input sizes grow sufficiently large.

\section{Importance of Algorithm Analysis}
Algorithm analysis provides the quantitative framework required to predict computational resource requirements—principally execution time and memory space—without requiring implementation on every conceivable hardware architecture. By evaluating algorithms mathematically as functions of input size $n$, theoretical analysis enables researchers and engineers to:
\begin{enumerate}
    \item Evaluate algorithmic performance independently of machine clock rates, operating system preemption, and memory bus bandwidth.
    \item Establish rigorous performance guarantees (ceilings and floors) across best-, average-, and worst-case input configurations.
    \item Select the optimal algorithmic strategy for a given application domain prior to resource-intensive software development.
\end{enumerate}

\section{Problem Statement}
While discrete mathematics establishes formal asymptotic bounds using Big-$\mathcal{O}$, Big-$\Omega$, and Big-$\Theta$ notations, university students and practitioners often encounter a conceptual disconnect between theoretical asymptotic curves and observed empirical execution times. Modern physical computers introduce complex architectural phenomena—such as CPU cache lines (L1/L2/L3), instruction pipelining, speculative execution, branch prediction, and memory management overhead—that can obscure pure mathematical growth. Without disciplined empirical validation, theoretical models risk appearing detached from practical computing, while purely experimental timings risk being misinterpreted due to instrumentation interference and hardware noise.

\section{Objectives of the Analytical Study}
This monograph pursues four central academic objectives:
\begin{enumerate}
    \item \textbf{Mathematical Derivation}: Derive exact closed-form operation-count formulas $T(n)$ for best-, average-, and worst-case performance across canonical searching and sorting algorithms.
    \item \textbf{Asymptotic Classification}: Formally prove asymptotic upper ($\mathcal{O}$), lower ($\Omega$), and tight ($\Theta$) bounds using explicit witness constants $(C, k)$ strictly grounded in Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (8th Edition), Chapter 3.
    \item \textbf{Empirical Microbenchmarking}: Construct an isolated, reproducible Python microbenchmarking suite that measures execution duration ($\pm 100\text{ ns}$) and operation counts across calibrated input scales without measurement distortion.
    \item \textbf{Comparative Synthesis}: Empirically validate theoretical scaling laws, verify the Inversion Equivalence Theorem, and analyze the architectural trade-offs between unconditional algorithms and precondition-dependent acceleration.
\end{enumerate}

\section{Scope of the Assignment}
The academic scope of this monograph is defined strictly by the university assignment curriculum grounded in Kenneth H. Rosen, \emph{Discrete Mathematics and Its Applications} (8th Edition), Chapter 3:
\begin{itemize}
    \item \textbf{Section 3.1: Algorithms} --- Algorithmic properties, pseudocode conventions, flowcharts, and representative searching and sorting problems.
    \item \textbf{Section 3.2: The Growth of Functions} --- Asymptotic complexity hierarchy, dominant terms, and formal definitions of Big-$\mathcal{O}$, Big-$\Omega$, and Big-$\Theta$.
    \item \textbf{Section 3.3: Complexity of Algorithms} --- Exact operation counting, space and time complexity, and comparative efficiency.
\end{itemize}
\noindent
\textbf{Note on Algorithmic Scope}: The faculty assignment explicitly identifies four foundational theoretical topics. To conduct a concrete analytical and experimental evaluation, four canonical algorithms—Linear Search, Binary Search, Bubble Sort, and Insertion Sort—were selected as representative textbook case studies. Furthermore, an optional interactive HTML5 dashboard was engineered to provide visual demonstration value, while remaining strictly supplementary to this core academic monograph.

\section{Research Questions}
This investigation is structured around five central research questions:
\begin{itemize}
    \item \textbf{RQ1 (Model Accuracy)}: Do closed-form discrete operation formulas derived mathematically from loop invariants predict instrumented operation counts with zero discrepancy?
    \item \textbf{RQ2 (Logarithmic Domination)}: Under what input scale does Binary Search's $\Theta(\log n)$ interval halving overcome Linear Search's $\Theta(n)$ sequential scan, and does pre-sorting justify the setup overhead?
    \item \textbf{RQ3 (Inversion Dynamics)}: Does empirical telemetry confirm that Bubble Sort adjacent swaps and Insertion Sort right shifts strictly equal the permutation inversion count $I(A)$ on identical random arrays?
    \item \textbf{RQ4 (Adaptive Sorting)}: How quantitatively does Insertion Sort's inner-loop early termination compare against fixed-pass Bubble Sort on pre-sorted arrays?
    \item \textbf{RQ5 (Physical Divergence)}: Where and why do physical execution times diverge from idealized discrete mathematical models due to micro-architectural factors?
\end{itemize}

\section{Methodology Overview}
Our methodology unifies formal discrete mathematical analysis with empirical telemetry:
\begin{enumerate}
    \item \textbf{Analytical Modeling}: Formulate loop invariants and step counters for each algorithm, deriving exact algebraic expressions for comparisons, swaps, and shifts.
    \item \textbf{Authoritative Implementation}: Implement each algorithm in Python 3.14.7 supporting dual execution modes: high-speed uninstrumented execution for timing and instrumented execution for telemetry.
    \item \textbf{Isolated Microbenchmarking}: Benchmark algorithms across calibrated input scales ($n \in [100, 100\,000]$ for searching; $n \in [100, 3\,000]$ for sorting) over $k = 30$ independent replications, using batch timing for sub-microsecond probes and fresh array copies for in-place sorts.
    \item \textbf{Statistical Evaluation \& Visualization}: Aggregate telemetry into robust statistics (median, mean, standard deviation, interquartile range) and synthesize dual-format publication figures and comparative tables.
\end{enumerate}

\section{Organization of the Report}
The remainder of this monograph is structured as follows:
\begin{itemize}
    \item \textbf{Chapter \ref{chap:what_is_algo}}: Establishes foundational definitions, the seven essential algorithmic properties, representation methods (pseudocode, flowcharts, source code), and correctness criteria.
    \item \textbf{Chapter \ref{chap:types_of_algo}}: Classifies computational problem categories and algorithm design paradigms, presenting a unified comparative matrix.
    \item \textbf{Chapter \ref{chap:growth_of_func}}: Analyzes the mathematical growth of functions from constant to factorial scaling, presenting numerical evaluations and asymptotic hierarchies.
    \item \textbf{Chapter \ref{chap:asymptotic_notations}}: Formalizes Big-$\mathcal{O}$, Big-$\Omega$, and Big-$\Theta$ with explicit witness proofs and geometric interpretations.
    \item \textbf{Chapter \ref{chap:complexity_of_algo}}: Examines computational complexity, best/average/worst cases, and operation counting versus wall-clock duration.
    \item \textbf{Chapter \ref{chap:case_studies}}: Delivers exhaustive analytical case studies of Linear Search, Binary Search, Bubble Sort, and Insertion Sort, complete with TikZ flowcharts, pseudocode, and Python listings.
    \item \textbf{Chapter \ref{chap:methodology}}: Details the experimental benchmarking framework, input generators, hardware telemetry, and calibration procedures.
    \item \textbf{Chapter \ref{chap:results}}: Presents the empirical benchmark findings, integrating all nine publication figures and data tables.
    \item \textbf{Chapter \ref{chap:comparative}}: Synthesizes theoretical models with empirical measurements, proving Inversion Equivalence and discussing architectural effects.
    \item \textbf{Chapter \ref{chap:conclusion}}: Concludes the study, evaluating research questions, pedagogical implications, and future research directions.
    \item \textbf{Appendices}: Provide full Python code listings, supplemental tables, execution output traces, and reproduction instructions.
\end{itemize}
""")

    # =========================================================================
    # CHAPTER 2 — WHAT IS AN ALGORITHM?
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 2: WHAT IS AN ALGORITHM?
% ==============================================================================
\chapter{What is an Algorithm?}
\label{chap:what_is_algo}

\section{Definition of an Algorithm}
In mathematical computer science, an algorithm is far more than an informal collection of computer code. Grounded in Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (§3.1) \cite{rosen2019discrete}, we state the formal mathematical definition:

\begin{definition}[Algorithm]
An \textbf{algorithm} is a finite sequence of precise instructions for performing a computation or for solving a problem.
\end{definition}

An algorithm accepts an input from a designated discrete domain, undergoes a finite sequence of deterministic, unambiguous state transitions, and halts, producing an output in a specified target domain. Crucially, an algorithm exists independently of any physical machine, compiler, or programming language: it is an abstract mathematical procedure that can be studied, proven correct, and analyzed for computational complexity using pure discrete mathematics.

\section{Characteristics of Algorithms}
To distinguish a legitimate mathematical algorithm from an incomplete procedural heuristic, an arbitrary script, or a non-terminating loop, Rosen defines seven essential properties that any valid algorithm must satisfy:

\subsection{Input}
\begin{property}[Input]
An algorithm must possess a specified set of input values taken from a well-defined domain. The input represents the problem instance to be solved. An algorithm may accept zero or more input quantities; if zero inputs are provided, the algorithm operates on predetermined constant initial states.
\end{property}

\subsection{Output}
\begin{property}[Output]
From each set of valid input values, an algorithm must produce output values taken from a specified domain. The output represents the problem's solution (e.g., a boolean decision, a located index, or an ordered sequence).
\end{property}

\subsection{Definiteness}
\begin{property}[Definiteness]
Every individual instruction or state transition within the algorithm must be defined precisely and unambiguously. There must be no room for subjective interpretation by the executing agent (whether a human mathematician or a physical processor).
\end{property}

\subsection{Correctness}
\begin{property}[Correctness]
An algorithm must be mathematically correct: it must produce the proper, expected output values for every allowable input configuration in its domain. Correctness is established through deductive logic, loop invariants, and mathematical induction rather than empirical testing alone.
\end{property}

\subsection{Finiteness}
\begin{property}[Finiteness]
An algorithm must terminate after a finite number of discrete operational steps for any valid input instance of finite size $n$. Computational procedures that enter non-terminating infinite loops fail this criterion and cannot be classified as algorithms.
\end{property}

\subsection{Effectiveness}
\begin{property}[Effectiveness]
Every operational step within the algorithm must be basic enough to be executed accurately and in a finite interval of time by a human or mechanical computing machine (e.g., basic arithmetic, pointer movement, or element comparison).
\end{property}

\subsection{Generality}
\begin{property}[Generality]
The procedure must apply generally to all problems belonging to the intended problem class, rather than functioning merely as an ad-hoc trick tailored for a specific, isolated dataset. For example, a sorting algorithm must correctly order \emph{any} finite sequence of comparable elements, not merely an array of pre-selected integers.
\end{property}

\section{Representation of Algorithms}
The specification of an algorithm can be expressed across various levels of formal abstraction:

\subsection{Natural Language Representation}
Natural language (e.g., English) provides an intuitive, highly accessible medium for communicating conceptual ideas. However, natural language is inherently vulnerable to linguistic ambiguities, syntactic vagueness, and unstated assumptions, making formal verification difficult.

\subsection{Structured Pseudocode}
Pseudocode is a high-level formal notation balancing natural language readability with rigorous mathematical control constructs (\texttt{while}, \texttt{for}, \texttt{if-then-else}). It emphasizes operational logic and data flow while abstracting away platform-specific details such as memory management, pointer arithmetic, and language syntax. Rosen adopts structured pseudocode throughout Chapter 3 as the primary medium for algorithmic discourse.

\subsection{Flowcharts}
Flowcharts provide a standardized graphical representation of algorithmic control flow. Using standardized geometric shapes (rectangles for operational tasks, diamonds for conditional branch points, and directed arrows for deterministic state transitions), flowcharts allow immediate visualization of loops, termination branches, and decision boundaries.

\subsection{Programming Language Implementation}
A programming language implementation (such as Python) translates abstract pseudocode into concrete, machine-executable source code. It enforces rigorous type signatures, index boundary checks, and concrete runtime semantics, allowing direct empirical benchmarking on physical computing platforms.

\subsection{Comparative Evaluation of Representation Methods}
Table \ref{tab:algo_representations} summarizes the comparative strengths and trade-offs of these four representation techniques.

\begin{table}[htbp]
\centering
\caption{Comparison of Algorithm Representation Techniques}
\label{tab:algo_representations}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lcccc}
\toprule
\textbf{Representation Method} & \textbf{Precision} & \textbf{Readability} & \textbf{Formal Verifiability} & \textbf{Executability} \\
\midrule
Natural Language & Low (Ambiguous) & High & Very Low & None \\
Structured Pseudocode & High & High & High & Simulated \\
Flowcharts & Medium--High & High (Visual) & Medium & Manual Trace \\
Programming Language & Absolute & Medium & High & Fully Machine-Executable \\
\bottomrule
\end{tabular*}
\end{table}

\section{Algorithm Correctness and Termination}
Establishing algorithmic correctness requires proving two distinct mathematical properties:
\begin{enumerate}
    \item \textbf{Partial Correctness}: If the algorithm terminates, it produces the mathematically correct output for all valid inputs. Partial correctness is established using \textbf{loop invariants}---predicates that remain invariant before, during, and after each loop iteration, proven via mathematical induction.
    \item \textbf{Total Correctness and Termination}: The algorithm is proven to halt in a finite number of steps on all valid inputs. Termination is established by identifying a strictly decreasing \textbf{variant function} (or loop counter) bounded below by a discrete non-negative integer (e.g., high boundary minus low boundary in Binary Search).
\end{enumerate}

\section{Independence from Programming Languages}
A vital principle emphasized by Rosen is that an algorithm is an invariant mathematical truth independent of any programming language. Linear Search remains $\Theta(n)$ and Binary Search remains $\Theta(\log n)$ whether expressed in structured pseudocode, implemented in C++, interpreted in Python, or hand-executed with pen and paper. The choice of implementation language alters constant hardware factors and interpreter overhead, but leaves fundamental asymptotic complexity classes completely unchanged.
""")

    # =========================================================================
    # CHAPTER 3 — TYPES AND CLASSIFICATION OF ALGORITHMS
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 3: TYPES AND CLASSIFICATION OF ALGORITHMS
% ==============================================================================
\chapter{Types and Classification of Algorithms}
\label{chap:types_of_algo}

\section{Introduction to Algorithm Classification}
In discrete mathematics and algorithm theory, algorithms can be classified from two distinct analytical perspectives:
\begin{enumerate}
    \item \textbf{By Problem Category}: What computational objective does the algorithm achieve?
    \item \textbf{By Design Paradigm}: What algorithmic strategy or conceptual paradigm is employed to construct the solution?
\end{enumerate}
Conflating problem categories with design paradigms is a common pedagogical error. For example, sorting is a \emph{problem category}, whereas divide-and-conquer is an \emph{algorithmic design paradigm} that can be used to solve sorting problems (Merge Sort), searching problems (Binary Search), or arithmetic problems (Karatsuba multiplication).

\section{Primary Problem Categories}
Rosen (§3.1) identifies several foundational computational problem categories:

\subsection{Searching Algorithms}
Given a collection of discrete items $S = [a_0, a_1, \dots, a_{n-1}]$ and a target value $x$, searching algorithms determine whether $x \in S$, returning its index location $i$ if present, or an indicator of absence (typically $-1$). Searching problems form the basis of information retrieval, database queries, and symbol table resolution.

\subsection{Sorting Algorithms}
Given a sequence of $n$ elements $(a_0, a_1, \dots, a_{n-1})$ from a totally ordered set, sorting algorithms generate a permutation $(a'_0, a'_1, \dots, a'_{n-1})$ such that:
$$a'_0 \le a'_1 \le a'_2 \le \dots \le a'_{n-1}$$
Sorting is among the most heavily studied problems in computer science because ordered data dramatically accelerates downstream searching, deduplication, and relational joins.

\subsection{String Matching Algorithms}
Given a text string $T$ of length $n$ and a pattern string $P$ of length $m$ ($m \le n$), string matching algorithms find all occurrences of $P$ within $T$. Classic examples include the Knuth-Morris-Pratt (KMP) and Boyer-Moore algorithms.

\subsection{Optimization Problems}
Optimization problems seek to find a configuration within a discrete feasibility space that minimizes or maximizes a designated objective function (e.g., shortest paths in graphs or minimum spanning trees).

\section{Algorithmic Design Paradigms}
Algorithms are constructed using several classical problem-solving paradigms:

\subsection{Brute-Force Approaches}
Brute-force algorithms evaluate candidate solutions exhaustively and sequentially according to the problem definition, without exploiting internal structural shortcuts. While rarely asymptotically optimal, brute-force algorithms are conceptually straightforward, widely applicable, and serve as valuable baselines. \textbf{Linear Search} is a canonical brute-force algorithm.

\subsection{Divide-and-Conquer Approaches}
Divide-and-conquer algorithms solve a problem by:
\begin{enumerate}
    \item \textbf{Divide}: Breaking the original problem into smaller, independent subproblems of the identical type.
    \item \textbf{Conquer}: Recursively or iteratively solving the smaller subproblems.
    \item \textbf{Combine}: Merging subproblem solutions into a solution for the original problem.
\end{enumerate}
By halving the search space on each iteration, \textbf{Binary Search} represents the purest iterative realization of divide-and-conquer.

\subsection{Incremental and Iterative Construction}
Incremental algorithms construct solutions one element at a time, expanding a verified partial solution by integrating the next element into its correct relative position. \textbf{Insertion Sort} is the classic archetype of this paradigm.

\subsection{Adjacent Exchange (Bubble) Approaches}
Exchange algorithms sweep through sequences, comparing and interchanging adjacent elements that violate the ordering relation until no inversions remain. \textbf{Bubble Sort} is the foundational adjacent exchange sort.

\subsection{Greedy Approaches}
Greedy algorithms construct solutions through a sequence of decision steps, making the locally optimal choice at each stage in hopes of arriving at a globally optimal solution. While greedy approaches fail for arbitrary optimization problems, they yield optimal solutions for specific discrete matroids (e.g., Huffman coding, Prim's and Kruskal's minimum spanning tree algorithms).

\section{Comparison of Problem Categories and Design Paradigms}
Table \ref{tab:algo_classification_matrix} provides a comprehensive classification matrix synthesizing problem categories, design paradigms, time complexity, and representative textbook algorithms.

\begin{table}[htbp]
\centering
\caption{Comprehensive Classification Matrix of Algorithms and Paradigms}
\label{tab:algo_classification_matrix}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lllll}
\toprule
\textbf{Problem Category} & \textbf{Algorithm} & \textbf{Design Paradigm} & \textbf{Worst-Case Time} & \textbf{Preconditions} \\
\midrule
Searching & Linear Search & Brute-Force & $\Theta(n)$ & None \\
Searching & Binary Search & Divide-and-Conquer & $\Theta(\log n)$ & Sorted Sequence \\
Sorting & Bubble Sort & Adjacent Exchange & $\Theta(n^2)$ & None \\
Sorting & Insertion Sort & Incremental Insertion & $\Theta(n^2)$ & None \\
Sorting & Merge Sort & Divide-and-Conquer & $\Theta(n \log n)$ & None \\
Sorting & Quick Sort & Divide-and-Conquer & $\Theta(n^2)$ & Pivot Selection \\
String Matching & Naive String Match & Brute-Force & $\Theta(m(n - m + 1))$ & None \\
Optimization & Dijkstra's Algorithm & Greedy & $\Theta(|V|^2)$ & Non-negative Weights \\
\bottomrule
\end{tabular*}
\end{table}

\section{Rationale for Selecting the Four Case-Study Algorithms}
To provide an in-depth analytical and experimental investigation for this university assignment, four foundational algorithms from Rosen Chapter 3 were selected:
\begin{enumerate}
    \item \textbf{Linear Search (Rosen §3.1, Algorithm 2)}: Serves as the baseline linear-time brute-force search requiring zero preconditions.
    \item \textbf{Binary Search (Rosen §3.1, Algorithm 3)}: Demonstrates the immense computational acceleration of divide-and-conquer logarithmic scaling under a strict pre-sorting precondition.
    \item \textbf{Bubble Sort (Rosen §3.1, Algorithm 4)}: Demonstrates adjacent exchange dynamics and fixed-pass comparison invariance.
    \item \textbf{Insertion Sort (Rosen §3.1, Algorithm 5)}: Demonstrates incremental construction and adaptive linear performance on nearly sorted sequences.
\end{enumerate}
Contrasting these two pairs—Linear vs. Binary Search and Bubble vs. Insertion Sort—allows rigorous mathematical comparison of asymptotic bounds, operation counting conventions, and real-world micro-architectural performance.
""")

    # =========================================================================
    # CHAPTER 4 — THE GROWTH OF FUNCTIONS
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 4: THE GROWTH OF FUNCTIONS
% ==============================================================================
\chapter{The Growth of Functions}
\label{chap:growth_of_func}

\section{Introduction to Growth of Functions}
When analyzing the computational efficiency of an algorithm, we examine how its required operations scale as the size of the input $n$ increases toward infinity. Grounded in Rosen §3.2 \cite{rosen2019discrete}, the \textbf{growth of functions} describes the mathematical rate at which a function $f(n)$ expands. In discrete mathematics, asymptotic growth enables computer scientists to classify algorithms by their scaling trajectories, focusing on orders of magnitude while abstracting away machine-specific constant coefficients and low-order terms.

\section{Input Size and Running-Time Functions}
The parameter $n$ represents the discrete size of the problem instance—such as the number of elements in a list, the number of vertices in a graph, or the number of bits in an integer. The running-time function $T(n)$ maps each positive integer $n \in \mathbb{Z}^+$ to the maximum, average, or minimum number of elementary operations required to process an input of size $n$.

\section{The Seven Canonical Complexity Classes}
Rosen (§3.2, Table 1) establishes the canonical hierarchy of standard mathematical growth functions:

\subsection{Constant Growth: $f(n) = 1$}
A function exhibits constant growth if its value remains invariant regardless of input size $n$. Algorithms with constant complexity execute the identical number of steps for $n = 10$ as for $n = 10^{12}$. Example: Accessing an array element by index ($A[0]$).

\subsection{Logarithmic Growth: $f(n) = \log_2(n)$}
Logarithmic growth occurs when an algorithm repeatedly bisects or divides the problem space by a constant factor on each step. Because $\log_2(n)$ grows exceptionally slowly, logarithmic algorithms scale effortlessly to massive datasets. Doubling the input size $n \to 2n$ increments the function by exactly one unit:
$$\log_2(2n) = \log_2(2) + \log_2(n) = 1 + \log_2(n)$$
Example: Binary Search.

\subsection{Linear Growth: $f(n) = n$}
Linear growth signifies that operations scale in direct, one-to-one proportion with input size. Doubling $n$ doubles the computational workload. Algorithms that must inspect every input item at least once belong to at least linear growth. Example: Linear Search.

\subsection{Linearithmic Growth: $f(n) = n \log_2(n)$}
Linearithmic (or quasilinear) growth arises frequently in divide-and-conquer algorithms that divide a problem of size $n$ into subproblems, solve each subproblem in logarithmic depth, and perform linear work across each level. Example: Merge Sort, Heap Sort.

\subsection{Quadratic Growth: $f(n) = n^2$}
Quadratic growth occurs typically in algorithms containing nested loops, where an outer loop iterates $n$ times and an inner loop performs work proportional to $n$. Doubling $n$ quadruples the workload ($f(2n) = 4n^2$). Example: Fixed-pass Bubble Sort, worst-case Insertion Sort.

\subsection{Polynomial Growth: $f(n) = n^b$}
Polynomial growth encompasses functions where the base is the variable $n$ and the exponent is a constant positive real number $b$ ($n^3, n^4, \dots$). In computational complexity theory, problems solvable by polynomial-time algorithms form the complexity class \textbf{P} and are classified as \emph{tractable}.

\subsection{Exponential Growth: $f(n) = 2^n$}
Exponential growth occurs when each incremental addition of a single input element doubles the total computational workload ($f(n+1) = 2 \cdot f(n)$). Exponential algorithms become computationally impossible for even modest input sizes ($n \ge 60$) and are classified as \emph{intractable}. Example: Exhaustive subset evaluation.

\subsection{Factorial Growth: $f(n) = n!$}
Factorial growth expands faster than exponential growth for $n \ge 4$. By Stirling's approximation:
$$n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n$$
Factorial algorithms arise in brute-force permutations of combinatorial optimization problems (e.g., brute-force Traveling Salesperson Problem).

\section{Numerical Comparison of Growth Functions}
Table \ref{tab:growth_evaluation_table} presents the exact numerical evaluation of these seven mathematical functions across discrete scales from $n = 1$ to $n = 1\,024$. 

\begin{table}[htbp]
\centering
\caption{Exact Numerical Evaluation of Canonical Mathematical Growth Functions}
\label{tab:growth_evaluation_table}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}rrrrrrrr}
\toprule
$n$ & \textbf{Constant} & \textbf{Logarithmic} & \textbf{Linear} & \textbf{Linearithmic} & \textbf{Quadratic} & \textbf{Exponential} & \textbf{Factorial} \\
 & $1$ & $\log_2(n)$ & $n$ & $n \log_2(n)$ & $n^2$ & $2^n$ & $n!$ \\
\midrule
1 & 1 & 0.00 & 1 & 0.00 & 1 & 2 & 1 \\
2 & 1 & 1.00 & 2 & 2.00 & 4 & 4 & 2 \\
4 & 1 & 2.00 & 4 & 8.00 & 16 & 16 & 24 \\
8 & 1 & 3.00 & 8 & 24.00 & 64 & 256 & 40\,320 \\
16 & 1 & 4.00 & 16 & 64.00 & 256 & 65\,536 & $2.09 \times 10^{13}$ \\
32 & 1 & 5.00 & 32 & 160.00 & 1\,024 & $4.29 \times 10^9$ & $2.63 \times 10^{35}$ \\
64 & 1 & 6.00 & 64 & 384.00 & 4\,096 & $1.84 \times 10^{19}$ & $1.27 \times 10^{89}$ \\
128 & 1 & 7.00 & 128 & 896.00 & 16\,384 & $3.40 \times 10^{38}$ & $3.86 \times 10^{215}$ \\
256 & 1 & 8.00 & 256 & 2\,048.00 & 65\,536 & $1.16 \times 10^{77}$ & $8.58 \times 10^{506}$ \\
512 & 1 & 9.00 & 512 & 4\,608.00 & 262\,144 & $1.34 \times 10^{154}$ & $3.07 \times 10^{1166}$ \\
1024 & 1 & 10.00 & 1\,024 & 10\,240.00 & 1\,048\,576 & $1.80 \times 10^{308}$ & $5.42 \times 10^{2639}$ \\
\bottomrule
\end{tabular*}
\end{table}

\noindent
\textbf{Critical Mathematical Clarification}: In Table \ref{tab:growth_evaluation_table}, column headers represent the exact mathematical functions $f(n)$, not asymptotic sets ($\mathcal{O}$). Big-$\mathcal{O}$ designates an asymptotic upper bound, not an exact numerical evaluation. Furthermore, finite factorials $n!$ for finite integers $n$ remain strictly finite; scientific notation is used to represent these astronomically large quantities accurately.

\section{Dominant Terms and Asymptotic Dominance}
In complex algebraic polynomial expressions, such as:
$$f(n) = 5n^3 + 120n^2 + 4500n + 98000$$
as $n \to \infty$, the highest-degree term $5n^3$ completely dominates the total magnitude. At $n = 10\,000$, $5n^3 = 5 \times 10^{12}$, while $120n^2 = 1.2 \times 10^{10}$ represents only $0.24\%$ of the total. Consequently, in asymptotic analysis, low-order terms and constant coefficients are eliminated, leaving the dominant term to establish the asymptotic classification: $f(n) = \Theta(n^3)$.

\section{Visual Interpretation of Growth Curves}
Figures \ref{fig:growth_common} and \ref{fig:growth_hierarchy} illustrate the mathematical growth curves synthesized through our analytical plotting pipeline.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.88\textwidth]{figures/figure1_common_growth_functions.pdf}
    \caption{Figure 1: Common Polynomial and Sub-Polynomial Growth Curves on a Linear Scale.}
    \label{fig:growth_common}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.88\textwidth]{figures/figure2_growth_hierarchy_log_scale.pdf}
    \caption{Figure 2: Complete Complexity Hierarchy from $\mathcal{O}(1)$ to $\mathcal{O}(n!)$ on a Semi-Logarithmic Scale.}
    \label{fig:growth_hierarchy}
\end{figure}

\subsection{Analytical Discussion of Figures 1 and 2}
In Figure \ref{fig:growth_common}, plotted on a standard linear scale, quadratic growth ($n^2$) accelerates dramatically, rapidly separating from linear ($n$), linearithmic ($n \log n$), and logarithmic ($\log n$) curves. Logarithmic growth appears virtually flat, demonstrating why logarithmic algorithms scale with unmatched efficiency. 

However, linear-scale plots cannot effectively display exponential ($2^n$) and factorial ($n!$) functions because their extreme vertical expansion forces all sub-polynomial curves to collapse against the horizontal axis. To resolve this visualization challenge without distorting mathematical reality, Figure \ref{fig:growth_hierarchy} employs a semi-logarithmic vertical scale ($\log_{10}(f(n))$). On this scale, exponential functions manifest as straight lines with constant positive slope ($\log_{10}(2^n) = n \log_{10}(2)$), while factorial growth displays an upward-curving trajectory ($\log_{10}(n!) \approx n \log_{10}(n)$), visually proving that factorial complexity decisively surpasses exponential growth.
""")

    # =========================================================================
    # CHAPTER 5 — ASYMPTOTIC NOTATIONS
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 5: ASYMPTOTIC NOTATIONS
% ==============================================================================
\chapter{Asymptotic Notations: Big-O, Big-Omega, Big-Theta}
\label{chap:asymptotic_notations}

\section{Introduction to Asymptotic Notations}
Asymptotic notation provides the formal mathematical language used to describe the limiting behavior of functions as their arguments approach infinity. Grounded in Rosen §3.2 \cite{rosen2019discrete}, asymptotic notations characterize the efficiency of algorithms by establishing asymptotic upper bounds (Big-$\mathcal{O}$), asymptotic lower bounds (Big-$\Omega$), and asymptotically tight bounds (Big-$\Theta$).

\section{Formal Mathematical Definitions}
We present the formal definitions utilizing precise mathematical quantifiers and inequalities:

\begin{definition}[Big-$\mathcal{O}$ Notation: Asymptotic Upper Bound]
Let $f$ and $g$ be functions from the set of integers or real numbers to the set of real numbers. We write:
$$f(n) = \mathcal{O}(g(n))$$
if and only if there exist positive real constants $C$ and $k$ such that:
$$|f(n)| \le C |g(n)| \quad \text{for all } n > k$$
The constants $C$ and $k$ are called \textbf{witnesses} to the relationship $f(n) = \mathcal{O}(g(n))$. Geometrically, $C g(n)$ serves as an asymptotic ceiling that upper-bounds $f(n)$ for all sufficiently large $n$.
\end{definition}

\begin{definition}[Big-$\Omega$ Notation: Asymptotic Lower Bound]
Let $f$ and $g$ be functions from the set of integers or real numbers to the set of real numbers. We write:
$$f(n) = \Omega(g(n))$$
if and only if there exist positive real constants $C$ and $k$ such that:
$$|f(n)| \ge C |g(n)| \quad \text{for all } n > k$$
Geometrically, $C g(n)$ serves as an asymptotic floor that lower-bounds $f(n)$ for all sufficiently large $n$.
\end{definition}

\begin{definition}[Big-$\Theta$ Notation: Asymptotically Tight Bound]
Let $f$ and $g$ be functions from the set of integers or real numbers to the set of real numbers. We write:
$$f(n) = \Theta(g(n))$$
if and only if $f(n) = \mathcal{O}(g(n))$ and $f(n) = \Omega(g(n))$. Equivalently, there exist positive real constants $C_1$, $C_2$, and $k$ such that:
$$C_1 |g(n)| \le |f(n)| \le C_2 |g(n)| \quad \text{for all } n > k$$
When $f(n) = \Theta(g(n))$, we say that $f$ is of the \textbf{order} of $g$, or that $f(n)$ is bounded tightly by $g(n)$ from both above and below.
\end{definition}

\section{Worked Mathematical Proofs with Witnesses}
To demonstrate the formal construction of witness pairs $(C, k)$, we provide three complete mathematical proofs:

\begin{example}[Witness Proof for Quadratic Function]
Prove that $f(n) = 3n^2 + 5n + 2$ is $\Theta(n^2)$.
\begin{proof}
To establish $f(n) = \Theta(n^2)$, we must find positive constants $C_1, C_2$ and $k$ such that:
$$C_1 n^2 \le 3n^2 + 5n + 2 \le C_2 n^2 \quad \text{for all } n > k$$

\textbf{Step 1: Establishing the Upper Bound ($f(n) = \mathcal{O}(n^2)$)}.\\
For all $n \ge 1$, we observe that $5n \le 5n^2$ and $2 \le 2n^2$. Therefore:
$$f(n) = 3n^2 + 5n + 2 \le 3n^2 + 5n^2 + 2n^2 = 10n^2$$
Thus, selecting witness constant $C_2 = 10$ and threshold $k_1 = 1$, we have $|f(n)| \le 10n^2$ for all $n > 1$. Hence, $f(n) = \mathcal{O}(n^2)$.

\textbf{Step 2: Establishing the Lower Bound ($f(n) = \Omega(n^2)$)}.\\
Since $n > 0$, $5n > 0$ and $2 > 0$. Therefore:
$$f(n) = 3n^2 + 5n + 2 \ge 3n^2$$
Thus, selecting witness constant $C_1 = 3$ and threshold $k_2 = 1$, we have $|f(n)| \ge 3n^2$ for all $n > 1$. Hence, $f(n) = \Omega(n^2)$.

\textbf{Conclusion}: Combining both inequalities for threshold $k = \max(k_1, k_2) = 1$:
$$3n^2 \le 3n^2 + 5n + 2 \le 10n^2 \quad \text{for all } n > 1$$
With witness constants $C_1 = 3$, $C_2 = 10$, and $k = 1$, we conclude that $f(n) = \Theta(n^2)$.
\end{proof}
\end{example}

\begin{example}[Witness Proof for Linear Function]
Prove that $f(n) = 5n + 3$ is $\Theta(n)$.
\begin{proof}
For all $n \ge 1$:
$$3 \le 3n \implies 5n + 3 \le 5n + 3n = 8n$$
Thus, choosing $C_2 = 8$ and $k_1 = 1$, $f(n) \le 8n$, proving $f(n) = \mathcal{O}(n)$.
Conversely, since $3 > 0$:
$$5n + 3 \ge 5n$$
Thus, choosing $C_1 = 5$ and $k_2 = 1$, $f(n) \ge 5n$, proving $f(n) = \Omega(n)$.
Combining with $k = 1$, $C_1 = 5$, and $C_2 = 8$:
$$5n \le 5n + 3 \le 8n \quad \text{for all } n > 1$$
Therefore, $f(n) = \Theta(n)$.
\end{proof}
\end{example}

\begin{example}[Witness Proof for Factorial Logarithm]
Prove that $f(n) = \log_2(n!)$ is $\Theta(n \log_2 n)$.
\begin{proof}
By expanding the factorial logarithm:
$$\log_2(n!) = \sum_{i=1}^n \log_2(i)$$
\textbf{Upper bound}: Since each term $\log_2(i) \le \log_2(n)$ for $1 \le i \le n$:
$$\log_2(n!) = \sum_{i=1}^n \log_2(i) \le \sum_{i=1}^n \log_2(n) = n \log_2(n)$$
Thus, $C_2 = 1$ and $k_1 = 1$ establish that $\log_2(n!) = \mathcal{O}(n \log_2 n)$.

\textbf{Lower bound}: For $n \ge 2$, discarding the first $\lfloor n/2 \rfloor$ terms:
$$\log_2(n!) \ge \sum_{i=\lceil n/2 \rceil}^n \log_2(i) \ge \sum_{i=\lceil n/2 \rceil}^n \log_2\left(\frac{n}{2}\right) = \frac{n}{2} \left(\log_2(n) - 1\right)$$
For $n \ge 4$, $\log_2(n) - 1 \ge \frac{1}{2}\log_2(n)$. Therefore:
$$\log_2(n!) \ge \frac{n}{2} \cdot \frac{1}{2}\log_2(n) = \frac{1}{4} n \log_2(n)$$
Thus, $C_1 = 0.25$ and $k_2 = 4$ establish that $\log_2(n!) = \Omega(n \log_2 n)$.
Consequently, $\log_2(n!) = \Theta(n \log_2 n)$.
\end{proof}
\end{example}

\section{Comparison of Asymptotic Notations}
Table \ref{tab:asymptotic_summary} summarizes the three primary asymptotic notations.

\begin{table}[htbp]
\centering
\caption{Mathematical Comparison of Asymptotic Notations}
\label{tab:asymptotic_summary}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}llll}
\toprule
\textbf{Notation} & \textbf{Formal Witness Condition} & \textbf{Intuitive Meaning} & \textbf{Relational Analogy} \\
\midrule
$f(n) = \mathcal{O}(g(n))$ & $\exists C, k > 0 : |f(n)| \le C |g(n)|, \forall n > k$ & Upper Bound (Ceiling) & $f \le g$ \\
$f(n) = \Omega(g(n))$ & $\exists C, k > 0 : |f(n)| \ge C |g(n)|, \forall n > k$ & Lower Bound (Floor) & $f \ge g$ \\
$f(n) = \Theta(g(n))$ & $\exists C_1, C_2, k > 0 : C_1 |g(n)| \le |f(n)| \le C_2 |g(n)|, \forall n > k$ & Tight Bound (Order) & $f = g$ \\
\bottomrule
\end{tabular*}
\end{table}

\section{Common Misinterpretations of Asymptotic Notations}
Several prevalent misconceptions must be rigorously avoided:
\begin{enumerate}
    \item \textbf{Conflating Big-$\mathcal{O}$ with Worst-Case Complexity}: Big-$\mathcal{O}$ is an asymptotic upper-bounding operator, not an execution scenario. An algorithm has a best-case time complexity, an average-case time complexity, and a worst-case time complexity. Each of these three distinct functions can be independently bounded using $\mathcal{O}, \Omega,$ or $\Theta$. For example, Linear Search's \emph{best-case} complexity is $\Theta(1)$, while its \emph{worst-case} complexity is $\Theta(n)$.
    \item \textbf{Assuming Big-$\mathcal{O}$ Implies Tightness}: Saying $f(n) = \mathcal{O}(n^3)$ does not imply $f(n)$ grows cubically; a linear function $f(n) = 5n$ is mathematically in $\mathcal{O}(n^3)$, though $\Theta(n)$ is its tight bound.
    \item \textbf{Ignoring Witness Threshold $k$}: Asymptotic dominance applies solely for $n > k$. For small inputs ($n \le k$), an algorithm with worse asymptotic complexity may execute faster due to smaller constant factors.
\end{enumerate}
""")

    # =========================================================================
    # CHAPTER 6 — COMPLEXITY OF ALGORITHMS
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 6: COMPLEXITY OF ALGORITHMS
% ==============================================================================
\chapter{Complexity of Algorithms}
\label{chap:complexity_of_algo}

\section{Introduction to Complexity Analysis}
Algorithm complexity analysis investigates the resource consumption of an algorithm as a function of input size $n$. Grounded in Rosen §3.3 \cite{rosen2019discrete}, complexity analysis provides the mathematical foundation for evaluating algorithmic feasibility, scalability, and efficiency.

\section{Time Complexity}
Time complexity analyzes the number of elementary operations executed by an algorithm. Rather than measuring elapsed seconds on a specific CPU, time complexity counts discrete operational steps—such as key comparisons, variable assignments, bitwise shifts, or arithmetic evaluations—expressed as a function $T(n)$.

\section{Space and Auxiliary Space Complexity}
Space complexity measures the total physical memory consumed by an algorithm during execution. In modern algorithm analysis, computer scientists distinguish:
\begin{itemize}
    \item \textbf{Total Space Complexity}: The total memory required, including space allocated for storing the input data itself.
    \item \textbf{Auxiliary Space Complexity}: The extra or temporary memory allocated by the algorithm \emph{beyond} the input data storage.
\end{itemize}
An algorithm is defined as \textbf{in-place} if its auxiliary space complexity is $\Theta(1)$ (i.e., bounded by a constant independent of $n$). All four algorithms evaluated in this monograph (Linear Search, Binary Search, Bubble Sort, Insertion Sort) operate in-place with $\Theta(1)$ auxiliary memory.

\section{Best-Case, Average-Case, and Worst-Case Analysis}
Because an algorithm's operational count frequently depends on the specific arrangement or permutation of input data, complexity analysis evaluates three canonical scenarios:

\subsection{Best-Case Analysis}
Let $\mathcal{D}_n$ denote the set of all allowable input instances of size $n$. The best-case complexity $T_{\text{best}}(n)$ is the minimum number of operations executed across all inputs in $\mathcal{D}_n$:
$$T_{\text{best}}(n) = \min_{I \in \mathcal{D}_n} T(I)$$
Best-case analysis identifies ideal operating conditions (e.g., target located at index 0 in Linear Search, or an already sorted array in Insertion Sort).

\subsection{Worst-Case Analysis}
The worst-case complexity $T_{\text{worst}}(n)$ is the maximum number of operations executed across all inputs of size $n$:
$$T_{\text{worst}}(n) = \max_{I \in \mathcal{D}_n} T(I)$$
Worst-case analysis provides an absolute upper bound guarantee, ensuring that the algorithm will never exceed this resource consumption regardless of input permutation.

\subsection{Average-Case Analysis}
The average-case complexity $T_{\text{avg}}(n)$ is the expected number of operations executed over a specified probability distribution $P(I)$ across all inputs $I \in \mathcal{D}_n$:
$$T_{\text{avg}}(n) = \mathbb{E}[T(I)] = \sum_{I \in \mathcal{D}_n} P(I) \cdot T(I)$$
Under the standard uniform distribution assumption, every input permutation or target position is assumed to be equally likely.

\section{Operation Counting Methodology}
To ensure rigorous mathematical fidelity, our analytical framework decomposes execution into distinct operation classes:
\begin{enumerate}
    \item \textbf{Key Comparisons}: Explicit equality or relational tests between input elements and target keys (or between adjacent elements).
    \item \textbf{Loop Evaluations}: Evaluations of loop boundary conditions (e.g., \texttt{while i <= n} or \texttt{low <= high}).
    \item \textbf{Data Movements}: Physical register assignments, adjacent swaps, or rightward array shifts.
\end{enumerate}

\section{Theoretical Complexity vs. Actual Execution Time}
While theoretical operation counts $T(n)$ scale deterministically according to discrete mathematical formulas, physical wall-clock duration $t_{\text{phys}}$ is governed by:
$$t_{\text{phys}} = T(n) \cdot \tau_{\text{cycle}} \cdot \text{CPI} + t_{\text{overhead}}$$
where $\tau_{\text{cycle}}$ is the CPU clock period, $\text{CPI}$ is the average cycles per instruction, and $t_{\text{overhead}}$ represents runtime environment and OS scheduling latency. Micro-architectural factors—such as CPU cache misses, branch mispredictions, and Python bytecode interpretation—introduce minor non-linearities into empirical runtimes.
""")

    # =========================================================================
    # CHAPTER 7 — DETAILED ALGORITHM CASE STUDIES
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 7: DETAILED CASE STUDIES OF FOUR CANONICAL ALGORITHMS
% ==============================================================================
\chapter{Detailed Case Studies of Four Canonical Algorithms}
\label{chap:case_studies}

In accordance with Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (§3.1 and §3.3) \cite{rosen2019discrete}, we present exhaustive analytical and empirical case studies of four foundational algorithms.

% ------------------------------------------------------------------------------
% 7.1 LINEAR SEARCH
% ------------------------------------------------------------------------------
\section{Linear Search (Rosen §3.1, Algorithm 2)}
\label{sec:linear_search}

\subsection{Problem Statement and Objective}
Given a sequence of $n$ elements $S = [a_0, a_1, \dots, a_{n-1}]$ and a target key $x$, determine the index $i$ of the first occurrence of $x$ in $S$. If $x \notin S$, return $-1$.

\subsection{Input and Output}
\begin{itemize}
    \item \textbf{Input}: A sequence of comparable elements $S$ of size $n \ge 0$, and target key $x$.
    \item \textbf{Output}: An integer index $i \in \{0, 1, \dots, n-1\}$ such that $S[i] == x$, or $-1$ if $x$ is absent.
\end{itemize}

\subsection{Working Principle}
Linear Search sequentially inspects elements from index $0$ to $n-1$, testing equality $S[i] == x$ at each position. The search terminates immediately upon locating a matching element or halts with failure when the sequence boundary is reached. It requires zero preconditions on element ordering.

\subsection{Step-by-Step Sample Trace}
Given $S = [15, 23, 7, 42, 19]$ and target $x = 42$:
\begin{enumerate}
    \item \textbf{Index 0}: Compare $S[0] = 15$ with $42$. $15 \neq 42$. Continue. (Comparison 1)
    \item \textbf{Index 1}: Compare $S[1] = 23$ with $42$. $23 \neq 42$. Continue. (Comparison 2)
    \item \textbf{Index 2}: Compare $S[2] = 7$ with $42$. $7 \neq 42$. Continue. (Comparison 3)
    \item \textbf{Index 3}: Compare $S[3] = 42$ with $42$. $42 == 42$. Target matched! Return index $3$. (Comparison 4)
\end{enumerate}
Total key comparisons: $4$.

\subsection{Pseudocode (Rosen §3.1, Algorithm 2)}
\begin{lstlisting}[caption={Pseudocode: Linear Search (Rosen §3.1, Algorithm 2)}]
procedure linear_search(x: integer, a1, a2, ..., an: integers)
    i := 1
    while (i <= n and x != a_i)
        i := i + 1
    if i <= n then location := i
    else location := 0
    return location
\end{lstlisting}

\subsection{Flowchart Representation}
Figure \ref{fig:flowchart_linear} presents the deterministic control logic of Linear Search.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.5cm]
    \node (start) [startstop] {Start};
    \node (init) [process, below of=start] {$i \leftarrow 0$};
    \node (dec1) [decision, below of=init, yshift=-0.4cm] {$i < n$?};
    \node (dec2) [decision, right of=dec1, xshift=2.5cm] {$S[i] == x$?};
    \node (inc) [process, below of=dec2, yshift=-0.4cm] {$i \leftarrow i + 1$};
    \node (found) [startstop, right of=dec2, xshift=2.2cm] {Return $i$};
    \node (notfound) [startstop, below of=dec1, yshift=-1.8cm] {Return $-1$};

    \draw [arrow] (start) -- (init);
    \draw [arrow] (init) -- (dec1);
    \draw [arrow] (dec1) -- node[anchor=south] {Yes} (dec2);
    \draw [arrow] (dec1) -- node[anchor=east] {No} (notfound);
    \draw [arrow] (dec2) -- node[anchor=south] {Yes} (found);
    \draw [arrow] (dec2) -- node[anchor=east] {No} (inc);
    \draw [arrow] (inc) -| (dec1);
\end{tikzpicture}
\caption{Vector Flowchart of the Linear Search Algorithm.}
\label{fig:flowchart_linear}
\end{figure}

\subsection{Authoritative Python Implementation}
Listing \ref{lst:linear_search_code} extracts the authoritative source implementation from \texttt{src/algorithms/search.py}.

\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Linear Search}, label={lst:linear_search_code}]
def linear_search(seq: Sequence[Any], target: Any) -> int:
    for index, item in enumerate(seq):
        if item == target:
            return index
    return -1

def linear_search_instrumented(seq: Sequence[Any], target: Any) -> tuple[int, SearchMetrics]:
    n = len(seq)
    key_comparisons = 0
    equality_comparisons = 0
    loop_evaluations = 0

    for index in range(n):
        loop_evaluations += 1
        equality_comparisons += 1
        key_comparisons += 1
        if seq[index] == target:
            return index, SearchMetrics(
                key_comparisons=key_comparisons,
                equality_comparisons=equality_comparisons,
                ordering_comparisons=0,
                loop_evaluations=loop_evaluations,
            )

    loop_evaluations += 1
    return -1, SearchMetrics(
        key_comparisons=key_comparisons,
        equality_comparisons=equality_comparisons,
        ordering_comparisons=0,
        loop_evaluations=loop_evaluations,
    )
\end{lstlisting}

\subsection{Actual Execution Output}
Executing \texttt{linear\_search\_instrumented} on sample $S = [15, 23, 7, 42, 19]$ yields:
\begin{verbatim}
Case: First Element (x=15) -> Index:  0, Key Comparisons: 1, Loop Checks: 1
Case: Middle Element(x=7)  -> Index:  2, Key Comparisons: 3, Loop Checks: 3
Case: Last Element  (x=19) -> Index:  4, Key Comparisons: 5, Loop Checks: 5
Case: Missing Target(x=99) -> Index: -1, Key Comparisons: 5, Loop Checks: 6
\end{verbatim}

\subsection{Mathematical Complexity Derivation}
\begin{itemize}
    \item \textbf{Best-Case Comparisons}: When target is at index $0$, $C_{\text{best}}(n) = 1 = \Theta(1)$.
    \item \textbf{Worst-Case Comparisons}: When target is at index $n-1$ or absent, $C_{\text{worst}}(n) = n = \Theta(n)$.
    \item \textbf{Average-Case Comparisons}: Under uniform distribution $P(x = S[i]) = 1/n$:
    $$C_{\text{avg}}(n) = \sum_{i=1}^n i \cdot \frac{1}{n} = \frac{1}{n} \frac{n(n + 1)}{2} = \frac{n + 1}{2} = \Theta(n)$$
    \item \textbf{Auxiliary Space Complexity}: $\Theta(1)$ (iterative scalar pointer).
\end{itemize}

\subsection{Advantages, Limitations, and Practical Applications}
\begin{itemize}
    \item \textbf{Advantages}: Zero preprocessing or ordering preconditions; operates on unsorted arrays, linked lists, and streaming data.
    \item \textbf{Limitations}: Linear scaling $\Theta(n)$ becomes computationally prohibitive on massive datasets.
    \item \textbf{Applications}: Small lists ($n \le 64$), unsorted lookups, single-query searches.
\end{itemize}

% ------------------------------------------------------------------------------
% 7.2 BINARY SEARCH
% ------------------------------------------------------------------------------
\section{Binary Search (Rosen §3.1, Algorithm 3)}
\label{sec:binary_search}

\subsection{Problem Statement and Objective}
Given an array $S = [a_0, a_1, \dots, a_{n-1}]$ sorted in non-decreasing order ($a_0 \le a_1 \le \dots \le a_{n-1}$) and a target key $x$, locate the index $m$ such that $S[m] == x$, or return $-1$ if absent.

\subsection{Precondition and Boundary Pointers}
Binary Search strictly requires pre-sorted input. It maintains two boundary pointers: $\text{low} = 0$ and $\text{high} = n - 1$. On each iteration, it computes the midpoint:
$$\text{mid} = \left\lfloor \frac{\text{low} + \text{high}}{2} \right\rfloor$$
If $S[\text{mid}] == x$, the search terminates. If $S[\text{mid}] < x$, the left subrange $[ \text{low}, \text{mid} ]$ is eliminated by setting $\text{low} = \text{mid} + 1$. If $S[\text{mid}] > x$, the right subrange is eliminated by setting $\text{high} = \text{mid} - 1$.

\subsection{Step-by-Step Sample Trace}
Given sorted array $S = [7, 12, 19, 23, 35, 42, 56, 78, 91]$ ($n = 9$) and target $x = 42$:
\begin{enumerate}
    \item \textbf{Probe 1}: $\text{low}=0, \text{high}=8$. $\text{mid} = \lfloor 8/2 \rfloor = 4$. $S[4] = 35$.
    \begin{itemize}
        \item Equality check: $35 == 42$ (False).
        \item Ordering check: $35 < 42$ (True). Discard left half. New $\text{low} = 5$.
    \end{itemize}
    \item \textbf{Probe 2}: $\text{low}=5, \text{high}=8$. $\text{mid} = \lfloor 13/2 \rfloor = 6$. $S[6] = 56$.
    \begin{itemize}
        \item Equality check: $56 == 42$ (False).
        \item Ordering check: $56 < 42$ (False). Discard right half. New $\text{high} = 5$.
    \end{itemize}
    \item \textbf{Probe 3}: $\text{low}=5, \text{high}=5$. $\text{mid} = 5$. $S[5] = 42$.
    \begin{itemize}
        \item Equality check: $42 == 42$ (True). Target matched! Return index $5$.
    \end{itemize}
\end{enumerate}
Total key comparisons: $5$ ($2$ on Probe 1, $2$ on Probe 2, $1$ terminating on Probe 3).

\subsection{Pseudocode (Rosen §3.1, Algorithm 3)}
\begin{lstlisting}[caption={Pseudocode: Binary Search (Rosen §3.1, Algorithm 3)}]
procedure binary_search(x: integer, a1, a2, ..., an: increasing integers)
    i := 1      {low boundary}
    j := n      {high boundary}
    while i < j
        m := floor((i + j) / 2)
        if x > a_m then i := m + 1
        else j := m
    if x = a_i then location := i
    else location := 0
    return location
\end{lstlisting}

\subsection{Flowchart Representation}
Figure \ref{fig:flowchart_binary} illustrates the interval-halving logic of Binary Search.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.4cm]
    \node (start) [startstop] {Start};
    \node (init) [process, below of=start] {$\text{low} \leftarrow 0, \text{high} \leftarrow n - 1$};
    \node (dec1) [decision, below of=init, yshift=-0.3cm] {$\text{low} \le \text{high}$?};
    \node (mid) [process, right of=dec1, xshift=2.2cm] {$\text{mid} \leftarrow \lfloor(\text{low}+\text{high})/2\rfloor$};
    \node (dec2) [decision, below of=mid, yshift=-0.5cm] {$S[\text{mid}] == x$?};
    \node (found) [startstop, right of=dec2, xshift=2.2cm] {Return mid};
    \node (dec3) [decision, below of=dec2, yshift=-0.6cm] {$S[\text{mid}] < x$?};
    \node (right) [process, left of=dec3, xshift=-2.0cm] {$\text{high} \leftarrow \text{mid} - 1$};
    \node (left) [process, right of=dec3, xshift=2.0cm] {$\text{low} \leftarrow \text{mid} + 1$};
    \node (notfound) [startstop, below of=dec1, yshift=-3.5cm] {Return $-1$};

    \draw [arrow] (start) -- (init);
    \draw [arrow] (init) -- (dec1);
    \draw [arrow] (dec1) -- node[anchor=south] {Yes} (mid);
    \draw [arrow] (dec1) -- node[anchor=east] {No} (notfound);
    \draw [arrow] (mid) -- (dec2);
    \draw [arrow] (dec2) -- node[anchor=south] {Yes} (found);
    \draw [arrow] (dec2) -- node[anchor=east] {No} (dec3);
    \draw [arrow] (dec3) -- node[anchor=south] {Yes} (left);
    \draw [arrow] (dec3) -- node[anchor=south] {No} (right);
    \draw [arrow] (left) |- (dec1);
    \draw [arrow] (right) |- (dec1);
\end{tikzpicture}
\caption{Vector Flowchart of the Binary Search Algorithm.}
\label{fig:flowchart_binary}
\end{figure}

\subsection{Authoritative Python Implementation}
Listing \ref{lst:binary_search_code} presents the authoritative source implementation from \texttt{src/algorithms/search.py}.

\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Binary Search}, label={lst:binary_search_code}]
def binary_search(seq: Sequence[Any], target: Any, check_sorted: bool = False) -> int:
    if check_sorted and not is_sorted_sequence(seq):
        raise ValueError("Binary search precondition violated: input must be sorted.")

    low = 0
    high = len(seq) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = seq[mid]
        if mid_val == target:
            return mid
        if mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
\end{lstlisting}

\subsection{Mathematical Recurrence and Complexity Derivation}
On each non-terminating probe, the search range $[ \text{low}, \text{high} ]$ of size $k$ is reduced to at most $\lfloor k/2 \rfloor$. The maximum number of probes $P(n)$ satisfies the recurrence:
$$P(n) = P(\lfloor n/2 \rfloor) + 1, \quad P(1) = 1$$
Solving this classic recurrence yields:
$$P(n) = \lfloor \log_2 n \rfloor + 1$$
Under our concrete probing model (1 comparison on terminating match, 2 comparisons on non-match), the worst-case key comparisons $C_{\text{worst}}(n)$ is:
$$C_{\text{worst}}(n) = 2 \lfloor \log_2 n \rfloor + 1 \quad (\text{successful}), \quad 2(\lfloor \log_2 n \rfloor + 1) \quad (\text{unsuccessful})$$
Thus, $T_{\text{worst}}(n) = \Theta(\log n)$ and $T_{\text{best}}(n) = \Theta(1)$ (when target resides at initial midpoint).

\subsection{Validation Cost vs. Search Cost}
When \texttt{check\_sorted=True} is enabled, validating non-decreasing order requires $n-1$ adjacent comparisons ($\Theta(n)$). Because $\Theta(n) \gg \Theta(\log n)$, validating sorting on every single query completely eliminates the logarithmic advantage. Thus, sorting validation must occur once at data ingestion rather than per search query.

% ------------------------------------------------------------------------------
% 7.3 BUBBLE SORT
% ------------------------------------------------------------------------------
\section{Bubble Sort (Rosen §3.1, Algorithm 4)}
\label{sec:bubble_sort}

\subsection{Problem Statement and Objective}
Given an array $A = [a_0, a_1, \dots, a_{n-1}]$ of $n$ comparable elements, permute $A$ in place such that $a_0 \le a_1 \le \dots \le a_{n-1}$.

\subsection{Working Principle}
Bubble Sort makes $n - 1$ successive passes through the array. In each pass, it sweeps from index $0$ to $n - 2 - i$, comparing adjacent pairs $(a_j, a_{j+1})$ and interchanging them if $a_j > a_{j+1}$. Each pass "bubbles" the largest remaining element to its final sorted position.

\subsection{Textbook Fixed-Pass Formulation (No Early Exit)}
In strict accordance with Kenneth H. Rosen's canonical formulation (§3.1, Algorithm 4), our implementation executes exactly $n - 1$ fixed passes without early-exit flags. This design ensures strict comparison invariance: exactly $\frac{n(n-1)}{2}$ comparisons across all input permutations.

\subsection{Step-by-Step Sample Trace}
Given $A = [5, 1, 4, 2, 8]$ ($n = 5$):
\begin{itemize}
    \item \textbf{Pass 1} ($4$ comparisons):
    $(5, 1) \to \text{Swap } [1, 5, 4, 2, 8]$;
    $(5, 4) \to \text{Swap } [1, 4, 5, 2, 8]$;
    $(5, 2) \to \text{Swap } [1, 4, 2, 5, 8]$;
    $(5, 8) \to \text{No swap}$. Element $8$ settled.
    \item \textbf{Pass 2} ($3$ comparisons):
    $(1, 4) \to \text{No swap}$;
    $(4, 2) \to \text{Swap } [1, 2, 4, 5, 8]$;
    $(4, 5) \to \text{No swap}$. Element $5$ settled.
    \item \textbf{Pass 3} ($2$ comparisons):
    $(1, 2) \to \text{No swap}$;
    $(2, 4) \to \text{No swap}$. Element $4$ settled.
    \item \textbf{Pass 4} ($1$ comparison):
    $(1, 2) \to \text{No swap}$. Element $2$ settled.
\end{itemize}
Total comparisons: $4 + 3 + 2 + 1 = 10 = \frac{5 \times 4}{2}$. Total swaps: $4$.

\subsection{Pseudocode (Rosen §3.1, Algorithm 4)}
\begin{lstlisting}[caption={Pseudocode: Bubble Sort (Rosen §3.1, Algorithm 4)}]
procedure bubblesort(a1, ..., an: real numbers with n >= 2)
    for i := 1 to n - 1
        for j := 1 to n - i
            if aj > aj+1 then
                interchange aj and aj+1
\end{lstlisting}

\subsection{Flowchart Representation}
Figure \ref{fig:flowchart_bubble} presents the control flow for fixed-pass Bubble Sort.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.3cm]
    \node (start) [startstop] {Start};
    \node (p1) [process, below of=start] {$i \leftarrow 0$};
    \node (deci) [decision, below of=p1, yshift=-0.3cm] {$i < n - 1$?};
    \node (p2) [process, right of=deci, xshift=2.2cm] {$j \leftarrow 0$};
    \node (decj) [decision, below of=p2, yshift=-0.5cm] {$j < n - 1 - i$?};
    \node (decswap) [decision, below of=decj, yshift=-0.6cm] {$A[j] > A[j+1]$?};
    \node (swap) [process, right of=decswap, xshift=2.0cm] {$\text{Swap } A[j], A[j+1]$};
    \node (incj) [process, left of=decswap, xshift=-2.0cm] {$j \leftarrow j + 1$};
    \node (inci) [process, left of=deci, xshift=-2.0cm] {$i \leftarrow i + 1$};
    \node (end) [startstop, below of=deci, yshift=-3.5cm] {End (Sorted)};

    \draw [arrow] (start) -- (p1);
    \draw [arrow] (p1) -- (deci);
    \draw [arrow] (deci) -- node[anchor=south] {Yes} (p2);
    \draw [arrow] (deci) -- node[anchor=east] {No} (end);
    \draw [arrow] (p2) -- (decj);
    \draw [arrow] (decj) -- node[anchor=east] {Yes} (decswap);
    \draw [arrow] (decj) -| node[anchor=south] {No} (inci);
    \draw [arrow] (inci) -- (deci);
    \draw [arrow] (decswap) -- node[anchor=south] {Yes} (swap);
    \draw [arrow] (decswap) -- node[anchor=south] {No} (incj);
    \draw [arrow] (swap) |- (incj);
    \draw [arrow] (incj) |- (decj);
\end{tikzpicture}
\caption{Vector Flowchart of the Fixed-Pass Bubble Sort Algorithm.}
\label{fig:flowchart_bubble}
\end{figure}

\subsection{Authoritative Python Implementation}
Listing \ref{lst:bubble_sort_code} extracts the authoritative source implementation from \texttt{src/algorithms/sorting.py}.

\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Bubble Sort}, label={lst:bubble_sort_code}]
def bubble_sort(arr: MutableSequence[Any]) -> MutableSequence[Any]:
    n = len(arr)
    if n < 2:
        return arr

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
\end{lstlisting}

\subsection{Comparison and Swap Complexity}
\begin{itemize}
    \item \textbf{Comparison Invariance}: For all inputs of size $n$, comparisons equal the arithmetic series:
    $$C(n) = \sum_{i=0}^{n-2} (n - 1 - i) = (n - 1) + (n - 2) + \dots + 1 = \frac{n(n - 1)}{2} = \Theta(n^2)$$
    \item \textbf{Swaps}: Best-case (sorted) is $0$; Worst-case (reverse-sorted distinct) is $\frac{n(n-1)}{2}$; Average-case (random) is $\frac{n(n-1)}{4}$.
    \item \textbf{Inversion Equivalence}: Every adjacent swap eliminates exactly one inversion. Thus, for distinct elements, $\text{Swaps} \equiv I(A)$.
\end{itemize}

% ------------------------------------------------------------------------------
% 7.4 INSERTION SORT
% ------------------------------------------------------------------------------
\section{Insertion Sort (Rosen §3.1, Algorithm 5)}
\label{sec:insertion_sort}

\subsection{Problem Statement and Objective}
Given an array $A = [a_0, a_1, \dots, a_{n-1}]$, sort $A$ in place by iteratively inserting each unsorted element into its proper relative position within an expanding sorted prefix.

\subsection{Working Principle}
Insertion Sort partitions the array into a sorted prefix $[0 \dots i-1]$ and an unsorted suffix $[i \dots n-1]$. At step $i$, the key element $A[i]$ is extracted. Elements in the prefix greater than the key are shifted rightward by one position ($A[j+1] = A[j]$). The key is then inserted into the newly vacated position.

\subsection{Step-by-Step Sample Trace}
Given $A = [5, 1, 4, 2, 8]$ ($n = 5$):
\begin{itemize}
    \item \textbf{Pass 1} ($\text{key}=1$): $5 > 1 \to \text{Shift } 5$. Insert $1 \to [1, 5, 4, 2, 8]$. (1 comparison, 1 shift)
    \item \textbf{Pass 2} ($\text{key}=4$): $5 > 4 \to \text{Shift } 5$. $1 \le 4 \to \text{Halt}$. Insert $4 \to [1, 4, 5, 2, 8]$. (2 comparisons, 1 shift)
    \item \textbf{Pass 3} ($\text{key}=2$): $5 > 2 \to \text{Shift } 5$. $4 > 2 \to \text{Shift } 4$. $1 \le 2 \to \text{Halt}$. Insert $2 \to [1, 2, 4, 5, 8]$. (3 comparisons, 2 shifts)
    \item \textbf{Pass 4} ($\text{key}=8$): $5 \le 8 \to \text{Halt immediate}$. Insert $8 \to [1, 2, 4, 5, 8]$. (1 comparison, 0 shifts)
\end{itemize}
Total comparisons: $7$. Total right shifts: $4$.

\subsection{Pseudocode (Rosen §3.1, Algorithm 5)}
\begin{lstlisting}[caption={Pseudocode: Insertion Sort (Rosen §3.1, Algorithm 5)}]
procedure insertionsort(a1, a2, ..., an: real numbers with n >= 2)
    for j := 2 to n
        i := 1
        while aj > ai
            i := i + 1
        m := aj
        for k := 0 to j - i - 1
            aj-k := aj-k-1
        ai := m
\end{lstlisting}

\subsection{Flowchart Representation}
Figure \ref{fig:flowchart_insertion} illustrates the incremental insertion logic.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}[node distance=1.3cm]
    \node (start) [startstop] {Start};
    \node (p1) [process, below of=start] {$i \leftarrow 1$};
    \node (deci) [decision, below of=p1, yshift=-0.3cm] {$i < n$?};
    \node (setkey) [process, right of=deci, xshift=2.4cm] {$\text{key} \leftarrow A[i], j \leftarrow i - 1$};
    \node (decj) [decision, below of=setkey, yshift=-0.6cm] {$j \ge 0 \text{ and } A[j] > \text{key}$?};
    \node (shift) [process, below of=decj, yshift=-0.6cm] {$A[j+1] \leftarrow A[j], j \leftarrow j - 1$};
    \node (insert) [process, left of=shift, xshift=-2.2cm] {$A[j+1] \leftarrow \text{key}, i \leftarrow i + 1$};
    \node (end) [startstop, below of=deci, yshift=-3.5cm] {End (Sorted)};

    \draw [arrow] (start) -- (p1);
    \draw [arrow] (p1) -- (deci);
    \draw [arrow] (deci) -- node[anchor=south] {Yes} (setkey);
    \draw [arrow] (deci) -- node[anchor=east] {No} (end);
    \draw [arrow] (setkey) -- (decj);
    \draw [arrow] (decj) -- node[anchor=east] {Yes} (shift);
    \draw [arrow] (shift) -| (decj);
    \draw [arrow] (decj) -| node[anchor=south] {No} (insert);
    \draw [arrow] (insert) |- (deci);
\end{tikzpicture}
\caption{Vector Flowchart of the Insertion Sort Algorithm.}
\label{fig:flowchart_insertion}
\end{figure}

\subsection{Authoritative Python Implementation}
Listing \ref{lst:insertion_sort_code} extracts the authoritative source implementation from \texttt{src/algorithms/sorting.py}.

\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Insertion Sort}, label={lst:insertion_sort_code}]
def insertion_sort(arr: MutableSequence[Any]) -> MutableSequence[Any]:
    n = len(arr)
    if n < 2:
        return arr

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
\end{lstlisting}

\subsection{Detailed Operation-Count Convention}
\begin{itemize}
    \item \textbf{Right Shifts}: Each execution of $A[j+1] = A[j]$ constitutes exactly one right shift.
    \item \textbf{Element Comparisons}: In Python's short-circuit \texttt{while j >= 0 and arr[j] > key}, element comparison occurs only when $j \ge 0$. If the loop exits because $j < 0$ (key is smallest element), no extra comparison occurs. If it exits because $A[j] \le \text{key}$, one non-shifting comparison is recorded.
    \item \textbf{Best-Case Complexity}: On pre-sorted arrays, inner loops terminate on the very first test. Comparisons: $n - 1 = \Theta(n)$; Shifts: $0$.
    \item \textbf{Worst-Case Complexity}: On reverse-sorted distinct arrays, every key shifts to the start. Comparisons: $\frac{n(n-1)}{2} = \Theta(n^2)$; Shifts: $\frac{n(n-1)}{2} = \Theta(n^2)$.
\end{itemize}
""")

    # =========================================================================
    # CHAPTER 8 — EXPERIMENTAL METHODOLOGY
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 8: EXPERIMENTAL METHODOLOGY
% ==============================================================================
\chapter{Experimental Methodology}
\label{chap:methodology}

\section{Experimental Objectives}
The primary objective of the experimental benchmarking suite is to empirically evaluate algorithm execution duration and operation counts across calibrated input sizes and topological arrangements, ensuring total reproducibility without telemetry interference.

\section{Hardware and Software Environment}
All benchmarks were executed in an isolated execution environment. Table \ref{tab:environment_metadata} documents the host environment metadata recorded during the benchmark run.

\begin{table}[htbp]
\centering
\caption{Empirical Hardware, Software, and Benchmark Execution Environment}
\label{tab:environment_metadata}
\small
\begin{tabularx}{\textwidth}{l X}
\toprule
\textbf{Environment Parameter} & \textbf{Recorded Value} \\
\midrule
Operating System & Windows 11 (Build 10.0.26300) \\
Host Architecture & AMD64 (AMD64 Family 23 Model 96 Stepping 1, AuthenticAMD) \\
Logical CPU Cores & 12 Cores \\
Python Runtime & 3.14.7 (CPython) \\
High-Resolution Timer & \texttt{time.perf\_counter\_ns} (Resolution: 100.0 ns) \\
Replication Factor & $k = 30$ Independent Iterations per Configuration \\
Deterministic Seed & \texttt{42} \\
Total Benchmark Suite Duration & 87.11 seconds \\
\bottomrule
\end{tabularx}
\end{table}

\section{Input Generation and Topologies}
Input datasets are generated deterministically using discrete integer sequences:
\begin{enumerate}
    \item \textbf{Sorted Lists}: Strictly increasing sequences $a_i = \text{start} + i \cdot \text{step}$ ($a_0 < a_1 < \dots < a_{n-1}$).
    \item \textbf{Reverse-Sorted Lists}: Strictly decreasing sequences $a_i = \text{start} + (n - 1 - i) \cdot \text{step}$ ($a_0 > a_1 > \dots > a_{n-1}$), maximizing the inversion count to exactly $I(A) = \frac{n(n-1)}{2}$.
    \item \textbf{Randomly Ordered Lists}: Permutations of the exact same distinct elements generated via the Fisher-Yates shuffle initialized with deterministic seed \texttt{42}.
\end{enumerate}

\section{Input Size Selection}
\begin{itemize}
    \item \textbf{Searching Benchmark Sizes}: $n \in \{100, 500, 1\,000, 5\,000, 10\,000, 50\,000, 100\,000\}$.
    \item \textbf{Sorting Benchmark Sizes}: $n \in \{100, 250, 500, 1\,000, 2\,000, 3\,000\}$.
\end{itemize}

\section{Timing Block Isolation from Telemetry Overhead}
A classic error in software benchmarking is measuring execution time while running instrumented counters. In our harness:
\begin{itemize}
    \item \textbf{Timing Block}: Executes the unadorned, uninstrumented algorithm implementations (\texttt{linear\_search}, \texttt{binary\_search}, \texttt{bubble\_sort}, \texttt{insertion\_sort}) using \texttt{time.perf\_counter\_ns()}.
    \item \textbf{Telemetry Block}: Executes instrumented counterparts once on separate copies to log exact comparisons, swaps, and shifts.
\end{itemize}

\section{Fresh Input Copies for In-Place Sorts}
Because Bubble Sort and Insertion Sort mutate input lists in place, each timed iteration instantiates a fresh copy:
$$\text{\texttt{arr\_to\_sort = list(base\_dataset)}}$$
This copy operation occurs strictly \emph{outside} the timing window, guaranteeing that every replication starts from the identical permutation without polluting duration measurements.

\section{Calibrated Batch Timing for Sub-Microsecond Probes}
Binary Search and best-case Linear Search execute in under $500\text{ ns}$, where timer quantization ($100\text{ ns}$) and OS scheduling jitter can skew single-shot measurements. The harness measures these operations in calibrated batches of $M = 50$ to $200$ invocations, reporting the exact quotient $\Delta t / M$.

\section{Data Aggregation and Descriptive Statistics}
Every configuration is measured across $k = 30$ independent repetitions. For each distribution, we report:
\begin{itemize}
    \item \textbf{Arithmetic Mean} ($\bar{x} = \frac{1}{k} \sum x_i$)
    \item \textbf{Sample Median} (50th percentile, robust to outliers)
    \item \textbf{Sample Standard Deviation} ($s = \sqrt{\frac{1}{k-1} \sum (x_i - \bar{x})^2}$)
    \item \textbf{Interquartile Range} ($\text{IQR} = Q_3 - Q_1$)
\end{itemize}
""")

    # =========================================================================
    # CHAPTER 9 — EXPERIMENTAL RESULTS AND GRAPH ANALYSIS
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 9: EXPERIMENTAL RESULTS AND GRAPH ANALYSIS
% ==============================================================================
\chapter{Experimental Results and Graph Analysis}
\label{chap:results}

\section{Overview of Experimental Artifacts}
The empirical benchmarking harness generated 1,680 individual search trials across 56 configurations and 1,080 sorting trials across 36 configurations. All numerical data presented herein originate from actual physical execution.

\section{Searching Telemetry Analysis}
Table \ref{tab:search_worst_table} reports the empirical measurements for worst-case (missing target) searching across all input scales.

\begin{table}[htbp]
\centering
\caption{Searching Algorithms Worst-Case Empirical Telemetry (Missing Target)}
\label{tab:search_worst_table}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr}
\toprule
\textbf{Algorithm} & $n$ & \textbf{Key Comps} & \textbf{Median ($\mu$s)} & \textbf{Mean ($\mu$s)} & \textbf{Std Dev ($\mu$s)} & \textbf{IQR ($\mu$s)} \\
\midrule
Binary Search & 100 & 14 & 0.69 & 0.69 & 0.02 & 0.01 \\
Linear Search & 100 & 100 & 3.33 & 3.31 & 0.08 & 0.15 \\
Binary Search & 500 & 18 & 1.08 & 1.09 & 0.02 & 0.01 \\
Linear Search & 500 & 500 & 18.50 & 18.42 & 0.17 & 0.20 \\
Binary Search & 1\,000 & 20 & 1.19 & 1.20 & 0.05 & 0.02 \\
Linear Search & 1\,000 & 1\,000 & 37.95 & 38.32 & 1.08 & 0.57 \\
Binary Search & 5\,000 & 26 & 1.50 & 1.51 & 0.03 & 0.02 \\
Linear Search & 5\,000 & 5\,000 & 197.15 & 197.78 & 2.77 & 2.70 \\
Binary Search & 10\,000 & 28 & 1.63 & 1.64 & 0.04 & 0.04 \\
Linear Search & 10\,000 & 10\,000 & 382.05 & 381.96 & 5.86 & 7.42 \\
Binary Search & 50\,000 & 32 & 1.85 & 1.85 & 0.05 & 0.09 \\
Linear Search & 50\,000 & 50\,000 & 1\,922.25 & 1\,925.47 & 28.43 & 39.92 \\
Binary Search & 100\,000 & 34 & 1.96 & 1.98 & 0.05 & 0.01 \\
Linear Search & 100\,000 & 100\,000 & 3\,822.10 & 3\,882.46 & 236.84 & 97.40 \\
\bottomrule
\end{tabular*}
\end{table}

\subsection{Search Operation Counts and Duration Analysis}
Figures \ref{fig:search_ops} and \ref{fig:search_times} illustrate the empirical comparison counts and execution durations for Linear and Binary Search.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure3_search_operation_counts.pdf}
    \caption{Figure 3: Search Key Comparisons across Scales and Scenarios.}
    \label{fig:search_ops}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.88\textwidth]{figures/figure4_search_execution_times.pdf}
    \caption{Figure 4: Search Execution Times with Error Bars Across Scenarios.}
    \label{fig:search_times}
\end{figure}

In Figure \ref{fig:search_ops}, Linear Search comparisons scale linearly with $n$, reaching exactly $100\,000$ operations at $n = 100\,000$. Binary Search comparisons appear completely horizontal against the linear axis, scaling from 14 to 34 comparisons across three orders of magnitude. 

In Figure \ref{fig:search_times}, Linear Search execution duration increases linearly to $3\,822.10\ \mu\text{s}$ ($3.82\text{ ms}$), while Binary Search completes in $1.96\ \mu\text{s}$. The empirical speedup factor is:
$$\text{Speedup} = \frac{3\,822.10\ \mu\text{s}}{1.96\ \mu\text{s}} \approx \mathbf{1\,946.5\times}$$

\section{Sorting Telemetry Analysis}
Table \ref{tab:sorting_random_table} documents the empirical performance for Bubble Sort and Insertion Sort on random permutations.

\begin{table}[htbp]
\centering
\caption{Sorting Algorithms Empirical Telemetry on Random Permutations}
\label{tab:sorting_random_table}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr}
\toprule
\textbf{Algorithm} & $n$ & \textbf{Comparisons} & \textbf{Swaps / Shifts} & \textbf{Median (ms)} & \textbf{Mean (ms)} & \textbf{Std Dev (ms)} \\
\midrule
Bubble Sort & 100 & 4\,950 & 2\,502 & 0.38 & 0.38 & 0.01 \\
Insertion Sort & 100 & 2\,597 & 2\,502 & 0.19 & 0.19 & 0.01 \\
Bubble Sort & 250 & 31\,125 & 15\,618 & 2.29 & 2.29 & 0.02 \\
Insertion Sort & 250 & 15\,863 & 15\,618 & 1.13 & 1.13 & 0.02 \\
Bubble Sort & 500 & 124\,750 & 61\,188 & 9.57 & 9.58 & 0.13 \\
Insertion Sort & 500 & 61\,682 & 61\,188 & 4.76 & 4.74 & 0.07 \\
Bubble Sort & 1\,000 & 499\,500 & 248\,445 & 42.78 & 42.72 & 0.46 \\
Insertion Sort & 1\,000 & 249\,438 & 248\,445 & 20.23 & 20.30 & 0.33 \\
Bubble Sort & 2\,000 & 1\,999\,000 & 1\,026\,195 & 176.56 & 177.16 & 2.41 \\
Insertion Sort & 2\,000 & 1\,028\,183 & 1\,026\,195 & 85.42 & 86.30 & 3.51 \\
Bubble Sort & 3\,000 & 4\,498\,500 & 2\,296\,691 & 405.59 & 406.85 & 6.62 \\
Insertion Sort & 3\,000 & 2\,299\,685 & 2\,296\,691 & 191.65 & 191.80 & 3.41 \\
\bottomrule
\end{tabular*}
\end{table}

\subsection{Sorting Operation Counts and Execution Times}
Figures \ref{fig:sorting_ops} and \ref{fig:sorting_times} present the comparative operations and execution times for both sorting algorithms.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure5_sorting_operation_counts.pdf}
    \caption{Figure 5: Sorting Operation Counts: Comparisons, Swaps, and Right Shifts.}
    \label{fig:sorting_ops}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure6_sorting_execution_times.pdf}
    \caption{Figure 6: Sorting Execution Times on Linear and Log-Log Scales.}
    \label{fig:sorting_times}
\end{figure}

\subsection{Inversion Equivalence Verification at $n = 3\,000$}
A critical empirical milestone is validating the \textbf{Inversion Equivalence Theorem}. Table \ref{tab:sorting_random_table} reveals that on the identical random permutation at $n = 3\,000$:
$$\text{Bubble Sort Swaps} = \mathbf{2\,296\,691}, \quad \text{Insertion Sort Right Shifts} = \mathbf{2\,296\,691}$$
Both algorithms resolve the exact inversion count $I(A) = 2\,296\,691$ with \textbf{0.00\% discrepancy}.

Furthermore, the $+2\,994$ difference in Insertion Sort comparisons ($2\,299\,685$ vs. $2\,296\,691$ shifts) corresponds exactly to the non-boundary condition evaluations:
$$\text{Comparisons} - \text{Shifts} = 2\,299\,685 - 2\,296\,691 = 2\,994$$
Because the outer loop runs for $n - 1 = 2\,999$ passes, and exactly $5$ keys shifted all the way to index $0$ (short-circuiting the boundary check $j < 0$), the inner while loop terminated upon evaluating $A[j] \le \text{key}$ exactly $2\,999 - 5 = 2\,994$ times, providing complete analytical reconciliation.

\subsection{Topology-Specific Performance}
Figures \ref{fig:insertion_topo} and \ref{fig:bubble_topo} contrast the topology sensitivity of Insertion Sort against Bubble Sort's fixed-pass invariance.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure7_insertion_sort_arrangements.pdf}
    \caption{Figure 7: Insertion Sort Across Sorted, Random, and Reverse-Sorted Topologies.}
    \label{fig:insertion_topo}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure8_bubble_sort_arrangements.pdf}
    \caption{Figure 8: Bubble Sort Invariant Comparisons vs. Dynamic Swaps Across Topologies.}
    \label{fig:bubble_topo}
\end{figure}

In Figure \ref{fig:insertion_topo}, Insertion Sort displays dramatic adaptivity: on pre-sorted input ($n = 3\,000$), it requires only $2\,999$ comparisons and $0$ shifts, executing in $0.32\text{ ms}$ ($\Theta(n)$ linear time). On reverse-sorted input, it requires $4\,498\,500$ comparisons and shifts, executing in $365.02\text{ ms}$ ($\Theta(n^2)$ quadratic time).

In Figure \ref{fig:bubble_topo}, Bubble Sort's comparison count is strictly invariant across sorted, random, and reverse inputs: exactly $4\,498\,500$ comparisons. Consequently, on pre-sorted data, Insertion Sort ($0.32\text{ ms}$) outperforms fixed-pass Bubble Sort ($246.25\text{ ms}$) by a factor of:
$$\text{Speedup} = \frac{246.25\text{ ms}}{0.32\text{ ms}} \approx \mathbf{769\times}$$

\subsection{Theoretical Formulas vs. Empirical Telemetry Overlay}
Figure \ref{fig:theoretical_overlay} directly overlays the closed-form mathematical equations onto the physical telemetry counters.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/figure9_theoretical_vs_experimental.pdf}
    \caption{Figure 9: Mathematical Formulas vs. Empirical Telemetry Overlay (Rosen §3.3).}
    \label{fig:theoretical_overlay}
\end{figure}

In all four subplots of Figure \ref{fig:theoretical_overlay}, the empirical telemetry points coincide with the theoretical mathematical curves with \textbf{0.00\% discrepancy}. This verifies that discrete operation counting provides an exact model for physical software execution.
""")

    # =========================================================================
    # CHAPTER 10 — COMPARATIVE ANALYSIS AND DISCUSSION
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 10: COMPARATIVE ANALYSIS AND DISCUSSION
% ==============================================================================
\chapter{Comparative Analysis and Discussion}
\label{chap:comparative}

\section{Linear Search vs. Binary Search}
The comparative analysis of Linear Search and Binary Search highlights a fundamental trade-off in computer science: \textbf{unconditional flexibility versus conditional logarithmic acceleration}.
\begin{itemize}
    \item \textbf{Precondition Requirements}: Linear Search operates without preconditions on input ordering. Binary Search strictly requires a pre-sorted sequence ($\mathcal{O}(n)$ verification cost or $\mathcal{O}(n \log n)$ pre-sorting overhead).
    \item \textbf{Asymptotic Scaling}: As established empirically, at $n = 100\,000$, Binary Search delivers a $\approx 1\,946\times$ speedup over Linear Search.
    \item \textbf{The Break-Even Threshold}: If an unsorted list of $n$ elements is to be searched $q$ times, pre-sorting with an optimal $\mathcal{O}(n \log n)$ algorithm followed by $q$ binary searches is computationally superior to repeated linear scans whenever:
    $$c_{\text{sort}} \cdot n \log_2 n + q \cdot c_{\text{bin}} \cdot \log_2 n < q \cdot c_{\text{lin}} \cdot n$$
    Solving for $q$, pre-sorting is justified whenever the query volume satisfies:
    $$q > \frac{c_{\text{sort}} \cdot n \log_2 n}{c_{\text{lin}} \cdot n - c_{\text{bin}} \cdot \log_2 n} \approx \frac{c_{\text{sort}}}{c_{\text{lin}}} \log_2 n$$
\end{itemize}

\section{Bubble Sort vs. Insertion Sort}
While both Bubble Sort and Insertion Sort belong to the quadratic complexity class $\mathcal{O}(n^2)$ in the worst case, their internal mechanical structures diverge significantly:
\begin{itemize}
    \item \textbf{Mechanical Data Movements}: Bubble Sort performs three memory read/write operations per swap register exchange ($a_j \leftrightarrow a_{j+1}$). In contrast, Insertion Sort uses single-register rightward shifts ($a_{i+1} = a_i$), placing the key once upon loop termination.
    \item \textbf{Comparison Invariance vs. Adaptivity}: Fixed-pass Bubble Sort always executes $\frac{n(n-1)}{2}$ comparisons regardless of initial ordering. Insertion Sort evaluates condition $a_i > \text{key}$ dynamically, halting inner loops as soon as the key's position is resolved.
    \item \textbf{Pre-Sorted Performance}: On pre-sorted arrays ($n = 3\,000$), Insertion Sort completes in $0.32\text{ ms}$ ($\Theta(n)$), outperforming Bubble Sort ($246.25\text{ ms}$) by a factor of \textbf{$769\times$}.
\end{itemize}

\section{Effect of Input Size and Arrangement}
Input size $n$ establishes the macro-asymptotic trajectory. However, for algorithms with divergent best- and worst-case bounds (such as Insertion Sort), input topology exerts a massive constant and asymptotic influence:
$$\text{Sorted: } \Theta(n) \quad \longleftrightarrow \quad \text{Random: } \Theta(n^2) \quad \longleftrightarrow \quad \text{Reverse: } \Theta(n^2)$$

\section{Comparison of Time and Auxiliary Space Complexity}
Table \ref{tab:complexity_comparison_matrix} provides a comprehensive synthesis of all four algorithms.

\begin{table}[htbp]
\centering
\caption{Comprehensive Theoretical and Empirical Complexity Matrix}
\label{tab:complexity_comparison_matrix}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lcccccc}
\toprule
\textbf{Algorithm} & \textbf{Best Case} & \textbf{Average Case} & \textbf{Worst Case} & \textbf{Aux Space} & \textbf{Precondition} & \textbf{Stability} \\
\midrule
Linear Search & $\Theta(1)$ & $\Theta(n)$ & $\Theta(n)$ & $\Theta(1)$ & None & N/A \\
Binary Search & $\Theta(1)$ & $\Theta(\log n)$ & $\Theta(\log n)$ & $\Theta(1)$ & Sorted Input & N/A \\
Bubble Sort (Fixed) & $\Theta(n^2)$ & $\Theta(n^2)$ & $\Theta(n^2)$ & $\Theta(1)$ & None & Stable \\
Insertion Sort & $\Theta(n)$ & $\Theta(n^2)$ & $\Theta(n^2)$ & $\Theta(1)$ & None & Stable \\
\bottomrule
\end{tabular*}
\end{table}

\section{Micro-Architectural Factors Influencing Runtime}
Empirical runtimes exhibit minor non-linearities due to modern micro-architectural factors:
\begin{itemize}
    \item \textbf{Memory Hierarchy}: At small $n$ ($n \le 1\,000$), entire arrays fit inside the CPU's high-speed L1 data cache ($32\text{ KB}$), achieving sub-nanosecond access. At $n = 100\,000$, arrays spill into main RAM, increasing memory latency.
    \item \textbf{Branch Prediction}: In Insertion Sort on sorted inputs, branch predictors accurately anticipate that $a_i > \text{key}$ is False, eliminating pipeline flushes.
\end{itemize}

\section{Practical Real-World Applications}
The adaptive linear behavior $\Theta(n)$ of Insertion Sort on nearly sorted sequences explains why it is universally adopted as the base-case sort in production hybrid algorithms:
\begin{itemize}
    \item \textbf{Timsort}: The default sorting algorithm in Python (\texttt{list.sort()}) and Java (\texttt{Arrays.sort()}), which uses Merge Sort at macro-scale and switches to Insertion Sort for partitions of size $n < 64$ \cite{peters2002timsort}.
    \item \textbf{Introsort}: The standard C++ STL sorting algorithm, which switches from Quick Sort to Insertion Sort when partitions become small.
\end{itemize}

\section{Optional Interactive Dashboard}
\label{sec:dashboard_link}
As an optional enhancement to this analytical monograph, we engineered the \textbf{\DocDashboardTitle{}} located in the project's \texttt{dashboard/} directory. Grounded in Chapter 3 of Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (8th Edition), the dashboard delivers an interactive, client-side web application built with HTML5, CSS3, vanilla JavaScript (ES2022), and pure SVG charting.
\begin{itemize}
    \item \textbf{Project Status}: The dashboard application is fully functional locally. Public deployment to GitHub Pages is currently pending remote repository configuration.
    \item \textbf{Local Web Serving}: Launch via Python's built-in HTTP server:
    \begin{center}
    \texttt{python -m http.server 8000} $\longrightarrow$ \url{http://localhost:8000/dashboard/}
    \end{center}
    or double-click \texttt{dashboard/index.html} directly.
    \item \textbf{Key Capabilities}: (1) Interactive Searching Lab with precondition enforcement, (2) Interactive Sorting Lab with animated vertical bars, (3) Comparison Lab verifying Inversion Equivalence, (4) Growth of Functions Lab with dynamic logarithmic Y-scale toggles, and (5) Integrated Python 3.14.7 empirical benchmark telemetry.
    \item \textbf{Academic Completeness}: This monograph is fully self-contained and mathematically complete independently of the dashboard.
\end{itemize}
""")

    # =========================================================================
    # CHAPTER 11 — CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% CHAPTER 11: CONCLUSION AND FUTURE SCOPE
% ==============================================================================
\chapter{Conclusion and Future Scope}
\label{chap:conclusion}

\section{Summary of Major Findings}
This investigation has systematically explored computational complexity, asymptotic growth, and algorithm analysis grounded in Kenneth H. Rosen's \emph{Discrete Mathematics and Its Applications} (8th Edition), Chapter 3 \cite{rosen2019discrete}. Our major findings include:
\begin{enumerate}
    \item \textbf{Mathematical Model Exactness}: Closed-form operation-count formulas ($T(n) = n$, $T(n) = 2(\lfloor \log_2 n \rfloor + 1)$, $T(n) = n(n-1)/2$, $T(n) = n - 1$) model empirical counter telemetry with \textbf{0.00\% discrepancy}.
    \item \textbf{Asymptotic Scaling Domination}: At $n = 100\,000$, Binary Search delivers an empirical speedup of approximately \textbf{$1\,946\times$} over Linear Search for unsuccessful queries, confirming that logarithmic interval halving decisively eclipses linear scanning.
    \item \textbf{Inversion Equivalence Verification}: We verified empirically that Bubble Sort adjacent swaps and Insertion Sort right shifts are identical ($2\,296\,691$ operations at $n = 3\,000$) on the same random permutation, confirming that both algorithms resolve the identical number of permutation inversions $I(A)$.
    \item \textbf{Adaptive Linear Sorting}: Insertion Sort operates in linear time $\Theta(n)$ ($0.32\text{ ms}$ at $n = 3\,000$) on pre-sorted data, outperforming fixed-pass Bubble Sort ($246.25\text{ ms}$) by a factor of \textbf{$769\times$}.
\end{enumerate}

\section{Pedagogical Implications for MSc IT}
For graduate students in Computer Science and Information Technology, this study demonstrates that discrete mathematical complexity analysis is not merely an abstract academic exercise, but a precise predictive discipline. Understanding the mathematical mechanics of loop invariants, asymptotic bounds, and inversion dynamics is essential for engineering scalable software systems.

\section{Achievement of Assignment Objectives}
All four topics required by the faculty assignment have been thoroughly investigated:
\begin{itemize}
    \item \textbf{What is an Algorithm?}: Formalized through definitions, the seven properties, representation comparisons, and correctness invariants.
    \item \textbf{Types of Algorithms}: Classified into problem categories and design paradigms with an analytical matrix.
    \item \textbf{The Growth of Functions}: Analyzed mathematically across seven canonical functions ($1$ to $n!$) with numerical tables and Figures 1 and 2.
    \item \textbf{Complexity of Algorithms}: Derived mathematically and validated empirically through isolated microbenchmarks and Figures 3 through 9.
\end{itemize}

\section{Future Research Scope}
Future extensions to this research include:
\begin{itemize}
    \item Analyzing randomized algorithms (e.g., Randomized Quick Sort) and formal probabilistic recurrence relations.
    \item Extending the empirical benchmarking harness to external-memory and distributed sorting architectures (e.g., MapReduce, multi-threaded SIMD sorting).
    \item Formal verification of loop invariants using mechanized interactive theorem provers (such as Coq, Lean, or Isabelle/HOL).
\end{itemize}
""")

    # =========================================================================
    # BIBLIOGRAPHY
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% BIBLIOGRAPHY
% ==============================================================================
\begin{thebibliography}{99}

\bibitem{rosen2019discrete}
Kenneth~H. Rosen.
\newblock {\em Discrete Mathematics and Its Applications}.
\newblock McGraw-Hill Higher Education, New York, NY, 8th edition, 2019.
\newblock Chapter 3: Algorithms, the Growth of Functions, and Matrices.

\bibitem{cormen2022introduction}
Thomas~H. Cormen, Charles~E. Leiserson, Ronald~L. Rivest, and Clifford Stein.
\newblock {\em Introduction to Algorithms}.
\newblock The MIT Press, Cambridge, MA, 4th edition, 2022.

\bibitem{knuth1998art}
Donald~E. Knuth.
\newblock {\em The Art of Computer Programming, Volume 3: Sorting and Searching}.
\newblock Addison-Wesley, Reading, MA, 2nd edition, 1998.

\bibitem{hoare1962quicksort}
C.~A.~R. Hoare.
\newblock Quicksort.
\newblock {\em The Computer Journal}, 5(1):10--16, 1962.

\bibitem{peters2002timsort}
Tim Peters.
\newblock Timsort: An adaptive, stable, natural mergesort.
\newblock Python Software Foundation, CPython Source Tree, 2002.
\newblock \url{https://github.com/python/cpython/blob/main/Objects/listsort.txt}.

\end{thebibliography}
""")

    # =========================================================================
    # APPENDICES
    # =========================================================================
    doc.append(r"""
% ==============================================================================
% APPENDICES
% ==============================================================================
\appendix

\chapter{Authoritative Python Source Code Listings}
\label{app:code}

This appendix provides the complete, authoritative Python implementations from the project repository.

\section{Search Algorithms Implementation (\texttt{src/algorithms/search.py})}
\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Search Algorithms}]
""" + SEARCH_PY_CODE + r"""
\end{lstlisting}

\section{Sorting Algorithms Implementation (\texttt{src/algorithms/sorting.py})}
\begin{lstlisting}[language=Python, caption={Authoritative Implementation of Sorting Algorithms}]
""" + SORTING_PY_CODE + r"""
\end{lstlisting}

\chapter{Supplemental Empirical Telemetry Tables}
\label{app:tables}

\section{Search Middle Target Scenario}
Table \ref{tab:search_middle_app} documents the empirical measurements when the search target resides at index $\lfloor n / 2 \rfloor$.

\begin{table}[htbp]
\centering
\caption{Searching Empirical Summary: Middle Target Scenario}
\label{tab:search_middle_app}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrr}
\toprule
\textbf{Algorithm} & $n$ & \textbf{Key Comps} & \textbf{Median ($\mu$s)} & \textbf{Mean ($\mu$s)} & \textbf{Std Dev ($\mu$s)} \\
\midrule
Linear Search & 100 & 51 & 1.81 & 1.82 & 0.07 \\
Linear Search & 500 & 251 & 8.35 & 8.41 & 0.15 \\
Linear Search & 1\,000 & 501 & 19.00 & 19.02 & 0.28 \\
Linear Search & 5\,000 & 2\,501 & 96.40 & 96.35 & 1.66 \\
Linear Search & 10\,000 & 5\,001 & 190.80 & 191.64 & 3.33 \\
Linear Search & 50\,000 & 25\,001 & 952.00 & 952.52 & 10.71 \\
Linear Search & 100\,000 & 50\,001 & 1\,942.00 & 1\,944.48 & 29.89 \\
\midrule
Binary Search & 100 & 11 & 0.57 & 0.58 & 0.04 \\
Binary Search & 500 & 15 & 0.90 & 0.91 & 0.04 \\
Binary Search & 1\,000 & 17 & 1.04 & 1.04 & 0.02 \\
Binary Search & 5\,000 & 23 & 1.36 & 1.36 & 0.02 \\
Binary Search & 10\,000 & 25 & 1.49 & 1.51 & 0.06 \\
Binary Search & 50\,000 & 29 & 1.69 & 1.70 & 0.05 \\
Binary Search & 100\,000 & 31 & 1.90 & 1.94 & 0.06 \\
\bottomrule
\end{tabular*}
\end{table}

\section{Sorting Pre-Sorted Scenario: Best-Case Analysis}
Table \ref{tab:sorting_sorted_app} documents algorithm behavior on pre-sorted arrays.

\begin{table}[htbp]
\centering
\caption{Sorting Empirical Summary: Already Sorted Input Topology}
\label{tab:sorting_sorted_app}
\small
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrr}
\toprule
\textbf{Algorithm} & $n$ & \textbf{Comparisons} & \textbf{Swaps / Shifts} & \textbf{Median (ms)} & \textbf{Mean (ms)} \\
\midrule
Bubble Sort & 100 & 4\,950 & 0 & 0.221 & 0.220 \\
Bubble Sort & 250 & 31\,125 & 0 & 1.351 & 1.355 \\
Bubble Sort & 500 & 124\,750 & 0 & 5.676 & 5.680 \\
Bubble Sort & 1\,000 & 499\,500 & 0 & 25.795 & 25.737 \\
Bubble Sort & 2\,000 & 1\,999\,000 & 0 & 106.282 & 106.216 \\
Bubble Sort & 3\,000 & 4\,498\,500 & 0 & 246.252 & 246.870 \\
\midrule
Insertion Sort & 100 & 99 & 0 & 0.009 & 0.009 \\
Insertion Sort & 250 & 249 & 0 & 0.022 & 0.022 \\
Insertion Sort & 500 & 499 & 0 & 0.047 & 0.048 \\
Insertion Sort & 1\,000 & 999 & 0 & 0.102 & 0.102 \\
Insertion Sort & 2\,000 & 1\,999 & 0 & 0.208 & 0.209 \\
Insertion Sort & 3\,000 & 2\,999 & 0 & 0.311 & 0.311 \\
\bottomrule
\end{tabular*}
\end{table}

\chapter{Representative Execution Outputs}
\label{app:outputs}

\section{Automated Correctness Test Suite Log}
\begin{verbatim}
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: D:/DiscreteMathsProject_202612120
configfile: pyproject.toml
testpaths: tests
plugins: platformdirs-4.14.7
collected 64 items

tests/test_benchmarking.py .............                                 [ 20%]
tests/test_dashboard.py ....                                             [ 26%]
tests/test_report.py .....                                               [ 34%]
tests/test_search.py ........................                            [ 71%]
tests/test_sorting.py ..................                                 [100%]

============================= 64 passed in 2.98s ==============================
\end{verbatim}

\section{Pilot Benchmark Calibration Log}
\begin{verbatim}
======================================================================
ALGORITHM EXPLORER — EMPIRICAL BENCHMARKING SUITE
Academic Reference: Kenneth H. Rosen, Discrete Mathematics (8th Ed.)
Random Seed: 42 | Repetitions per Configuration: 30
======================================================================

[1/4] Running Environment Verification and Pilot Benchmark...
  Pilot n=100: BubbleSort=0.389ms, InsertionSort=0.199ms
  Pilot n=500: BubbleSort=9.931ms, InsertionSort=4.818ms
  Pilot n=1000: BubbleSort=42.626ms, InsertionSort=20.307ms
  Pilot n=2000: BubbleSort=176.271ms, InsertionSort=80.585ms
\end{verbatim}

\chapter{Reproducibility Instructions}
\label{app:reproduction}

To reproduce the empirical benchmarks, generate the publication figures, execute the interactive Jupyter notebook, and verify the automated test suite, execute the following commands from the project root:

\begin{verbatim}
# 1. Execute all empirical microbenchmarks:
python scripts/run_benchmarks.py

# 2. Synthesize all 9 publication-grade figures (.pdf and .png):
python scripts/generate_figures.py

# 3. Build, execute, and verify the interactive Jupyter research notebook:
python scripts/build_notebook.py

# 4. Synchronize LaTeX assets and package Overleaf archive:
python scripts/build_report.py

# 5. Execute full automated test suite:
python -m pytest -v
node scripts/test_dashboard_algorithms.js

# 6. Launch the optional web dashboard locally:
python -m http.server 8000
\end{verbatim}

\end{document}
""")

    full_content = "".join(doc)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Master Monograph successfully generated at: {out_path} ({len(full_content):,} chars)")

if __name__ == "__main__":
    generate_report()
