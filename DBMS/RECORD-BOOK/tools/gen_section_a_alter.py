#!/usr/bin/env python3
"""Generate the ALTER TABLE exercises (questions 2-21) for Section A."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(ROOT, "sql")
PAGE_DIR = os.path.join(ROOT, "record", "pages")
CAPTURE = os.path.join(ROOT, "tools", ".section_a_capture.json")

DEPT_DESC = """ Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 DEPT_ID                                   NOT NULL VARCHAR2(10)
 DEPT_NAME                                 NOT NULL VARCHAR2(20)
 OFFICE_LOCATION                                    VARCHAR2(50)
 CONTACT_NUMBER                                     VARCHAR2(15)
 HOD_FACULTY_ID                                     CHAR(5)"""

Q = [
    (2, "Add a column named address with datatype VARCHAR2(200) to the STUDENT table.",
     ["ALTER TABLE student ADD (address VARCHAR2(200));"], ["Table altered."]),
    (3, "Add two columns, city and state, to the STUDENT table.",
     ["ALTER TABLE student ADD (city VARCHAR2(30), state VARCHAR2(30));"], ["Table altered."]),
    (4, "Add a column named experience_years to the FACULTY table.",
     ["ALTER TABLE faculty ADD (experience_years NUMBER(2));"], ["Table altered."]),
    (5, "Modify the size of the student_name column to VARCHAR2(100).",
     ["ALTER TABLE student MODIFY (student_name VARCHAR2(100));"], ["Table altered."]),
    (6, "Modify the datatype of mobile_number so that it can store 15 characters.",
     ["ALTER TABLE student MODIFY (mobile_number VARCHAR2(15));"], ["Table altered."]),
    (7, "Rename the column mobile_number in the STUDENT table to contact_number.",
     ["ALTER TABLE student RENAME COLUMN mobile_number TO contact_number;"], ["Table altered."]),
    (8, "Rename the column course_name in the COURSE table to course_title.",
     ["ALTER TABLE course RENAME COLUMN course_name TO course_title;"], ["Table altered."]),
    (9, "Delete the newly added address column from the STUDENT table.",
     ["ALTER TABLE student DROP COLUMN address;"], ["Table altered."]),
    (10, "Drop the qualification column from the FACULTY table.",
     ["ALTER TABLE faculty DROP COLUMN qualification;"], ["Table altered."]),
    (11, "Add a CHECK constraint to ensure that faculty salary is greater than zero.",
     ["ALTER TABLE faculty ADD CONSTRAINT chk_faculty_salary CHECK (salary > 0);"],
     ["Table altered."]),
    (12, "Add a CHECK constraint to ensure that student CGPA remains between 0 and 10.",
     ["ALTER TABLE student",
      "    ADD CONSTRAINT chk_student_cgpa CHECK (cgpa BETWEEN 0 AND 10);"],
     ["Table altered."]),
    (13, "Add a NOT NULL constraint to the event_name column.",
     ["ALTER TABLE event MODIFY (event_name NOT NULL);"], ["Table altered."]),
    (14, "Add a unique constraint to the contact_number column of the STUDENT table.",
     ["ALTER TABLE student",
      "    ADD CONSTRAINT uq_student_contact UNIQUE (contact_number);"],
     ["Table altered."]),
    (15, "Rename the EVENT table to COLLEGE_EVENT.",
     ["ALTER TABLE event RENAME TO college_event;"], ["Table renamed."]),
    (16, "Rename the COLLEGE_EVENT table back to EVENT.",
     ["ALTER TABLE college_event RENAME TO event;"], ["Table renamed."]),
    (17, "Add a column named hod_faculty_id to the DEPARTMENT table.",
     ["ALTER TABLE department ADD (hod_faculty_id CHAR(5));"], ["Table altered."]),
    (18, "Create a foreign-key constraint linking hod_faculty_id in DEPARTMENT with "
         "faculty_id in FACULTY.",
     ["ALTER TABLE department",
      "    ADD CONSTRAINT fk_dept_hod FOREIGN KEY (hod_faculty_id)",
      "    REFERENCES faculty(faculty_id);"],
     ["Table altered."]),
    (19, "Remove the existing hod_name column from the DEPARTMENT table, as required in "
         "the database redesign, and display the structure of the modified table.",
     ["ALTER TABLE department DROP COLUMN hod_name;", "DESC department;"],
     ["Table altered.", "", DEPT_DESC]),
    (20, "Disable the foreign-key constraint connecting COURSE and FACULTY.",
     ["ALTER TABLE course DISABLE CONSTRAINT fk_course_faculty;"], ["Table altered."]),
    (21, "Enable the previously disabled foreign-key constraint.",
     ["ALTER TABLE course ENABLE CONSTRAINT fk_course_faculty;"], ["Table altered."]),
]

SPECIAL = {"_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$"}


def prose(text):
    return "".join(SPECIAL.get(ch, ch) for ch in text)


def page(num, question, code, out):
    code_txt = "\n".join(code)
    out_txt = "\n".join(out)
    return r"""%% ---------------------------------------------------------------------
%% Section A / question %(num)d
%% ---------------------------------------------------------------------

\noindent\begin{minipage}{\linewidth}
\begingroup\hyphenpenalty=10000\exhyphenpenalty=10000
{\fontsize{14}{17}\selectfont\textbf{%(num)d.}}\ %(question)s\par
\endgroup\vspace{12pt}

\codeheading{CODE:}

\begin{sqlcode}
%(code)s
\end{sqlcode}

\vspace{18pt}

\codeheading{OUTPUT:}

\begin{sqlout}
%(out)s
\end{sqlout}
\end{minipage}\par\vspace{30pt}

""" % dict(num=num, question=prose(question), code=code_txt, out=out_txt)


def main():
    cap = json.load(open(CAPTURE))["alter"]
    for num, question, code, _out in Q:
        entry = cap["%02d" % num]
        code = list(code)
        if "violation_sql" in entry:
            code.append(entry["violation_sql"])
            out = ["Table altered.", ""] + [l for l in entry["violation"]
                                          if not l.startswith("Help:")]
        else:
            if not any(s.strip().upper().startswith("DESC") for s in code):
                code.append(entry["desc_sql"])
            out = entry["desc"]
        with open(os.path.join(PAGE_DIR, "a1_q%02d.tex" % num), "w") as f:
            f.write(page(num, question, code, out))

    parts = ["""-- ============================================================
-- Section A : Basic DDL Commands  (ALTER TABLE)
-- Questions 2-21  (lab exercise Part C, 31-50)
-- Run as          : sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================

SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON
"""]
    for num, question, code, _out in Q:
        entry = cap["%02d" % num]
        code = list(code)
        if "violation_sql" in entry:
            code.append(entry["violation_sql"])
        elif not any(s.strip().upper().startswith("DESC") for s in code):
            code.append(entry["desc_sql"])
        parts.append("\nPROMPT\nPROMPT ===== Q%d =====\n\n%s\n" % (num, "\n".join(code)))
    with open(os.path.join(SQL_DIR, "A1_02_to_21_alter.sql"), "w") as f:
        f.write("".join(parts))

    print("generated %d pages and the ALTER script" % len(Q))


if __name__ == "__main__":
    main()
