import os
import sys

AUTHOR = "Abhishek Vincent"
ROLL = "03"


def escape(value):
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    return value


def make_page(number, date, title, description, first=False):
    display_number = "Project" if int(number) == 57 else str(int(number))
    reset = "\\pagenumbering{arabic}\n" if first else ""
    return f"""\\clearpage
{reset}\\label{{prog:{number}}}
\\programhead
  {{{display_number}}}
  {{{date}}}
  {{{escape(title)}}}
  {{{escape(description)}}}
  {{{AUTHOR}}}
  {{{ROLL}}}
  {{{date}}}
\\lstinputlisting[style=code]{{programs/p{number}.c}}
\\divider
\\textbf{{Output Text:}}\\par
\\vspace{{2pt}}
\\lstinputlisting[style=out]{{outputs/p{number}.txt}}
"""


def make_index(entries):
    lines = [
        r"\clearpage",
        r"\begin{center}",
        r"{\fontsize{18}{22}\selectfont\textbf{INDEX}}",
        r"\end{center}",
        r"\vspace{10pt}",
        r"{\fontsize{8.5}{10}\selectfont",
        r"\begin{longtable}{@{}p{0.55in}@{\hspace{6pt}}p{4.95in}@{\hspace{6pt}}r@{}}",
        r"\textbf{No.} & \textbf{Program Title} & \textbf{Page} \\ \hline",
        r"\endfirsthead",
        r"\textbf{No.} & \textbf{Program Title} & \textbf{Page} \\ \hline",
        r"\endhead",
    ]

    for display_number, title, number in entries:
        lines.append(
            f"{display_number} & {escape(title)} & \\pageref{{prog:{number}}} \\\\"
        )

    lines.extend([r"\end{longtable}", r"}"])

    return "\n".join(lines) + "\n"


def main():
    with open("meta.tsv", "r", encoding="utf-8") as handle:
        rows = [line.rstrip("\n").split("\t") for line in handle if line.strip()]

    numbers = []
    entries = []

    for row in rows:
        number, date, title, description = row
        number = f"{int(number):02d}"
        display_number = "Project" if int(number) == 57 else str(int(number))
        first = not numbers
        numbers.append(number)
        entries.append((display_number, title, number))
        page = make_page(number, date, title, description, first)

        with open(f"pages/p{number}.tex", "w", encoding="utf-8") as handle:
            handle.write(page)

    with open("pages/index.tex", "w", encoding="utf-8") as handle:
        handle.write(make_index(entries))

    with open("pages/all.tex", "w", encoding="utf-8") as handle:
        for number in numbers:
            handle.write(f"\\input{{pages/p{number}}}\n")

    print(f"generated {len(numbers)} pages")


if __name__ == "__main__":
    main()
