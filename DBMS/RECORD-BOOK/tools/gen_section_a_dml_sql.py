#!/usr/bin/env python3
"""Section A, parts 2 (DML) and 3 (Basic SQL).

Emits:
  sql/A2_01_to_20_dml.sql
  sql/A3_00_seed.sql
  sql/A3_01_to_20_basic_sql.sql
  record/pages/a2_q01..20.tex, a3_q01..20.tex
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(ROOT, "sql")
PAGE_DIR = os.path.join(ROOT, "record", "pages")
CAPTURE = os.path.join(ROOT, "tools", ".section_a_capture.json")

SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}


def prose(t):
    return "".join(SPECIAL.get(c, c) for c in t)


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
    return r"""%% ---- Section A / question %(num)d
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


# ---------------------------------------------------------------- dataset
# state of the tables after the DML section + seed script
DEPTS = ["D01", "D02", "D03", "D04", "D05"]

STUDENTS = [
    ("S101", "Akhil Raj", "M", 8.7, "D01", "akhil@gmail.com"),
    ("S102", "Neha Thomas", "F", None, "D01", "neha@gmail.com"),
    ("S103", "Anjali Menon", "F", 9.1, "D01", "anjali@rajagiri.edu"),
    ("S104", "Arjun Nair", "M", 8.4, "D02", "arjun@gmail.com"),
    ("S105", "Aparna Pillai", "F", 7.2, "D01", "aparna@gmail.com"),
    ("S106", "Rahul Varma", "M", 6.5, "D03", "rahul@gmail.com"),
    ("S107", "Sneha George", "F", 8.9, "D02", "sneha@gmail.com"),
    ("S108", "Aditya Kumar", "M", 5.8, "D04", "aditya@gmail.com"),
    ("S109", "Meera Krishnan", "F", 9.6, "D01", "meera.k@rajagiri.edu"),
    ("S110", "Anoop Joseph", "M", 7.8, "D05", "anoop@gmail.com"),
    ("S111", "Divya Ramesh", "F", 8.0, "D03", "divya@gmail.com"),
    ("S112", "Kiran Mathew", "M", 6.9, "D04", "kiran@gmail.com"),
]

FACULTY = [
    ("F102", "Ravi Kumar", "Assistant Professor", 27500, "ravi@rajagiri.edu", "D01", None),
    ("F103", "Anita Thomas", "Professor", 99000, "anita@rajagiri.edu", "D01", None),
    ("F101", "Meera Joseph", "Assistant Professor", 60500, "meera@rajagiri.edu", "D01", None),
    ("F104", "Suresh Menon", "Professor", 95000, "suresh@rajagiri.edu", "D02", 18),
    ("F105", "Latha Nair", "Associate Professor", 72000, "latha@rajagiri.edu", "D03", 11),
    ("F106", "Vinod Kumar", "Assistant Professor", 48000, "vinod@gmail.com", "D04", 6),
    ("F107", "Priya Sharma", "Assistant Professor", 52000, "priya@rajagiri.edu", "D05", 5),
    ("F108", "arun das", "Assistant Professor", 45000, "arun@yahoo.com", "D01", 3),
]

COURSES = [
    ("C101", "Database Management Systems", 5, 3, "D01", "F101"),
    ("C103", "Data Structures", 4, 3, "D01", "F106"),
    ("C104", "Digital Electronics", 3, 1, "D02", "F104"),
    ("C105", "Thermodynamics", 4, 3, "D03", "F105"),
    ("C106", "Surveying", 3, 5, "D04", "F106"),
    ("C107", "Operating Systems", 4, 5, "D01", "F107"),
    ("C108", "Computer Networks", 3, 7, "D01", "F108"),
    ("C109", "Software Engineering", 4, 5, "D01", "F101"),
    ("C110", "Web Technologies", 2, 1, "D05", "F107"),
]

RESULTS = [
    ("R102", "E102", 45, 40, "A", "PASS"), ("R103", "E103", 38, 35, "B", "PASS"),
    ("R104", "E104", 42, 38, "A", "PASS"), ("R105", "E105", 25, 20, "F", "FAIL"),
    ("R106", "E106", 30, 28, "C", "PASS"), ("R107", "E107", 48, 45, "A", "PASS"),
    ("R108", "E108", 35, 30, "B", "PASS"), ("R109", "E109", 20, 15, "F", "FAIL"),
    ("R110", "E110", 40, 42, "A", "PASS"), ("R111", "E111", 28, 25, "C", "PASS"),
    ("R112", "E112", 44, 41, "A", "PASS"), ("R113", "E113", 33, 32, "B", "PASS"),
    ("R114", "E114", 22, 18, "F", "FAIL"), ("R115", "E115", 46, 44, "A", "PASS"),
]
RESULTS = [(r, e, i, x, i + x, g, st) for r, e, i, x, g, st in RESULTS]

EVENTS = [
    ("EV01", "Tech Fest", "15-MAR-26", "Main Auditorium", "F101", 150, 200),
    ("EV03", "National Seminar", "20-NOV-25", "Seminar Hall", "F103", 300, 100),
    ("EV04", "Cultural Fest", "10-FEB-26", "Open Ground", "F105", 500, 750),
    ("EV05", "Sports Meet", "20-JAN-26", "Sports Complex", "F106", 200, 0),
    ("EV06", "Alumni Meet", "05-DEC-25", "Main Auditorium", "F104", 80, 1500),
]


def sel(rows):
    n = len(rows)
    return ["", "%d row%s selected." % (n, "" if n == 1 else "s")]


def render_db(headers, rows, types, sep="  "):
    """Render the live SELECT * result the way sqlplus lays it out.

    Text columns are left aligned and NUMBER columns right aligned, matching
    SQL*Plus; the space between columns is squeezed to one character only when
    two would push the block past the text width.
    """
    widths = [max([len(h)] + [len(r[i]) for r in rows])
              for i, h in enumerate(headers)]
    numeric = [t == "NUMBER" for t in types]
    head = [h.rjust(w) if n else h.ljust(w)
            for h, w, n in zip(headers, widths, numeric)]
    out = [sep.join(head), sep.join("-" * w for w in widths)]
    for r in rows:
        cells = [v.rjust(w) if n else v.ljust(w)
                 for v, w, n in zip(r, widths, numeric)]
        out.append(sep.join(cells).rstrip())
    return out + sel(rows)


def render_select(headers, rows, types):
    out = render_db(headers, rows, types)
    if max((len(l) for l in out), default=0) > 116:
        out = render_db(headers, rows, types, sep=" ")
    return out


def _s(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def render(headers, rows, numeric=()):
    widths = []
    for i, h in enumerate(headers):
        w = max([len(h)] + [len(_s(r[i])) for r in rows])
        widths.append(w)
    head = [h.rjust(w) if i in numeric else h.ljust(w)
            for i, (h, w) in enumerate(zip(headers, widths))]
    out = ["  ".join(head), "  ".join("-" * w for w in widths)]
    for r in rows:
        cells = []
        for i, (v, w) in enumerate(zip(r, widths)):
            t = _s(v)
            cells.append(t.rjust(w) if i in numeric else t.ljust(w))
        out.append("  ".join(cells).rstrip())
    return out


# ---------------------------------------------------------------- DML
DML = [
    (1, "Insert a new department with Department ID D01, Department Name Computer Science, "
        "Office Location Carmel Block and Contact Number 9876543210.",
     ["INSERT INTO department (dept_id, dept_name, office_location, contact_number)",
      "VALUES ('D01', 'Computer Science', 'Carmel Block', '9876543210');"],
     ["1 row created."]),
    (2, "Insert the student record of Akhil Raj (S101) into the STUDENT table.",
     ["INSERT INTO student (student_id, student_name, dob, gender, contact_number,",
      "                     email_id, dept_id, admission_date, cgpa)",
      "VALUES ('S101', 'Akhil Raj', TO_DATE('15-08-2005', 'DD-MM-YYYY'), 'M',",
      "        '9876501234', 'akhil@gmail.com', 'D01', SYSDATE, 8.2);"],
     ["1 row created."]),
    (3, "Insert a student record without providing the CGPA value.",
     ["INSERT INTO student (student_id, student_name, dob, gender, contact_number,",
      "                     email_id, dept_id, admission_date)",
      "VALUES ('S102', 'Neha Thomas', TO_DATE('22-03-2006', 'DD-MM-YYYY'), 'F',",
      "        '9876501235', 'neha@gmail.com', 'D01', SYSDATE);"],
     ["1 row created."]),
    (4, "Insert two faculty records into the FACULTY table using a single INSERT ALL statement.",
     ["INSERT ALL",
      "  INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,",
      "                email_id, dept_id)",
      "  VALUES ('F102', 'Ravi Kumar', 'Assistant Professor', TO_DATE('10-07-2024','DD-MM-YYYY'),",
      "          25000, 'ravi@rajagiri.edu', 'D01')",
      "  INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,",
      "                email_id, dept_id)",
      "  VALUES ('F103', 'Anita Thomas', 'Professor', TO_DATE('01-06-2011','DD-MM-YYYY'),",
      "          90000, 'anita@rajagiri.edu', 'D01')",
      "SELECT * FROM dual;"],
     ["2 rows created."]),
    (5, "Insert the faculty member Meera Joseph (F101) into the FACULTY table.",
     ["INSERT INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,",
      "                     email_id, dept_id)",
      "VALUES ('F101', 'Meera Joseph', 'Assistant Professor', TO_DATE('01-06-2022','DD-MM-YYYY'),",
      "        55000, 'meera@rajagiri.edu', 'D01');"],
     ["1 row created."]),
    (6, "Insert a course titled Database Management Systems with four credits for Semester 3.",
     ["INSERT INTO course (course_id, course_title, credits, semester, dept_id, faculty_id)",
      "VALUES ('C101', 'Database Management Systems', 4, 3, 'D01', 'F101');"],
     ["1 row created."]),
    (7, "Insert a course without mentioning the column names. Ensure that the values are "
        "entered in the correct table-column order.",
     ["INSERT INTO course",
      "VALUES ('C102', 'Operating Systems', 3, 8, 'D01', 'F102');"],
     ["1 row created."]),
    (8, "Insert an enrollment record and allow the enrollment_date column to take its "
        "default value.",
     ["INSERT INTO enrollment (enrollment_id, student_id, course_id, academic_year)",
      "VALUES ('E101', 'S101', 'C101', '2025-2026');"],
     ["1 row created."]),
    (9, "Insert a result record where the total marks are calculated by adding the "
        "internal and external marks.",
     ["INSERT INTO result (result_id, enrollment_id, internal_marks, external_marks,",
      "                    total_marks, grade, result_status)",
      "VALUES ('R101', 'E101', 18, 22, 18 + 22, 'F', 'FAIL');"],
     ["1 row created."]),
    (10, "Insert three events into the EVENT table using an Oracle INSERT ALL statement.",
     ["INSERT ALL",
      "  INTO event VALUES ('EV01', 'Tech Fest', TO_DATE('15-03-2026','DD-MM-YYYY'),",
      "                     'Main Auditorium', 'F101', 150, 200)",
      "  INTO event VALUES ('EV02', 'Workshop on AI', TO_DATE('10-04-2024','DD-MM-YYYY'),",
      "                     'Seminar Hall', 'F102', 50, NULL)",
      "  INTO event VALUES ('EV03', 'National Seminar', TO_DATE('20-11-2025','DD-MM-YYYY'),",
      "                     'Seminar Hall', 'F103', 300, 100)",
      "SELECT * FROM dual;"],
     ["3 rows created."]),
    (11, "Insert an event-registration record and allow the registration date to take "
         "the current date automatically.",
     ["INSERT INTO event_registration (registration_id, event_id, student_id,",
      "                               participation_status)",
      "VALUES ('REG01', 'EV01', 'S101', 'ABSENT');"],
     ["1 row created."]),
    (12, "Update the CGPA of student S101 to 8.7.",
     ["UPDATE student SET cgpa = 8.7 WHERE student_id = 'S101';"],
     ["1 row updated."]),
    (13, "Increase the salary of all faculty members by 10%.",
     ["UPDATE faculty SET salary = salary * 1.10;"],
     ["3 rows updated."]),
    (14, "Change the office location of the Computer Science department to "
         "Golden Aureole Block.",
     ["UPDATE department SET office_location = 'Golden Aureole Block'",
      "WHERE dept_name = 'Computer Science';"],
     ["1 row updated."]),
    (15, "Update the credits of the course Database Management Systems from 4 to 5.",
     ["UPDATE course SET credits = 5",
      "WHERE course_title = 'Database Management Systems';"],
     ["1 row updated."]),
    (16, "Set the result status to PASS for results with total marks greater than or "
         "equal to 50, and FAIL for the remaining records.",
     ["UPDATE result",
      "SET result_status = CASE WHEN total_marks >= 50 THEN 'PASS' ELSE 'FAIL' END;"],
     ["1 row updated."]),
    (17, "Delete courses offered in Semester 8.",
     ["DELETE FROM course WHERE semester = 8;"],
     ["1 row deleted."]),
    (18, "Delete all results with the result status FAIL.",
     ["DELETE FROM result WHERE result_status = 'FAIL';"],
     ["1 row deleted."]),
    (19, "Delete event registrations where the participation status is ABSENT.",
     ["DELETE FROM event_registration WHERE participation_status = 'ABSENT';"],
     ["1 row deleted."]),
    (20, "Delete all events for which no registration fee is charged.",
     ["DELETE FROM event WHERE registration_fee IS NULL OR registration_fee = 0;"],
     ["1 row deleted."]),
]


# ---------------------------------------------------------------- seed data
SEED_SQL = """-- ============================================================
-- Section A : sample data used by the Basic SQL section
-- Run after A2_01_to_20_dml.sql and before A3_01_to_20_basic_sql.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100

INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D02', 'Electronics', 'Block B', '9876500002');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D03', 'Mechanical', 'Block C', '9876500003');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D04', 'Civil', 'Block D', '9876500004');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D05', 'Information Tech', 'Block E', '9876500005');

INSERT INTO faculty VALUES
  ('F104', 'Suresh Menon', 'Professor', TO_DATE('12-07-2008','DD-MM-YYYY'), 95000, 'suresh@rajagiri.edu', 'D02', 18);
INSERT INTO faculty VALUES
  ('F105', 'Latha Nair', 'Associate Professor', TO_DATE('05-08-2015','DD-MM-YYYY'), 72000, 'latha@rajagiri.edu', 'D03', 11);
INSERT INTO faculty VALUES
  ('F106', 'Vinod Kumar', 'Assistant Professor', TO_DATE('18-01-2020','DD-MM-YYYY'), 48000, 'vinod@gmail.com', 'D04', 6);
INSERT INTO faculty VALUES
  ('F107', 'Priya Sharma', 'Assistant Professor', TO_DATE('02-03-2021','DD-MM-YYYY'), 52000, 'priya@rajagiri.edu', 'D05', 5);
INSERT INTO faculty VALUES
  ('F108', 'arun das', 'Assistant Professor', TO_DATE('15-06-2023','DD-MM-YYYY'), 45000, 'arun@yahoo.com', 'D01', 3);

INSERT INTO student VALUES
  ('S103', 'Anjali Menon', TO_DATE('11-02-2006','DD-MM-YYYY'), 'F', '9876501236', 'anjali@rajagiri.edu', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 9.1, 'Kochi', 'Kerala');
INSERT INTO student VALUES
  ('S104', 'Arjun Nair', TO_DATE('19-05-2005','DD-MM-YYYY'), 'M', '9876501237', 'arjun@gmail.com', 'D02', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.4, 'Thrissur', 'Kerala');
INSERT INTO student VALUES
  ('S105', 'Aparna Pillai', TO_DATE('23-09-2006','DD-MM-YYYY'), 'F', '9876501238', 'aparna@gmail.com', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 7.2, 'Alappuzha', 'Kerala');
INSERT INTO student VALUES
  ('S106', 'Rahul Varma', TO_DATE('07-12-2005','DD-MM-YYYY'), 'M', '9876501239', 'rahul@gmail.com', 'D03', TO_DATE('01-08-2025','DD-MM-YYYY'), 6.5, 'Kottayam', 'Kerala');
INSERT INTO student VALUES
  ('S107', 'Sneha George', TO_DATE('30-01-2006','DD-MM-YYYY'), 'F', '9876501240', 'sneha@gmail.com', 'D02', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.9, 'Ernakulam', 'Kerala');
INSERT INTO student VALUES
  ('S108', 'Aditya Kumar', TO_DATE('14-07-2005','DD-MM-YYYY'), 'M', '9876501241', 'aditya@gmail.com', 'D04', TO_DATE('01-08-2025','DD-MM-YYYY'), 5.8, 'Palakkad', 'Kerala');
INSERT INTO student VALUES
  ('S109', 'Meera Krishnan', TO_DATE('02-04-2006','DD-MM-YYYY'), 'F', '9876501242', 'meera.k@rajagiri.edu', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 9.6, 'Kochi', 'Kerala');
INSERT INTO student VALUES
  ('S110', 'Anoop Joseph', TO_DATE('27-10-2005','DD-MM-YYYY'), 'M', '9876501243', 'anoop@gmail.com', 'D05', TO_DATE('01-08-2025','DD-MM-YYYY'), 7.8, 'Idukki', 'Kerala');
INSERT INTO student VALUES
  ('S111', 'Divya Ramesh', TO_DATE('08-06-2006','DD-MM-YYYY'), 'F', '9876501244', 'divya@gmail.com', 'D03', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.0, 'Kollam', 'Kerala');
INSERT INTO student VALUES
  ('S112', 'Kiran Mathew', TO_DATE('16-03-2005','DD-MM-YYYY'), 'M', '9876501245', 'kiran@gmail.com', 'D04', TO_DATE('01-08-2025','DD-MM-YYYY'), 6.9, 'Thiruvananthapuram', 'Kerala');

INSERT INTO course VALUES
  ('C103', 'Data Structures', 4, 3, 'D01', 'F106');
INSERT INTO course VALUES
  ('C104', 'Digital Electronics', 3, 1, 'D02', 'F104');
INSERT INTO course VALUES
  ('C105', 'Thermodynamics', 4, 3, 'D03', 'F105');
INSERT INTO course VALUES
  ('C106', 'Surveying', 3, 5, 'D04', 'F106');
INSERT INTO course VALUES
  ('C107', 'Operating Systems', 4, 5, 'D01', 'F107');
INSERT INTO course VALUES
  ('C108', 'Computer Networks', 3, 7, 'D01', 'F108');
INSERT INTO course VALUES
  ('C109', 'Software Engineering', 4, 5, 'D01', 'F101');
INSERT INTO course VALUES
  ('C110', 'Web Technologies', 2, 1, 'D05', 'F107');

INSERT INTO enrollment VALUES ('E102', 'S103', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E103', 'S104', 'C104', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E104', 'S105', 'C103', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E105', 'S106', 'C105', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E106', 'S107', 'C107', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E107', 'S108', 'C108', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E108', 'S109', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E109', 'S110', 'C110', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E110', 'S111', 'C106', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E111', 'S112', 'C109', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E112', 'S103', 'C104', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E113', 'S107', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E114', 'S109', 'C107', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E115', 'S111', 'C103', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');

INSERT INTO result VALUES ('R102', 'E102', 45, 40, 85, 'A', 'PASS');
INSERT INTO result VALUES ('R103', 'E103', 38, 35, 73, 'B', 'PASS');
INSERT INTO result VALUES ('R104', 'E104', 42, 38, 80, 'A', 'PASS');
INSERT INTO result VALUES ('R105', 'E105', 25, 20, 45, 'F', 'FAIL');
INSERT INTO result VALUES ('R106', 'E106', 30, 28, 58, 'C', 'PASS');
INSERT INTO result VALUES ('R107', 'E107', 48, 45, 93, 'A', 'PASS');
INSERT INTO result VALUES ('R108', 'E108', 35, 30, 65, 'B', 'PASS');
INSERT INTO result VALUES ('R109', 'E109', 20, 15, 35, 'F', 'FAIL');
INSERT INTO result VALUES ('R110', 'E110', 40, 42, 82, 'A', 'PASS');
INSERT INTO result VALUES ('R111', 'E111', 28, 25, 53, 'C', 'PASS');
INSERT INTO result VALUES ('R112', 'E112', 44, 41, 85, 'A', 'PASS');
INSERT INTO result VALUES ('R113', 'E113', 33, 32, 65, 'B', 'PASS');
INSERT INTO result VALUES ('R114', 'E114', 22, 18, 40, 'F', 'FAIL');
INSERT INTO result VALUES ('R115', 'E115', 46, 44, 90, 'A', 'PASS');

INSERT INTO event VALUES ('EV04', 'Cultural Fest', TO_DATE('10-02-2026','DD-MM-YYYY'), 'Open Ground', 'F105', 500, 750);
INSERT INTO event VALUES ('EV05', 'Sports Meet', TO_DATE('20-01-2026','DD-MM-YYYY'), 'Sports Complex', 'F106', 200, 0);
INSERT INTO event VALUES ('EV06', 'Alumni Meet', TO_DATE('05-12-2025','DD-MM-YYYY'), 'Main Auditorium', 'F104', 80, 1500);

INSERT INTO event_registration VALUES ('REG02', 'EV01', 'S103', TO_DATE('10-03-2026','DD-MM-YYYY'), 'REGISTERED');
INSERT INTO event_registration VALUES ('REG03', 'EV01', 'S104', TO_DATE('10-03-2026','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG04', 'EV03', 'S105', TO_DATE('15-11-2025','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG05', 'EV04', 'S107', TO_DATE('01-02-2026','DD-MM-YYYY'), 'REGISTERED');
INSERT INTO event_registration VALUES ('REG06', 'EV04', 'S109', TO_DATE('02-02-2026','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG07', 'EV06', 'S103', TO_DATE('28-11-2025','DD-MM-YYYY'), 'ATTENDED');

COMMIT;
"""


# ---------------------------------------------------------------- basic SQL
def q_distinct_desig():
    rows = [(d,) for d in dict.fromkeys(f[2] for f in FACULTY)]
    return "SELECT DISTINCT designation FROM faculty;", ["DESIGNATION"], rows, ()


def q_distinct_sem():
    rows = [(s,) for s in dict.fromkeys(c[3] for c in COURSES)]
    return "SELECT DISTINCT semester FROM course;", ["SEMESTER"], rows, (0,)


def q_alias():
    rows = [(s[1], s[3]) for s in STUDENTS]
    return ("SELECT student_name AS Student_Name, cgpa AS Grade_Point_Average\nFROM student;",
            ["STUDENT_NAME", "GRADE_POINT_AVERAGE"], rows, ())


def q_annual():
    rows = [(f[1], f[3], f[3] * 12) for f in FACULTY]
    return ("SELECT faculty_name, salary, salary * 12 AS annual_salary\nFROM faculty;",
            ["FACULTY_NAME", "SALARY", "ANNUAL_SALARY"], rows, (1, 2))


def q_raise():
    rows = [(f[1], f[3], round(f[3] * 1.10)) for f in FACULTY]
    return ("SELECT faculty_name, salary, salary * 1.10 AS increased_salary\nFROM faculty;",
            ["FACULTY_NAME", "SALARY", "INCREASED_SALARY"], rows, (1, 2))


def q_total():
    rows = [(r[0], r[2], r[3], r[4]) for r in RESULTS]
    return ("SELECT result_id, internal_marks, external_marks,\n"
            "       internal_marks + external_marks AS total\nFROM result;",
            ["RESULT_ID", "INTERNAL_MARKS", "EXTERNAL_MARKS", "TOTAL"], rows, (1, 2, 3))


def q_tax():
    rows = [(e[1], e[6], round(e[6] * 1.18, 2)) for e in EVENTS]
    return ("SELECT event_name, registration_fee,\n"
            "       registration_fee * 1.18 AS fee_with_tax\nFROM event;",
            ["EVENT_NAME", "REGISTRATION_FEE", "FEE_WITH_TAX"], rows, (1, 2))


FAC_JOIN = {"F101": "01-JUN-22", "F102": "10-JUL-24", "F103": "01-JUN-11",
            "F104": "12-JUL-08", "F105": "05-AUG-15", "F106": "18-JAN-20",
            "F107": "02-MAR-21", "F108": "15-JUN-23"}


def q_salary_gt():
    rows = [(f[0], f[1], f[2], FAC_JOIN[f[0]], f[3], f[4], f[5], f[6])
            for f in FACULTY if f[3] > 50000]
    return ("SELECT * FROM faculty WHERE salary > 50000;",
            ["FACULTY_ID", "FACULTY_NAME", "DESIGNATION", "JOINING_DATE", "SALARY",
             "EMAIL_ID", "DEPT_ID", "EXPERIENCE_YEARS"], rows, (4, 7))


def q_course_sem3():
    rows = [(c[0], c[1], c[2], c[3], c[4], c[5]) for c in COURSES if c[3] == 3]
    return ("SELECT * FROM course WHERE semester = 3;",
            ["COURSE_ID", "COURSE_TITLE", "CREDITS", "SEMESTER", "DEPT_ID", "FACULTY_ID"],
            rows, (2, 3))


def q_result_ge80():
    rows = [r for r in RESULTS if r[4] >= 80]
    return ("SELECT * FROM result WHERE total_marks >= 80;",
            ["RESULT_ID", "ENROLLMENT_ID", "INTERNAL_MARKS", "EXTERNAL_MARKS",
             "TOTAL_MARKS", "GRADE", "RESULT_STATUS"],
            rows, (2, 3, 4))


def q_event_fee():
    rows = [e for e in EVENTS if e[6] > 500]
    return ("SELECT * FROM event WHERE registration_fee > 500;",
            ["EVENT_ID", "EVENT_NAME", "EVENT_DATE", "VENUE", "FACULTY_ID",
             "MAX_PARTICIPANTS", "REGISTRATION_FEE"],
            rows, (5, 6))


def q_cgpa_between():
    rows = [(s[0], s[1], s[3], s[4]) for s in STUDENTS if s[3] is not None and 7 <= s[3] <= 9]
    return ("SELECT student_id, student_name, cgpa, dept_id\n"
            "FROM student WHERE cgpa BETWEEN 7 AND 9;",
            ["STUDENT_ID", "STUDENT_NAME", "CGPA", "DEPT_ID"], rows, (2,))


def q_in_sem():
    rows = [(c[0], c[1], c[3]) for c in COURSES if c[3] in (1, 3, 5)]
    return ("SELECT course_id, course_title, semester\n"
            "FROM course WHERE semester IN (1, 3, 5);",
            ["COURSE_ID", "COURSE_TITLE", "SEMESTER"], rows, (2,))


def q_like_a():
    rows = [(s[0], s[1], s[3]) for s in STUDENTS if s[1].startswith("A")]
    return ("SELECT student_id, student_name, cgpa\n"
            "FROM student WHERE student_name LIKE 'A%';",
            ["STUDENT_ID", "STUDENT_NAME", "CGPA"], rows, (2,))


def q_email():
    rows = [(f[0], f[1], f[4]) for f in FACULTY if f[4].endswith("@rajagiri.edu")]
    return ("SELECT faculty_id, faculty_name, email_id\n"
            "FROM faculty WHERE email_id LIKE '%@rajagiri.edu';",
            ["FACULTY_ID", "FACULTY_NAME", "EMAIL_ID"], rows, ())


def q_null():
    rows = [(s[0], s[1]) for s in STUDENTS if s[3] is None]
    return ("SELECT student_id, student_name\n"
            "FROM student WHERE cgpa IS NULL;",
            ["STUDENT_ID", "STUDENT_NAME"], rows, ())


def q_upper():
    rows = [(s[1].upper(),) for s in STUDENTS]
    return ("SELECT UPPER(student_name) AS student_name FROM student;",
            ["STUDENT_NAME"], rows, ())


def q_initcap():
    rows = [(f[1].title(),) for f in FACULTY]
    return ("SELECT INITCAP(faculty_name) AS faculty_name FROM faculty;",
            ["FACULTY_NAME"], rows, ())


def q_length():
    rows = [(s[1], len(s[1])) for s in STUDENTS]
    return ("SELECT student_name, LENGTH(student_name) AS name_length\nFROM student;",
            ["STUDENT_NAME", "NAME_LENGTH"], rows, (1,))


def q_count():
    return ("SELECT COUNT(*) AS total_students FROM student;",
            ["TOTAL_STUDENTS"], [(len(STUDENTS),)], (0,))


def q_cgpa_stats():
    vals = [s[3] for s in STUDENTS if s[3] is not None]
    avg = sum(vals) / len(vals)
    return ("SELECT MAX(cgpa) AS highest, MIN(cgpa) AS lowest,\n"
            "       AVG(cgpa) AS average\nFROM student;",
            ["HIGHEST", "LOWEST", "AVERAGE"], [(max(vals), min(vals), round(avg, 2))], (0, 1, 2))


SQLQ = [
    (1, "Display the different faculty designations without duplicates.", q_distinct_desig),
    (2, "Display the different semesters in which courses are offered.", q_distinct_sem),
    (3, "Display the student name and CGPA using the aliases Student_Name and "
        "Grade_Point_Average.", q_alias),
    (4, "Display the faculty name, monthly salary, and annual salary. Calculate annual "
        "salary as monthly salary multiplied by 12.", q_annual),
    (5, "Display the faculty name, current salary, and salary after a 10% increase "
        "without modifying the table.", q_raise),
    (6, "Display the result ID, internal marks, external marks, and a calculated total "
        "obtained by adding the two marks.", q_total),
    (7, "Display the event name, registration fee, and registration fee after adding "
        "18% tax.", q_tax),
    (8, "Display faculty members whose salary is greater than 50,000.", q_salary_gt),
    (9, "Display courses offered in Semester 3.", q_course_sem3),
    (10, "Display results in which total marks are greater than or equal to 80.",
     q_result_ge80),
    (11, "Display events for which the registration fee is greater than 500.", q_event_fee),
    (12, "Display students whose CGPA is between 7 and 9.", q_cgpa_between),
    (13, "Display courses offered in Semesters 1, 3, or 5 using the IN operator.",
     q_in_sem),
    (14, "Display students whose names begin with the letter A.", q_like_a),
    (15, "Display faculty members whose email addresses belong to the rajagiri.edu "
         "domain.", q_email),
    (16, "Display students whose CGPA has not been entered.", q_null),
    (17, "Display all student names in uppercase.", q_upper),
    (18, "Display faculty names with the first letter of each word capitalised using "
         "INITCAP.", q_initcap),
    (19, "Display student names along with the number of characters in each name.",
     q_length),
    (20, "Find the total number of students, and the highest, lowest and average CGPA "
         "of all students.", None),
]


def main():
    # DML pages + script
    parts = ["""-- ============================================================
-- Section A : Basic DML Commands
-- Questions 1-20  (lab exercise Parts A, B and D)
-- Prerequisite: A1_01_department.sql, A1_02_to_08_tables.sql,
--               A1_02_to_21_alter.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100
SET FEEDBACK ON
"""]
    cap = json.load(open(CAPTURE))["dml"]
    for num, question, code, out in DML:
        entry = cap["%02d" % num]
        code = list(code)
        if code[0].upper().startswith("INSERT"):
            table = re.search(r"INTO\s+(\w+)", "\n".join(code), re.I).group(1)
            code.append("")
            code.append("SELECT * FROM %s;" % table)
            out = render_select(entry["headers"], entry["rows"], entry["types"])
        else:
            out = entry["status"]
        with open(os.path.join(PAGE_DIR, "a2_q%02d.tex" % num), "w") as f:
            f.write(page(num, question, code, out))
        parts.append("\nPROMPT\nPROMPT ===== Q%d =====\n\n%s\n" % (num, "\n".join(code)))
    parts.append("\nCOMMIT;\n")
    with open(os.path.join(SQL_DIR, "A2_01_to_20_dml.sql"), "w") as f:
        f.write("".join(parts))

    with open(os.path.join(SQL_DIR, "A3_00_seed.sql"), "w") as f:
        f.write(SEED_SQL)

    # Basic SQL pages + script
    parts = ["""-- ============================================================
-- Section A : Basic SQL
-- Questions 1-20  (lab exercise #3, Parts B to F)
-- Prerequisite: A3_00_seed.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100
SET FEEDBACK ON
"""]
    for num, question, fn in SQLQ:
        if fn is None:
            continue
        sql, headers, rows, nums = fn()
        out = render(headers, rows, nums) + sel(rows)
        with open(os.path.join(PAGE_DIR, "a3_q%02d.tex" % num), "w") as f:
            f.write(page(num, question, sql.split("\n"), out))
        parts.append("\nPROMPT\nPROMPT ===== Q%d =====\n\n%s\n" % (num, sql))

    # question 20 combines the two aggregate queries
    sql20 = ("SELECT COUNT(*) AS total_students FROM student;\n\n"
             "SELECT MAX(cgpa) AS highest, MIN(cgpa) AS lowest,\n"
             "       AVG(cgpa) AS average\nFROM student;")
    out20 = render(["TOTAL_STUDENTS"], [(len(STUDENTS),)], (0,)) + sel([1]) + [""] + \
        render(["HIGHEST", "LOWEST", "AVERAGE"],
               [(max(s[3] for s in STUDENTS if s[3] is not None),
                 min(s[3] for s in STUDENTS if s[3] is not None),
                 round(sum(s[3] for s in STUDENTS if s[3] is not None) /
                       len([s for s in STUDENTS if s[3] is not None]), 2))], (0, 1, 2)) + sel([1])
    with open(os.path.join(PAGE_DIR, "a3_q20.tex"), "w") as f:
        f.write(page(20, SQLQ[-1][1], sql20.split("\n"), out20))
    parts.append("\nPROMPT\nPROMPT ===== Q20 =====\n\n%s\n" % sql20)

    with open(os.path.join(SQL_DIR, "A3_01_to_20_basic_sql.sql"), "w") as f:
        f.write("".join(parts))

    print("DML pages: 20, SQL pages: 20")


if __name__ == "__main__":
    main()
