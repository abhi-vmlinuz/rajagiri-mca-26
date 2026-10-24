#!/usr/bin/env python3
"""Section B - Advanced SQL (4.1 Select, 4.2 Joins, 4.3 Views, 4.4 TCL/DCL).

Runs every query against the live library schema, caches the real output in
tools/.section_b_cache.json, and generates

    record/pages/b1_qNN.tex, b2_qNN.tex, b3_qNN.tex, b4_qNN.tex
    sql/B1_01_to_20_select.sql, B2_01_to_20_joins.sql,
    sql/B3_01_to_07_views.sql, B4_01_to_15_tcl_dcl.sql

Usage:
    python3 tools/gen_section_b.py            # render from cache
    python3 tools/gen_section_b.py --refresh  # re-run everything against the DB
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(ROOT, "sql")
PAGE_DIR = os.path.join(ROOT, "record", "pages")
CACHE = os.path.join(ROOT, "tools", ".section_b_cache.json")

CONN = "mca/mca@localhost:1521/FREEPDB1"

SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}


def prose(t):
    return "".join(SPECIAL.get(c, c) for c in t)


# --------------------------------------------------------------------------
# 4.1  SELECT queries   (library_select_questions.sql, first 20)
# --------------------------------------------------------------------------
SEL = [
    ("Display the member ID, full name, member type and city of all ACTIVE members, "
     "arranged first by member type and then alphabetically by name.",
     ["SELECT member_id, full_name, member_type, city",
      "FROM member",
      "WHERE status = 'ACTIVE'",
      "ORDER BY member_type, full_name;"]),

    ("List the members whose outstanding amount is between 50 and 300, inclusive. Show "
     "member ID, name, outstanding amount and status in descending order of outstanding amount.",
     ["SELECT member_id, full_name, outstanding_amt, status",
      "FROM member",
      "WHERE outstanding_amt BETWEEN 50 AND 300",
      "ORDER BY outstanding_amt DESC;"]),

    ("Display all members who are either STUDENT or RESEARCHER and whose maximum "
     "borrowing limit is at least 4 books. Sort by max_books descending.",
     ["SELECT member_id, full_name, member_type, max_books",
      "FROM member",
      "WHERE member_type IN ('RESEARCHER', 'STUDENT')",
      "  AND max_books >= 4",
      "ORDER BY max_books DESC;"]),

    ("Display member name, join date and the number of complete years they have been "
     "members as of SYSDATE. Show the longest-standing members first.",
     ["SELECT full_name, join_date,",
      "       TRUNC(MONTHS_BETWEEN(SYSDATE, join_date) / 12) AS completed_years",
      "FROM member",
      "ORDER BY completed_years DESC;"]),

    ("Display the names and email addresses of members whose name contains the letter "
     "'a' anywhere, ignoring case, and whose account is ACTIVE.",
     ["SELECT LOWER(full_name) AS name, email",
      "FROM member",
      "WHERE LOWER(full_name) LIKE '%a%'",
      "  AND status = 'ACTIVE';"]),

    ("Produce a member-status summary showing each status, the number of members in that "
     "status and the average outstanding amount for that status, rounded to two decimal places.",
     ["SELECT status, COUNT(*) AS no_of_members,",
      "       ROUND(AVG(outstanding_amt), 2) AS average_out_amt",
      "FROM member",
      "GROUP BY status;"]),

    ("Display cities having at least 2 registered members. Show the city, number of "
     "members and total outstanding amount for that city, arranged by number of members descending.",
     ["SELECT city, COUNT(*) AS no_of_members,",
      "       SUM(outstanding_amt) AS total_out_amt",
      "FROM member",
      "GROUP BY city",
      "HAVING COUNT(member_id) >= 2",
      "ORDER BY no_of_members DESC;"]),

    ("Display staff name, role, shift and salary for staff earning from 32,000 to 56,000 "
     "inclusive, excluding GENERAL shift staff. Sort from highest to lowest salary.",
     ["SELECT full_name, role_name, shift_name, salary",
      "FROM staff",
      "WHERE salary BETWEEN 32000 AND 56000",
      "  AND shift_name != 'GENERAL'",
      "ORDER BY salary DESC;"]),

    ("For each shift in the STAFF table, display the number of employees, minimum salary, "
     "maximum salary and average salary, rounded to two decimal places.",
     ["SELECT shift_name, COUNT(*) AS no_of_employees,",
      "       MIN(salary) AS min_salary, MAX(salary) AS max_salary,",
      "       ROUND(AVG(salary), 2) AS avg_salary",
      "FROM staff",
      "GROUP BY shift_name", "ORDER BY shift_name;"]),

    ("Display staff members hired before 1 January 2020 whose salary is above 50,000. "
     "Show staff ID, name, hire date and salary.",
     ["SELECT staff_id, full_name, hire_date, salary",
      "FROM staff",
      "WHERE hire_date < TO_DATE('01-01-2020', 'DD-MM-YYYY')",
      "  AND salary > 50000",
      "ORDER BY staff_id;"]),

    ("Display each publisher's name, country and age in years in 2026 "
     "(2026 - established_year). Show the oldest publishers first.",
     ["SELECT publisher_name, country,",
      "       (EXTRACT(YEAR FROM SYSDATE) - established_year) AS age",
      "FROM publisher",
      "ORDER BY age DESC;"]),

    ("Display countries that have at least two publishers in the database. "
     "Show country and number of publishers.",
     ["SELECT country, COUNT(*) AS no_of_publishers",
      "FROM publisher",
      "GROUP BY country",
      "HAVING COUNT(publisher_id) >= 2", "ORDER BY country;"]),

    ("Display authors born before 1960 who have received at least 2 awards. Show author "
     "name, nationality, birth year and awards count, ordered by awards count descending "
     "and then birth year ascending.",
     ["SELECT author_name, nationality, birth_year, awards_count",
      "FROM author",
      "WHERE birth_year < 1960",
      "  AND awards_count >= 2",
      "ORDER BY awards_count DESC, birth_year;"]),

    ("For each nationality in AUTHOR, display the number of authors and the total number "
     "of awards received. Include only nationalities whose total awards count is at least 5.",
     ["SELECT nationality, COUNT(*) AS no_of_authors,",
      "       SUM(awards_count) AS total_awards",
      "FROM author",
      "GROUP BY nationality",
      "HAVING SUM(awards_count) >= 5", "ORDER BY nationality;"]),

    ("Display book ID, title, category, publication year and price for books published "
     "from 2014 onward with price above 700. Sort by price descending.",
     ["SELECT book_id, title, category, publication_year, price",
      "FROM book",
      "WHERE publication_year >= 2014",
      "  AND price > 700",
      "ORDER BY price DESC;"]),

    ("Display books whose title contains either the word 'Data' or the word 'Learning', "
     "ignoring case. Show title, category, year, pages and rating.",
     ["SELECT title, category, publication_year, pages, rating",
      "FROM book",
      "WHERE LOWER(title) LIKE '%data%'",
      "   OR LOWER(title) LIKE '%learning%'",
      "ORDER BY book_id;"]),

    ("Display books with more than 500 pages and a rating of at least 4.5. Add a computed "
     "column named PRICE_PER_100_PAGES showing the approximate price per 100 pages, "
     "rounded to two decimals.",
     ["SELECT title, pages, rating,",
      "       ROUND((price / pages) * 100, 2) AS price_per_100_pages",
      "FROM book",
      "WHERE pages > 500",
      "  AND rating >= 4.5",
      "ORDER BY pages DESC;"]),

    ("Display the category-wise number of books, average price and average rating. Show "
     "only categories containing at least 2 books. Round averages to two decimals.",
     ["SELECT category, COUNT(*) AS no_of_books,",
      "       ROUND(AVG(price), 2) AS avg_price,",
      "       ROUND(AVG(rating), 2) AS avg_rating",
      "FROM book",
      "GROUP BY category",
      "HAVING COUNT(book_id) >= 2", "ORDER BY category;"]),

    ("Display publication years in which at least 2 books in the BOOK table were "
     "published. Show the year, number of books and average price.",
     ["SELECT publication_year, COUNT(*) AS no_of_books,",
      "       ROUND(AVG(price), 2) AS avg_price",
      "FROM book",
      "GROUP BY publication_year",
      "HAVING COUNT(book_id) >= 2",
      "ORDER BY publication_year;"]),

    ("Categorise every book using a CASE expression: price below 400 is BUDGET, price from "
     "400 to 799 is STANDARD and price 800 or above is PREMIUM. Display book title, price "
     "and the computed price category, sorted by price descending.",
     ["SELECT title, price,",
      "       CAST(CASE WHEN price < 400 THEN 'BUDGET'",
      "                 WHEN price BETWEEN 400 AND 799 THEN 'STANDARD'",
      "                 WHEN price >= 800 THEN 'PREMIUM'",
      "            END AS VARCHAR2(14)) AS price_category",
      "FROM book",
      "ORDER BY price DESC;"]),
]

# --------------------------------------------------------------------------
# 4.2  JOIN queries (DBMS_JOIN_LAB_Questions_library.docx, 20 of the 33)
# --------------------------------------------------------------------------
JOIN = [
    ("Display each book title along with its publisher name.",
     ["SELECT b.title, p.publisher_name",
      "FROM book b",
      "JOIN publisher p ON p.publisher_id = b.publisher_id",
      "ORDER BY b.book_id;"]),

    ("Display each library member's name, member type, and the name of the branch to "
     "which the member belongs.",
     ["SELECT m.full_name, m.member_type, br.branch_name",
      "FROM member m",
      "JOIN library_branch br ON br.branch_id = m.branch_id",
      "ORDER BY m.member_id;"]),

    ("Display the staff name, role, and branch name for all staff members.",
     ["SELECT s.full_name, s.role_name, br.branch_name",
      "FROM staff s",
      "JOIN library_branch br ON br.branch_id = s.branch_id",
      "ORDER BY s.staff_id;"]),

    ("Display each book title and the names of its authors.",
     ["SELECT b.title, a.author_name",
      "FROM book b",
      "JOIN book_author ba ON ba.book_id = b.book_id",
      "JOIN author a ON a.author_id = ba.author_id",
      "ORDER BY b.book_id, ba.author_order;"]),

    ("Display the reservation ID, member name, book title, and reservation status for "
     "all reservations.",
     ["SELECT r.reservation_id, m.full_name, b.title, r.reservation_status",
      "FROM reservation r",
      "JOIN member m ON m.member_id = r.member_id",
      "JOIN book b ON b.book_id = r.book_id",
      "ORDER BY r.reservation_id;"]),

    ("Display the fine ID, member name, loan ID, fine amount, and payment status for "
     "fines recorded in the library.",
     ["SELECT f.fine_id, m.full_name, f.loan_id, f.amount, f.payment_status",
      "FROM fine f",
      "JOIN member m ON m.member_id = f.member_id",
      "ORDER BY f.fine_id;"]),

    ("Display all library branches and the names of members registered at each branch. "
     "Include branches that have no members.",
     ["SELECT br.branch_name, m.full_name",
      "FROM library_branch br",
      "LEFT JOIN member m ON m.branch_id = br.branch_id",
      "ORDER BY br.branch_id, m.member_id;"]),

    ("Display all books and their physical copy IDs. Include books that do not have any "
     "physical copies.",
     ["SELECT b.title, c.copy_id",
      "FROM book b",
      "LEFT JOIN book_copy c ON c.book_id = b.book_id",
      "ORDER BY b.book_id, c.copy_id;"]),

    ("Display all members and their loan IDs. Include members who have never borrowed a book.",
     ["SELECT m.full_name, l.loan_id",
      "FROM member m",
      "LEFT JOIN loan l ON l.member_id = m.member_id",
      "ORDER BY m.member_id, l.loan_id;"]),

    ("Display all authors and the titles of books associated with them through "
     "BOOK_AUTHOR. Include authors who are not linked to any book.",
     ["SELECT a.author_name, b.title",
      "FROM author a",
      "LEFT JOIN book_author ba ON ba.author_id = a.author_id",
      "LEFT JOIN book b ON b.book_id = ba.book_id",
      "ORDER BY a.author_id, b.title;"]),

    ("Display all publishers and the titles of books published by them. Include "
     "publishers that have not published any books.",
     ["SELECT p.publisher_name, b.title",
      "FROM publisher p",
      "LEFT JOIN book b ON b.publisher_id = p.publisher_id",
      "ORDER BY p.publisher_id, b.book_id;"]),

    ("Display branch name, city, and staff name using a RIGHT OUTER JOIN. Include all "
     "branches, even if a branch has no staff.",
     ["SELECT br.branch_name, br.city, s.full_name",
      "FROM staff s",
      "RIGHT JOIN library_branch br ON br.branch_id = s.branch_id",
      "ORDER BY br.branch_id, s.staff_id;"]),

    ("Display book title, copy ID, and availability status using a RIGHT OUTER JOIN. "
     "Include all physical copies in BOOK_COPY.",
     ["SELECT b.title, c.copy_id, c.availability_status",
      "FROM book b",
      "RIGHT JOIN book_copy c ON c.book_id = b.book_id",
      "ORDER BY c.copy_id;"]),

    ("Display publisher name, book title, and price using a RIGHT OUTER JOIN. Include all "
     "books, even if a matching publisher record is not found.",
     ["SELECT p.publisher_name, b.title, b.price",
      "FROM publisher p",
      "RIGHT JOIN book b ON b.publisher_id = p.publisher_id",
      "ORDER BY b.book_id;"]),

    ("Display all library branches and all members, showing matching branch-member "
     "records, branches without members, and members without a matching branch.",
     ["SELECT br.branch_name, m.full_name",
      "FROM library_branch br",
      "FULL OUTER JOIN member m ON m.branch_id = br.branch_id",
      "ORDER BY br.branch_id, m.member_id;"]),

    ("Display all books and all reservations, including books that have never been "
     "reserved and reservation records without a matching book.",
     ["SELECT b.title, r.reservation_id",
      "FROM book b",
      "FULL OUTER JOIN reservation r ON r.book_id = b.book_id",
      "ORDER BY b.book_id, r.reservation_id;"]),

    ("Display all members and all fine records, including members without fines and fine "
     "records without a matching member.",
     ["SELECT m.full_name, f.fine_id",
      "FROM member m",
      "FULL OUTER JOIN fine f ON f.member_id = m.member_id",
      "ORDER BY m.member_id, f.fine_id;"]),

    ("Display book title, copy ID, and branch name using a NATURAL JOIN between "
     "BOOK_COPY and LIBRARY_BRANCH.",
     ["SELECT b.title, c.copy_id, l.branch_name",
      "FROM book_copy c",
      "NATURAL JOIN library_branch l",
      "JOIN book b ON b.book_id = c.book_id",
      "ORDER BY c.copy_id;"]),

    ("Display member name, book title, copy accession number, issue date, and loan status "
     "for books that have been loaned.",
     ["SELECT m.full_name, b.title, c.accession_no, l.issue_date, l.loan_status",
      "FROM loan l",
      "JOIN member m ON m.member_id = l.member_id",
      "JOIN book_copy c ON c.copy_id = l.copy_id",
      "JOIN book b ON b.book_id = c.book_id",
      "ORDER BY l.loan_id;"]),

    ("Display book title, publisher name, author name, and contribution role for books "
     "linked to authors.",
     ["SELECT b.title, p.publisher_name, a.author_name,",
      "       ba.contribution_role",
      "FROM book b",
      "JOIN publisher p ON p.publisher_id = b.publisher_id",
      "JOIN book_author ba ON ba.book_id = b.book_id",
      "JOIN author a ON a.author_id = ba.author_id",
      "ORDER BY b.book_id, ba.author_order;"]),
]

# --------------------------------------------------------------------------
# 4.3  Views
# --------------------------------------------------------------------------
VIEWS = [
    ("Create a view named BOOK_DETAILS to display the book ID, book title, publisher ID, "
     "and price from the BOOK table.",
     ["CREATE VIEW book_details AS",
      "SELECT book_id, title, publisher_id, price",
      "FROM book;"], "status"),

    ("Create a view named MEMBER_DETAILS to display the member ID, member name, member "
     "type, and status of all library members.",
     ["CREATE VIEW member_details AS",
      "SELECT member_id, full_name, member_type, status",
      "FROM member;"], "status"),

    ("Create a view named MEMBER_BRANCH_DETAILS to display member name, member type, "
     "branch name, and city by joining MEMBER and LIBRARY_BRANCH.",
     ["CREATE VIEW member_branch_details AS",
      "SELECT m.full_name, m.member_type, br.branch_name, br.city",
      "FROM member m",
      "JOIN library_branch br ON br.branch_id = m.branch_id;"], "status"),

    ("Create a view named BOOK_PUBLISHER_DETAILS to display book title, publisher name, "
     "and price by joining BOOK and PUBLISHER.",
     ["CREATE VIEW book_publisher_details AS",
      "SELECT b.title, p.publisher_name, b.price",
      "FROM book b",
      "JOIN publisher p ON p.publisher_id = b.publisher_id;"], "status"),

    ("Create a view named LOAN_DETAILS to display member name, book title, issue date, "
     "due date, and loan status by joining the appropriate tables.",
     ["CREATE VIEW loan_details AS",
      "SELECT m.full_name, b.title, l.issue_date, l.due_date, l.loan_status",
      "FROM loan l",
      "JOIN member m ON m.member_id = l.member_id",
      "JOIN book_copy c ON c.copy_id = l.copy_id",
      "JOIN book b ON b.book_id = c.book_id;"], "status"),

    ("Display the names and branch names of all members using the "
     "MEMBER_BRANCH_DETAILS view.",
     ["SELECT full_name, branch_name",
      "FROM member_branch_details",
      "ORDER BY full_name;"], "query"),

    ("Display books from the BOOK_PUBLISHER_DETAILS view whose price is greater than 500.",
     ["SELECT title, publisher_name, price",
      "FROM book_publisher_details",
      "WHERE price > 500",
      "ORDER BY price DESC;"], "query"),
]

# --------------------------------------------------------------------------
# 4.4  TCL and DCL
# --------------------------------------------------------------------------
TCL = [
    ("Increase the price of all books published by publisher 201 by 10%. Save the changes "
     "permanently using COMMIT.",
     ["UPDATE book SET price = price * 1.10",
      "WHERE publisher_id = 201;",
      "COMMIT;"]),

    ("Update the status of library member 1006 from EXPIRED to ACTIVE and permanently save "
     "the change using COMMIT.",
     ["UPDATE member SET status = 'ACTIVE'",
      "WHERE member_id = 1006 AND status = 'EXPIRED';",
      "COMMIT;"]),

    ("Update the availability status of book copy 6001 to REPAIR, so that it can no longer be issued. Commit the transaction.",
     ["UPDATE book_copy SET availability_status = 'REPAIR'",
      "WHERE copy_id = 6001;",
      "COMMIT;"]),

    ("Update the price of book 4001. Create a savepoint named price_update, perform "
     "another update on the same book, and then roll back to the price_update savepoint.",
     ["UPDATE book SET price = 500 WHERE book_id = 4001;",
      "SAVEPOINT price_update;",
      "UPDATE book SET price = 900 WHERE book_id = 4001;",
      "ROLLBACK TO price_update;"]),

    ("Perform the following operations in a single transaction: update the status of a "
     "member, create a savepoint named member_update, update the price of a book, roll "
     "back to member_update, and commit the transaction.",
     ["UPDATE member SET status = 'SUSPENDED' WHERE member_id = 1007;",
      "SAVEPOINT member_update;",
      "UPDATE book SET price = 1200 WHERE book_id = 4007;",
      "ROLLBACK TO member_update;",
      "COMMIT;"]),

    ("Perform two different updates on the BOOK table with a savepoint between them. Roll "
     "back only the second update using ROLLBACK TO SAVEPOINT.",
     ["UPDATE book SET price = 420 WHERE book_id = 4002;",
      "SAVEPOINT second_update;",
      "UPDATE book SET price = 780 WHERE book_id = 4005;",
      "ROLLBACK TO second_update;"]),

    ("Grant SELECT permission on the BOOK table to user LIBUSER.",
     ["GRANT SELECT ON book TO libuser;"]),

    ("Grant SELECT permission on the BOOK_DETAILS view to user LIBUSER.",
     ["GRANT SELECT ON book_details TO libuser;"]),

    ("Grant SELECT and INSERT privileges on the MEMBER table to user LIBUSER.",
     ["GRANT SELECT, INSERT ON member TO libuser;"]),

    ("Grant SELECT, UPDATE, and DELETE privileges on the BOOK_COPY table to user LIBUSER.",
     ["GRANT SELECT, UPDATE, DELETE ON book_copy TO libuser;"]),

    ("Grant SELECT permission on the MEMBER_BRANCH_DETAILS view to user LIBUSER.",
     ["GRANT SELECT ON member_branch_details TO libuser;"]),

    ("Revoke the SELECT privilege on the BOOK table from user LIBUSER.",
     ["REVOKE SELECT ON book FROM libuser;"]),

    ("Revoke the INSERT privilege on the MEMBER table from user LIBUSER.",
     ["REVOKE INSERT ON member FROM libuser;"]),

    ("Revoke the UPDATE and DELETE privileges on the BOOK_COPY table from user LIBUSER.",
     ["REVOKE UPDATE, DELETE ON book_copy FROM libuser;"]),

    ("Revoke all previously granted privileges on the BOOK_DETAILS view from user LIBUSER.",
     ["REVOKE ALL ON book_details FROM libuser;"]),
]

SECTIONS = [
    ("b1", SEL, "query", "B1_01_to_20_select.sql", "4.1  Select Queries"),
    ("b2", JOIN, "query", "B2_01_to_20_joins.sql", "4.2  Joins"),
    ("b3", VIEWS, "mixed", "B3_01_to_07_views.sql", "4.3  Views"),
    ("b4", TCL, "status", "B4_01_to_15_tcl_dcl.sql", "4.4  TCL and DCL Commands"),
]


# --------------------------------------------------------------------------
# running
# --------------------------------------------------------------------------
def sqlplus(script):
    p = subprocess.run(
        ["podman", "exec", "-i", "oracledb", "sqlplus", "-S", CONN],
        input=script, capture_output=True, text=True)
    return [l for l in p.stdout.splitlines()]


QUERY_PREAMBLE = """SET LINESIZE 32767
SET PAGESIZE 500
SET FEEDBACK OFF
SET UNDERLINE OFF
SET COLSEP '~'
SET TRIMSPOOL ON
SELECT '<<<BEGIN>>>' FROM dual;
"""

STATUS_PREAMBLE = """SET LINESIZE 200
SET PAGESIZE 100
SET FEEDBACK ON
SET ECHO OFF
SET VERIFY OFF
"""


def run_query(code):
    out = sqlplus(QUERY_PREAMBLE + "\n".join(code) + "\n")
    start = [i for i, l in enumerate(out) if "<<<BEGIN>>>" in l][0]
    body = [l for l in out[start + 1:] if l.strip()]
    if not body:
        return {"headers": [], "rows": []}
    headers = [c.strip() for c in body[0].split("~")]
    rows = []
    for line in body[1:]:
        fields = [c.strip() for c in line.split("~")]
        if len(fields) < len(headers):
            fields += [""] * (len(headers) - len(fields))
        rows.append(fields[:len(headers)])
    return {"headers": headers, "rows": rows}


def run_status(code):
    out = sqlplus(STATUS_PREAMBLE + "\n".join(code) + "\n")
    keep = []
    for l in out:
        s = l.strip()
        if not s or s.startswith("SQL>"):
            continue
        keep.append(s)
    return {"lines": keep}


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def is_number(s):
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", s))


def render(headers, rows):
    if not headers:
        return ["no rows selected."]
    widths = []
    numeric = []
    for i, h in enumerate(headers):
        vals = [r[i] for r in rows]
        widths.append(max([len(h)] + [len(v) for v in vals]))
        numeric.append(bool(vals) and all(v == "" or is_number(v) for v in vals))
    head = [h.rjust(w) if n else h.ljust(w)
            for h, w, n in zip(headers, widths, numeric)]
    out = ["  ".join(head), "  ".join("-" * w for w in widths)]
    for r in rows:
        cells = []
        for i, (v, w) in enumerate(zip(r, widths)):
            cells.append(v.rjust(w) if numeric[i] else v.ljust(w))
        out.append("  ".join(cells).rstrip())
    n = len(rows)
    out += ["", "%d row%s selected." % (n, "" if n == 1 else "s") if n else "no rows selected."]
    return out


def page(num, question, code, out_lines):
    longest = max((len(l) for l in out_lines), default=0)
    if longest <= 84:
        size = r"\small"
    elif longest <= 98:
        size = r"\footnotesize"
    elif longest <= 112:
        size = r"\scriptsize"
    else:
        size = r"\tiny"
    return r"""%% ---- Section B / question %(num)d
\noindent\begin{minipage}{\linewidth}
\begingroup\hyphenpenalty=10000\exhyphenpenalty=10000
{\fontsize{14}{17}\selectfont\textbf{%(num)d.}}\ %(q)s\par
\endgroup\vspace{12pt}

\codeheading{CODE:}

\begin{sqlcode}
%(code)s
\end{sqlcode}

\vspace{18pt}

\codeheading{OUTPUT:}

\begin{sqlout}[fontsize=%(size)s]
%(out)s
\end{sqlout}
\end{minipage}\par\vspace{24pt}

""" % dict(num=num, q=prose(question), code="\n".join(code),
           out="\n".join(out_lines), size=size)


def main():
    refresh = "--refresh" in sys.argv
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE))

    for prefix, items, kind, sqlname, _title in SECTIONS:
        parts = ["-- ============================================================\n"
                 "-- Section B : %s\n"
                 "-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1\n"
                 "-- ============================================================\n\n" % _title]
        for i, item in enumerate(items, 1):
            question, code = item[0], item[1]
            qkind = item[2] if len(item) > 2 else ("query" if kind in ("query",) else kind)
            if kind == "mixed":
                qkind = item[2]
            key = "%s_q%02d" % (prefix, i)
            if refresh or key not in cache:
                cache[key] = run_query(code) if qkind == "query" else run_status(code)
            res = cache[key]
            if qkind == "query":
                out = render(res["headers"], res["rows"])
            else:
                out = res["lines"]
            with open(os.path.join(PAGE_DIR, "%s_q%02d.tex" % (prefix, i)), "w") as f:
                f.write(page(i, question, code, out))
            parts.append("\nPROMPT\nPROMPT ===== Q%d =====\n\n%s\n" % (i, "\n".join(code)))
        with open(os.path.join(SQL_DIR, sqlname), "w") as f:
            f.write("".join(parts))

    json.dump(cache, open(CACHE, "w"), indent=1)
    print("generated %d pages" % sum(len(s[1]) for s in SECTIONS))


if __name__ == "__main__":
    main()
