#!/usr/bin/env python3
"""Generate Section A DDL pages + SQL for the Rajagiri academic schema.

Single source of truth for: the 4-column column table, the CREATE TABLE code,
and the DESC output (formatted the way SQL*Plus prints it at LINESIZE 80).
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(ROOT, "sql")
PAGE_DIR = os.path.join(ROOT, "record", "pages")


def desc_block(table):
    """Render SQL*Plus DESC output (name field 42, null field 9)."""
    out = [" Name".ljust(43) + "Null?".ljust(9) + "Type",
           " " + "-" * 41 + " " + "-" * 8 + " " + "-" * 28]
    for c in table["cols"]:
        null = "" if c["null"] else "NOT NULL"
        out.append(" " + c["name"].upper().ljust(42) + null.ljust(9) + c["type"])
    return "\n".join(out)


def create_sql(table):
    wname = max(len(c["name"]) for c in table["cols"])
    wtype = max(len(c["type"]) for c in table["cols"])
    lines = []
    for c in table["cols"]:
        head = "    " + c["name"].lower().ljust(wname) + " " + c["type"].ljust(wtype)
        if c["ddl"]:
            line = head + "  " + c["ddl"]
            if len(line) > 74:
                lines.append(head.rstrip() + "\n        " + c["ddl"])
            else:
                lines.append(line.rstrip())
        else:
            lines.append(head.rstrip())
    if table.get("extra"):
        lines.append("    " + table["extra"])
    return "CREATE TABLE %s (\n%s\n);" % (table["name"].lower(), ",\n".join(lines))


def cell(text):
    text = re.sub(r"(?<=[A-Za-z])\(", " (", text)   # let long FK refs break at the paren
    return text.replace("_", r"\_")


def page_tex(table):
    rows = []
    for c in table["cols"]:
        rows.append("%s & %s & %s & %s \\\\" % (
            cell(c["name"].lower()), c["desc"], c["type"], cell(c["constraint"])))
    if table.get("extra_row"):
        rows.append("%s \\\\" % table["extra_row"])
    body = "\n\\hline\n".join(rows)

    return r"""%% ---------------------------------------------------------------------
%% %(label)s
%% ---------------------------------------------------------------------

\textbf{Table Name:} %(name)s \hspace{1em plus 1fill}
\textbf{Description:} %(tabledesc)s

\vspace{8pt}

\renewcommand{\arraystretch}{1.4}
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Column Name} & \textbf{Description} & \textbf{Data Type} & \textbf{Constraint} \\
\hline
%(body)s
\hline
\end{tabularx}

\vspace{14pt}

\codeheading{CODE:}

\begin{sqlcode}
%(code)s
\end{sqlcode}

\vspace{16pt}

\codeheading{OUTPUT:}

\begin{sqlout}
Table created.

%(desc)s
\end{sqlout}

\clearpage
""" % dict(label=table["label"], num=table["num"], name=cell(table["name"]),
           tabledesc=table["desc"], body=body, code=create_sql(table),
           desc=desc_block(table))


TABLES = [
    dict(num=2, name="STUDENT", label="Section A / Table 2 : STUDENT",
         desc="Stores the personal and academic details of every student.",
         cols=[
             dict(name="student_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Student ID", constraint="PRIMARY KEY"),
             dict(name="student_name", type="VARCHAR2(50)", null=False, ddl="NOT NULL",
                  desc="Student Name", constraint="NOT NULL"),
             dict(name="dob", type="DATE", null=True, ddl="",
                  desc="Date of Birth", constraint="--"),
             dict(name="gender", type="CHAR(1)", null=True,
                  ddl="CHECK (gender IN ('M', 'F'))",
                  desc="Gender", constraint="CHECK (M or F)"),
             dict(name="mobile_number", type="VARCHAR2(10)", null=True, ddl="",
                  desc="Mobile Number", constraint="--"),
             dict(name="email_id", type="VARCHAR2(50)", null=True, ddl="UNIQUE",
                  desc="Email ID", constraint="UNIQUE"),
             dict(name="dept_id", type="VARCHAR2(10)", null=True,
                  ddl="REFERENCES department(dept_id)",
                  desc="Department ID", constraint="FOREIGN KEY REFERENCES department(dept_id)"),
             dict(name="admission_date", type="DATE", null=True, ddl="",
                  desc="Admission Date", constraint="--"),
             dict(name="cgpa", type="NUMBER(4,2)", null=True,
                  ddl="CHECK (cgpa BETWEEN 0 AND 10)",
                  desc="CGPA", constraint="CHECK (0 to 10)"),
         ]),
    dict(num=3, name="FACULTY", label="Section A / Table 3 : FACULTY",
         desc="Stores the details of the teaching faculty.",
         cols=[
             dict(name="faculty_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Faculty ID", constraint="PRIMARY KEY"),
             dict(name="faculty_name", type="VARCHAR2(50)", null=False, ddl="NOT NULL",
                  desc="Faculty Name", constraint="NOT NULL"),
             dict(name="qualification", type="VARCHAR2(30)", null=True, ddl="",
                  desc="Qualification", constraint="--"),
             dict(name="designation", type="VARCHAR2(30)", null=True, ddl="",
                  desc="Designation", constraint="--"),
             dict(name="joining_date", type="DATE", null=True, ddl="",
                  desc="Date of Joining", constraint="--"),
             dict(name="salary", type="NUMBER(10,2)", null=True,
                  ddl="CHECK (salary > 0)",
                  desc="Salary", constraint="CHECK (salary > 0)"),
             dict(name="email_id", type="VARCHAR2(50)", null=True, ddl="UNIQUE",
                  desc="Email ID", constraint="UNIQUE"),
             dict(name="dept_id", type="VARCHAR2(10)", null=True,
                  ddl="REFERENCES department(dept_id)",
                  desc="Department ID", constraint="FOREIGN KEY REFERENCES department(dept_id)"),
         ]),
    dict(num=4, name="COURSE", label="Section A / Table 4 : COURSE",
         desc="Stores the courses offered by each department.",
         cols=[
             dict(name="course_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Course Code", constraint="PRIMARY KEY"),
             dict(name="course_name", type="VARCHAR2(50)", null=False, ddl="NOT NULL",
                  desc="Course Name", constraint="NOT NULL"),
             dict(name="credits", type="NUMBER(1)", null=True,
                  ddl="CHECK (credits BETWEEN 1 AND 6)",
                  desc="Number of Credits", constraint="CHECK (1 to 6)"),
             dict(name="semester", type="NUMBER(1)", null=True,
                  ddl="CHECK (semester BETWEEN 1 AND 8)",
                  desc="Semester", constraint="CHECK (1 to 8)"),
             dict(name="dept_id", type="VARCHAR2(10)", null=True,
                  ddl="REFERENCES department(dept_id)",
                  desc="Department ID", constraint="FOREIGN KEY REFERENCES department(dept_id)"),
             dict(name="faculty_id", type="CHAR(5)", null=True,
                  ddl="CONSTRAINT fk_course_faculty REFERENCES faculty(faculty_id)",
                  desc="Faculty ID", constraint="FOREIGN KEY REFERENCES faculty(faculty_id)"),
         ]),
    dict(num=5, name="ENROLLMENT", label="Section A / Table 5 : ENROLLMENT",
         desc="Records the courses enrolled by each student.",
         cols=[
             dict(name="enrollment_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Enrollment ID", constraint="PRIMARY KEY"),
             dict(name="student_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES student(student_id)",
                  desc="Student ID", constraint="FOREIGN KEY REFERENCES student(student_id)"),
             dict(name="course_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES course(course_id)",
                  desc="Course Code", constraint="FOREIGN KEY REFERENCES course(course_id)"),
             dict(name="enrollment_date", type="DATE", null=True, ddl="DEFAULT SYSDATE",
                  desc="Enrollment Date", constraint="DEFAULT SYSDATE"),
             dict(name="academic_year", type="VARCHAR2(9)", null=True, ddl="",
                  desc="Academic Year", constraint="--"),
         ],
         extra="UNIQUE (student_id, course_id)"),
    dict(num=6, name="RESULT", label="Section A / Table 6 : RESULT",
         desc="Stores the internal, external and total marks of each enrollment.",
         cols=[
             dict(name="result_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Result ID", constraint="PRIMARY KEY"),
             dict(name="enrollment_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES enrollment(enrollment_id)",
                  desc="Enrollment ID", constraint="FOREIGN KEY REFERENCES enrollment(enrollment_id)"),
             dict(name="internal_marks", type="NUMBER(5,2)", null=True,
                  ddl="CHECK (internal_marks BETWEEN 0 AND 50)",
                  desc="Internal Marks", constraint="CHECK (0 to 50)"),
             dict(name="external_marks", type="NUMBER(5,2)", null=True,
                  ddl="CHECK (external_marks BETWEEN 0 AND 50)",
                  desc="External Marks", constraint="CHECK (0 to 50)"),
             dict(name="total_marks", type="NUMBER(6,2)", null=True, ddl="",
                  desc="Total Marks", constraint="--"),
             dict(name="grade", type="CHAR(1)", null=True,
                  ddl="CHECK (grade IN ('A', 'B', 'C', 'D', 'F'))",
                  desc="Grade", constraint="CHECK (A, B, C, D, F)"),
             dict(name="result_status", type="VARCHAR2(10)", null=True,
                  ddl="CHECK (result_status IN ('PASS', 'FAIL'))",
                  desc="PASS / FAIL", constraint="CHECK (PASS or FAIL)"),
         ]),
    dict(num=7, name="EVENT", label="Section A / Table 7 : EVENT",
         desc="Stores the details of events conducted by the college.",
         cols=[
             dict(name="event_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Event ID", constraint="PRIMARY KEY"),
             dict(name="event_name", type="VARCHAR2(50)", null=True, ddl="",
                  desc="Event Name", constraint="--"),
             dict(name="event_date", type="DATE", null=True, ddl="",
                  desc="Event Date", constraint="--"),
             dict(name="venue", type="VARCHAR2(50)", null=True, ddl="",
                  desc="Venue", constraint="--"),
             dict(name="faculty_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES faculty(faculty_id)",
                  desc="Coordinator Faculty ID", constraint="FOREIGN KEY REFERENCES faculty(faculty_id)"),
             dict(name="max_participants", type="NUMBER(5)", null=True,
                  ddl="CHECK (max_participants > 0)",
                  desc="Maximum Participants", constraint="CHECK (max_participants > 0)"),
             dict(name="registration_fee", type="NUMBER(8,2)", null=True,
                  ddl="CHECK (registration_fee >= 0)",
                  desc="Registration Fee", constraint="CHECK (registration_fee >= 0)"),
         ]),
    dict(num=8, name="EVENT_REGISTRATION", label="Section A / Table 8 : EVENT_REGISTRATION",
         desc="Records student registrations for each event.",
         cols=[
             dict(name="registration_id", type="CHAR(5)", null=False, ddl="PRIMARY KEY",
                  desc="Registration ID", constraint="PRIMARY KEY"),
             dict(name="event_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES event(event_id)",
                  desc="Event ID", constraint="FOREIGN KEY REFERENCES event(event_id)"),
             dict(name="student_id", type="CHAR(5)", null=True,
                  ddl="REFERENCES student(student_id)",
                  desc="Student ID", constraint="FOREIGN KEY REFERENCES student(student_id)"),
             dict(name="registration_date", type="DATE", null=True, ddl="DEFAULT SYSDATE",
                  desc="Registration Date", constraint="DEFAULT SYSDATE"),
             dict(name="participation_status", type="VARCHAR2(15)", null=True,
                  ddl="CHECK (participation_status IN ('REGISTERED', 'ATTENDED', 'ABSENT'))",
                  desc="Participation Status", constraint="CHECK (REGISTERED, ATTENDED, ABSENT)"),
         ]),
]


def main():
    os.makedirs(SQL_DIR, exist_ok=True)
    os.makedirs(PAGE_DIR, exist_ok=True)
    for t in TABLES:
        slug = "%02d_%s" % (t["num"], t["name"].lower())
        with open(os.path.join(PAGE_DIR, "a1_%s.tex" % slug), "w") as f:
            f.write(page_tex(t))

    parts = ["""-- ============================================================
-- Section A : Basic DDL Commands
-- Tables 2-8 : STUDENT, FACULTY, COURSE, ENROLLMENT,
--              RESULT, EVENT, EVENT_REGISTRATION
-- Prerequisite: DEPARTMENT (run A1_01_department.sql first)
-- Run as      : sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================

SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON
"""]
    for t in TABLES:
        parts.append("\nPROMPT\nPROMPT ===== TABLE %d : %s =====\n\n%s\n\nDESC %s;\n"
                     % (t["num"], t["name"], create_sql(t), t["name"].lower()))
    with open(os.path.join(SQL_DIR, "A1_02_to_08_tables.sql"), "w") as f:
        f.write("".join(parts))

    print("generated %d pages and the DDL script" % len(TABLES))


if __name__ == "__main__":
    main()
