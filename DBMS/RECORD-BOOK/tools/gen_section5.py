#!/usr/bin/env python3
"""Section 5.4 - 5.6 (Functions, Triggers, Views) of the DBMS record.

Runs every answer against the live library schema, caches the result and
writes one LaTeX page per question:

    record/pages5/s5x_*n.tex
    record/section5.tex              (page numbering starts at 104)

    python3 tools/gen_section5.py            # rebuild pages from the cache
    python3 tools/gen_section5.py --capture  # re-run everything on the DB
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE_DIR = os.path.join(ROOT, "record", "pages5")
TEX = os.path.join(ROOT, "record", "section5.tex")
CACHE = os.path.join(ROOT, "tools", ".section5_cache.json")
CONN = "mca/mca@localhost:1521/FREEPDB1"

SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}
STATUS_RE = re.compile(
    r"^(\d+ rows? (created|updated|deleted)\.|Table (altered|created|dropped)\.|"
    r"Function created\.|Trigger created\.|View created\.|"
    r"Commit complete\.)$")


def prose(t):
    return "".join(SPECIAL.get(c, c) for c in t)


# --------------------------------------------------------------------------
# the answers: (number, question, ddl, demo, [show sql], [[(column, type)]])
# --------------------------------------------------------------------------
FUNCS = [
    (1, "Create a function that returns a member's name using the member ID.",
     """CREATE OR REPLACE FUNCTION get_member_name (p_member_id NUMBER)
RETURN member.full_name%TYPE
IS
   v_name member.full_name%TYPE;
BEGIN
   SELECT full_name INTO v_name
   FROM member
   WHERE member_id = p_member_id;

   RETURN v_name;
END;
/""", "",
     ["SELECT get_member_name(1003) AS member_name FROM dual;"],
     [[("MEMBER_NAME", "VARCHAR2")]]),
    (2, "Create a function that returns the total number of books.",
     """CREATE OR REPLACE FUNCTION total_books
RETURN NUMBER
IS
   v_count NUMBER;
BEGIN
   SELECT COUNT(*) INTO v_count FROM book;
   RETURN v_count;
END;
/""", "",
     ["SELECT total_books() AS total_books FROM dual;"],
     [[("TOTAL_BOOKS", "NUMBER")]]),
    (3, "Create a function that returns the number of members of a given member "
        "type.",
     """CREATE OR REPLACE FUNCTION member_count (p_type VARCHAR2)
RETURN NUMBER
IS
   v_count NUMBER;
BEGIN
   SELECT COUNT(*) INTO v_count
   FROM member
   WHERE member_type = UPPER(p_type);

   RETURN v_count;
END;
/""", "",
     ["SELECT member_count('STUDENT') AS student_members FROM dual;"],
     [[("STUDENT_MEMBERS", "NUMBER")]]),
    (4, "Create a function that returns the number of AVAILABLE copies of a book.",
     """CREATE OR REPLACE FUNCTION available_copies (p_book_id NUMBER)
RETURN NUMBER
IS
   v_count NUMBER;
BEGIN
   SELECT COUNT(*) INTO v_count
   FROM book_copy
   WHERE book_id = p_book_id
     AND availability_status = 'AVAILABLE';

   RETURN v_count;
END;
/""", "",
     ["SELECT available_copies(4003) AS available_copies FROM dual;"],
     [[("AVAILABLE_COPIES", "NUMBER")]]),
    (5, "Create a function that returns the total fine amount recorded for a "
        "given member ID.",
     """CREATE OR REPLACE FUNCTION total_fine (p_member_id NUMBER)
RETURN NUMBER
IS
   v_total NUMBER;
BEGIN
   SELECT NVL(SUM(amount), 0) INTO v_total
   FROM fine
   WHERE member_id = p_member_id;

   RETURN v_total;
END;
/""", "",
     ["SELECT total_fine(1012) AS total_fine FROM dual;"],
     [[("TOTAL_FINE", "NUMBER")]]),
    (6, "Create a function that returns a staff member's salary using the staff ID.",
     """CREATE OR REPLACE FUNCTION staff_salary (p_staff_id NUMBER)
RETURN NUMBER
IS
   v_salary staff.salary%TYPE;
BEGIN
   SELECT salary INTO v_salary
   FROM staff
   WHERE staff_id = p_staff_id;

   RETURN v_salary;
END;
/""", "",
     ["SELECT staff_salary(503) AS salary FROM dual;"],
     [[("SALARY", "NUMBER")]]),
]

TRIGGERS = [
    (1, "Create a trigger to change a member's name to uppercase before inserting "
        "the member.",
     """CREATE OR REPLACE TRIGGER trg_member_name_upper
BEFORE INSERT ON member
FOR EACH ROW
BEGIN
   :NEW.full_name := UPPER(:NEW.full_name);
END;
/""",
     """INSERT INTO member (member_id, full_name, member_type, branch_id)
VALUES (1016, 'arjun das', 'STUDENT', 101);""",
     ["SELECT member_id, full_name FROM member WHERE member_id = 1016;"],
     [[("MEMBER_ID", "NUMBER"), ("FULL_NAME", "VARCHAR2")]]),
    (2, "Create a trigger to stop a book's price from being set below zero.",
     """CREATE OR REPLACE TRIGGER trg_book_price_positive
BEFORE INSERT OR UPDATE OF price ON book
FOR EACH ROW
WHEN (NEW.price < 0)
BEGIN
   RAISE_APPLICATION_ERROR(-20001, 'Book price cannot be negative');
END;
/""",
     "UPDATE book SET price = -250 WHERE book_id = 4002;",
     [], []),
    (3, "Create a trigger to fill in the join date with today's date when it is "
        "not provided.",
     """CREATE OR REPLACE TRIGGER trg_member_join_date
BEFORE INSERT ON member
FOR EACH ROW
WHEN (NEW.join_date IS NULL)
BEGIN
   :NEW.join_date := SYSDATE;
END;
/""",
     """INSERT INTO member (member_id, full_name, member_type, branch_id)
VALUES (1017, 'KAVYA MENON', 'PUBLIC', 102);""",
     ["SELECT member_id, full_name, join_date FROM member WHERE member_id = 1017;"],
     [[("MEMBER_ID", "NUMBER"), ("FULL_NAME", "VARCHAR2"), ("JOIN_DATE", "DATE")]]),
    (4, "Create a trigger to set a book copy's status to AVAILABLE when a loan is "
        "marked RETURNED.",
     """CREATE OR REPLACE TRIGGER trg_loan_returned
AFTER UPDATE OF loan_status ON loan
FOR EACH ROW
WHEN (NEW.loan_status = 'RETURNED')
BEGIN
   UPDATE book_copy
   SET availability_status = 'AVAILABLE'
   WHERE copy_id = :OLD.copy_id;
END;
/""",
     """UPDATE loan SET loan_status = 'RETURNED', return_date = SYSDATE
WHERE loan_id = 7001;""",
     ["SELECT loan_id, loan_status FROM loan WHERE loan_id = 7001;",
      "SELECT copy_id, availability_status FROM book_copy WHERE copy_id = 6002;"],
     [[("LOAN_ID", "NUMBER"), ("LOAN_STATUS", "VARCHAR2")],
      [("COPY_ID", "NUMBER"), ("AVAILABILITY_STATUS", "VARCHAR2")]]),
    (5, "Create a trigger to stop the amount paid for a fine from being greater "
        "than the fine amount.",
     """CREATE OR REPLACE TRIGGER trg_fine_paid_limit
BEFORE INSERT OR UPDATE OF amount_paid ON fine
FOR EACH ROW
WHEN (NEW.amount_paid > NEW.amount)
BEGIN
   RAISE_APPLICATION_ERROR(-20002, 'Amount paid cannot exceed the fine amount');
END;
/""",
     "UPDATE fine SET amount_paid = amount + 100 WHERE fine_id = 9001;",
     [], []),
    (6, "Create a simple trigger that displays a message when a new book is added.",
     """CREATE OR REPLACE TRIGGER trg_book_added
AFTER INSERT ON book
FOR EACH ROW
BEGIN
   DBMS_OUTPUT.PUT_LINE('New book added: ' || :NEW.title);
END;
/""",
     """INSERT INTO book (book_id, isbn, title, category, publisher_id)
VALUES (4021, '978-81-0000-021', 'Database Systems',
        'Computer Science', 201);""",
     [], []),
]

VIEWS = [
    (1, "Create a view named BOOK_DETAILS showing each book's ID, title, category, "
        "publication year, and price.",
     """CREATE OR REPLACE VIEW book_details AS
SELECT book_id, title, category, publication_year, price
FROM book;""", "",
     ["SELECT * FROM book_details;"],
     [[("BOOK_ID", "NUMBER"), ("TITLE", "VARCHAR2"), ("CATEGORY", "VARCHAR2"),
       ("PUBLICATION_YEAR", "NUMBER"), ("PRICE", "NUMBER")]]),
    (2, "Create a view named ACTIVE_MEMBERS showing members whose status is ACTIVE.",
     """CREATE OR REPLACE VIEW active_members AS
SELECT member_id, full_name, member_type, city, join_date
FROM member
WHERE status = 'ACTIVE';""", "",
     ["SELECT * FROM active_members;"],
     [[("MEMBER_ID", "NUMBER"), ("FULL_NAME", "VARCHAR2"),
       ("MEMBER_TYPE", "VARCHAR2"), ("CITY", "VARCHAR2"),
       ("JOIN_DATE", "DATE")]]),
    (3, "Create a view named AVAILABLE_BOOKS showing copies whose status is "
        "AVAILABLE.",
     """CREATE OR REPLACE VIEW available_books AS
SELECT copy_id, book_id, branch_id, accession_no
FROM book_copy
WHERE availability_status = 'AVAILABLE';""", "",
     ["SELECT * FROM available_books;"],
     [[("COPY_ID", "NUMBER"), ("BOOK_ID", "NUMBER"), ("BRANCH_ID", "NUMBER"),
       ("ACCESSION_NO", "VARCHAR2")]]),
    (4, "Create a view showing book titles and publisher names, using the relevant "
        "tables if they exist in your database.",
     """CREATE OR REPLACE VIEW book_publishers AS
SELECT b.title, p.publisher_name
FROM book b
JOIN publisher p ON b.publisher_id = p.publisher_id;""", "",
     ["SELECT * FROM book_publishers;"],
     [[("TITLE", "VARCHAR2"), ("PUBLISHER_NAME", "VARCHAR2")]]),
    (5, "Create a view showing each book category and the number of books in it.",
     """CREATE OR REPLACE VIEW category_summary AS
SELECT category, COUNT(*) AS book_count
FROM book
GROUP BY category;""", "",
     ["SELECT * FROM category_summary;"],
     [[("CATEGORY", "VARCHAR2"), ("BOOK_COUNT", "NUMBER")]]),
    (6, "Create a view showing staff names and their salaries.",
     """CREATE OR REPLACE VIEW staff_salaries AS
SELECT full_name, salary
FROM staff;""", "",
     ["SELECT * FROM staff_salaries;"],
     [[("FULL_NAME", "VARCHAR2"), ("SALARY", "NUMBER")]]),
]

SECTIONS = [("5.4", "Functions", FUNCS, "f"),
            ("5.5", "Triggers", TRIGGERS, "t"),
            ("5.6", "Views", VIEWS, "v")]

# run between 5.5 and 5.6 so the demo rows do not leak into the view outputs
CLEANUP = """DROP TRIGGER trg_member_name_upper;
DROP TRIGGER trg_book_price_positive;
DROP TRIGGER trg_member_join_date;
DROP TRIGGER trg_loan_returned;
DROP TRIGGER trg_fine_paid_limit;
DROP TRIGGER trg_book_added;
DELETE FROM member WHERE member_id IN (1016, 1017);
DELETE FROM book WHERE book_id = 4021;
UPDATE loan SET loan_status = 'ISSUED', return_date = NULL WHERE loan_id = 7001;
UPDATE book_copy SET availability_status = 'ISSUED' WHERE copy_id = 6002;
COMMIT;"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def render_db(headers, rows, types):
    widths = [max([len(h)] + [len(r[i]) for r in rows])
              for i, h in enumerate(headers)]
    numeric = [t == "NUMBER" for t in types]
    head = [h.rjust(w) if n else h.ljust(w)
            for h, w, n in zip(headers, widths, numeric)]
    out = ["  ".join(head), "  ".join("-" * w for w in widths)]
    for r in rows:
        cells = [v.rjust(w) if n else v.ljust(w)
                 for v, w, n in zip(r, widths, numeric)]
        out.append("  ".join(cells).rstrip())
    return out


def page(num, question, code, out_lines):
    longest = max((len(l) for l in out_lines), default=0)
    if longest <= 85:
        size = r"\small"
    elif longest <= 93:
        size = r"\footnotesize"
    elif longest <= 116:
        size = r"\scriptsize"
    else:
        size = r"\tiny"
    return r"""%% ---- Section 5 / question %(num)d
\noindent\begin{minipage}{\linewidth}
\begingroup\hyphenpenalty=10000\exhyphenpenalty=10000
{\fontsize{14}{17}\selectfont\textbf{%(num)d.}}\ %(q)s\par
\endgroup\vspace{12pt}

\codeheading{CODE:}

\begin{sqlcode}%(codesize)s
%(code)s
\end{sqlcode}

\vspace{18pt}

\codeheading{OUTPUT:}

\begin{sqlout}[fontsize=%(size)s]
%(out)s
\end{sqlout}
\end{minipage}\par\vspace{24pt}

""" % dict(num=num, q=prose(question), code="\n".join(code),
           out="\n".join(out_lines), size=size,
           codesize="[fontsize=\\footnotesize]"
                    if max((len(l) for l in code), default=0) > 89 else "")


# --------------------------------------------------------------------------
# capture
# --------------------------------------------------------------------------
def sqlplus(script):
    p = subprocess.run(
        ["podman", "exec", "-i", "oracledb", "sqlplus", "-S", CONN],
        input=script, capture_output=True, text=True)
    return (p.stdout + p.stderr).splitlines()


def split_blocks(lines):
    """Split sqlplus output on @@name@@ markers -> {name: [lines]}."""
    pat = re.compile(r"^@@(\S+)@@$")
    out, cur = {}, None
    for line in lines:
        m = pat.match(line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


def tidy(lines):
    out = []
    for line in lines:
        if not line.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(line.rstrip())
    while out and out[-1] == "":
        out.pop()
    return out


def parse_rows(lines):
    rows = []
    for line in lines:
        if not line.strip() or re.match(r"^\d+ rows? selected\.$", line.strip()):
            continue
        rows.append([c.strip() for c in line.split("~")])
    return rows


def capture():
    script = ["SET SERVEROUTPUT ON", "SET HEADING OFF", "SET COLSEP '~'",
              "SET LINESIZE 32767", "SET TRIMSPOOL ON", "SET PAGESIZE 5000",
              "SET NEWPAGE NONE", "SET FEEDBACK ON", "SET ECHO OFF",
              "SET VERIFY OFF", ""]

    def emit(item, tag):
        num, _q, ddl, demo, shows, _cols = item
        key = "%s%02d" % (tag, num)
        script.append("PROMPT @@%s@@" % key)
        script.append(ddl)
        if demo:
            script.append(demo)
        for i, show in enumerate(shows):
            script.append("PROMPT @@%s_%d@@" % (key, i))
            script.append(show)

    for _sec, _title, items, tag in SECTIONS[:2]:
        for item in items:
            emit(item, tag)
    script.append("PROMPT @@CLEANUP@@")
    script.extend(CLEANUP.splitlines())
    for item in VIEWS:
        emit(item, "v")
    script.append("PROMPT @@ZZ99@@")

    out = sqlplus("\n".join(script) + "\n")
    blk = split_blocks(out)

    cache = {}
    for _sec, _title, items, tag in SECTIONS:
        for num, _q, ddl, demo, shows, cols in items:
            key = "%s%02d" % (tag, num)
            if key not in blk:
                print("missing block", key)
                print("\n".join(out[-40:]))
                sys.exit(1)
            entry = {"status": [], "tables": []}
            for line in tidy(blk[key]):
                if not line:
                    continue
                if line.startswith("ORA-06512") or line.startswith("ORA-04088"):
                    continue
                entry["status"].append(line)
            for i, spec in enumerate(cols):
                rows = parse_rows(blk.get("%s_%d" % (key, i), []))
                entry["tables"].append({
                    "headers": [c for c, _t in spec],
                    "types": [t for _c, t in spec],
                    "rows": rows})
            cache[key] = entry

    with open(CACHE, "w") as f:
        json.dump(cache, f, indent=1)
    print("captured", len(cache), "answers")


# --------------------------------------------------------------------------
# page build
# --------------------------------------------------------------------------
def build():
    cache = json.load(open(CACHE))
    os.makedirs(PAGE_DIR, exist_ok=True)
    tex = [r"""%% =====================================================================
%%  DBMS Lab Record - 5.4 Functions, 5.5 Triggers, 5.6 Views
%%  Continuation of the record: page numbering starts at 104.
%%  Build: latexmk -xelatex section5.tex
%% =====================================================================""",
           r"\input{record-preamble}", "", r"\setcounter{page}{104}", "",
           r"\begin{document}"]

    for sec, title, items, tag in SECTIONS:
        tex += ["", r"\clearpage", r"\subsubheading{%s  %s}" % (sec, title)]
        for num, q, ddl, demo, shows, _cols in items:
            key = "%s%02d" % (tag, num)
            entry = cache[key]
            code = ddl.split("\n")
            if demo:
                code += [""] + demo.split("\n")
            for show in shows:
                code += [""] + show.split("\n")

            out = list(entry["status"])
            for tbl in entry["tables"]:
                rows = tbl["rows"]
                out += [""] + render_db(tbl["headers"], rows, tbl["types"])
                out += ["", "%d row%s selected." % (len(rows),
                                                    "" if len(rows) == 1 else "s")]

            name = "s%s_%s%02d" % (sec.replace(".", ""), tag, num)
            tex.append(r"\input{pages5/%s}" % name)
            with open(os.path.join(PAGE_DIR, name + ".tex"), "w") as f:
                f.write(page(num, q, code, out))
    tex += ["", r"\end{document}"]
    with open(TEX, "w") as f:
        f.write("\n".join(tex) + "\n")
    print("wrote", TEX)


if __name__ == "__main__":
    if "--capture" in sys.argv:
        capture()
    build()
