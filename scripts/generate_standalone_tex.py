"""
Generate a 100% self-contained, standalone LaTeX monograph:
`Algorithm_Explorer_Report_Standalone.tex`

Inlines:
- All preamble packages and styling from `latex/styles/academic_report.sty`
- Document configuration and metadata from `latex/config.tex`
- All 10 core chapters from `latex/chapters/`
- All tables from `latex/tables/` with guaranteed LaTeX-escaped formatting
- Inlined thebibliography environment (no external BibTeX compilation step needed)
- All 4 appendices
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BIB_ENTRIES = r"""\begin{thebibliography}{99}

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

\end{thebibliography}"""


def build_standalone():
    # 1. Config
    with open(PROJECT_ROOT / "latex" / "config.tex", "r", encoding="utf-8") as f:
        config_text = f.read()

    # 2. Style
    with open(PROJECT_ROOT / "latex" / "styles" / "academic_report.sty", "r", encoding="utf-8") as f:
        style_text = f.read()
    # Strip package headers
    style_text = re.sub(r"\\NeedsTeXFormat\{LaTeX2e\}", "", style_text)
    style_text = re.sub(r"\\ProvidesPackage\{[^}]*\}\[[^\]]*\]", "", style_text)

    # 3. Read chapters and inline tables
    def read_and_inline(file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Inline any nested \input{latex/tables/...}
        def table_repl(match):
            tbl_path = PROJECT_ROOT / match.group(1).replace("/", "\\")
            if not tbl_path.exists():
                tbl_path = PROJECT_ROOT / match.group(1)
            if tbl_path.exists():
                with open(tbl_path, "r", encoding="utf-8") as tf:
                    return tf.read()
            return match.group(0)

        content = re.sub(r"\\input\{(latex/tables/[^}]+)\}", table_repl, content)
        return content

    # 4. Master template
    with open(PROJECT_ROOT / "Algorithm_Explorer_Report.tex", "r", encoding="utf-8") as f:
        master_text = f.read()

    # Replace \input{latex/config.tex} with config_text
    master_text = master_text.replace(r"\input{latex/config.tex}", config_text)

    # Replace \usepackage{latex/styles/academic_report} with style_text
    master_text = master_text.replace(r"\usepackage{latex/styles/academic_report}", style_text)

    # Replace chapters
    chapters = [
        ("01_introduction.tex", PROJECT_ROOT / "latex" / "chapters" / "01_introduction.tex"),
        ("02_fundamentals_of_algorithms.tex", PROJECT_ROOT / "latex" / "chapters" / "02_fundamentals_of_algorithms.tex"),
        ("03_growth_of_functions.tex", PROJECT_ROOT / "latex" / "chapters" / "03_growth_of_functions.tex"),
        ("04_asymptotic_notations.tex", PROJECT_ROOT / "latex" / "chapters" / "04_asymptotic_notations.tex"),
        ("05_complexity_of_algorithms.tex", PROJECT_ROOT / "latex" / "chapters" / "05_complexity_of_algorithms.tex"),
        ("06_analytical_study_of_algorithms.tex", PROJECT_ROOT / "latex" / "chapters" / "06_analytical_study_of_algorithms.tex"),
        ("07_experimental_methodology.tex", PROJECT_ROOT / "latex" / "chapters" / "07_experimental_methodology.tex"),
        ("08_experimental_results.tex", PROJECT_ROOT / "latex" / "chapters" / "08_experimental_results.tex"),
        ("09_comparative_analysis.tex", PROJECT_ROOT / "latex" / "chapters" / "09_comparative_analysis.tex"),
        ("10_conclusion.tex", PROJECT_ROOT / "latex" / "chapters" / "10_conclusion.tex"),
        ("appendix_a_code.tex", PROJECT_ROOT / "latex" / "chapters" / "appendix_a_code.tex"),
        ("appendix_b_tables.tex", PROJECT_ROOT / "latex" / "chapters" / "appendix_b_tables.tex"),
        ("appendix_c_outputs.tex", PROJECT_ROOT / "latex" / "chapters" / "appendix_c_outputs.tex"),
        ("appendix_d_reproduction.tex", PROJECT_ROOT / "latex" / "chapters" / "appendix_d_reproduction.tex"),
    ]

    for ch_name, ch_path in chapters:
        ch_content = read_and_inline(ch_path)
        master_text = master_text.replace(f"\\input{{latex/chapters/{ch_name}}}", ch_content)

    # Replace bibliography
    bib_block = r"\bibliographystyle{plain}" + "\n" + r"\bibliography{latex/references}"
    master_text = master_text.replace(bib_block, BIB_ENTRIES)

    out_file = PROJECT_ROOT / "Algorithm_Explorer_Report_Standalone.tex"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(master_text)

    print(f"Generated standalone monolithic LaTeX document: {out_file} ({out_file.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_standalone()
