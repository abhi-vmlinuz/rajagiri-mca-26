-- ============================================================
-- Section A : Basic DDL Commands  (ALTER TABLE)
-- Questions 2-21  (lab exercise Part C, 31-50)
-- Run as          : sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================

SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON

PROMPT
PROMPT ===== Q2 =====

ALTER TABLE student ADD (address VARCHAR2(200));
DESC student;

PROMPT
PROMPT ===== Q3 =====

ALTER TABLE student ADD (city VARCHAR2(30), state VARCHAR2(30));
DESC student;

PROMPT
PROMPT ===== Q4 =====

ALTER TABLE faculty ADD (experience_years NUMBER(2));
DESC faculty;

PROMPT
PROMPT ===== Q5 =====

ALTER TABLE student MODIFY (student_name VARCHAR2(100));
DESC student;

PROMPT
PROMPT ===== Q6 =====

ALTER TABLE student MODIFY (mobile_number VARCHAR2(15));
DESC student;

PROMPT
PROMPT ===== Q7 =====

ALTER TABLE student RENAME COLUMN mobile_number TO contact_number;
DESC student;

PROMPT
PROMPT ===== Q8 =====

ALTER TABLE course RENAME COLUMN course_name TO course_title;
DESC course;

PROMPT
PROMPT ===== Q9 =====

ALTER TABLE student DROP COLUMN address;
DESC student;

PROMPT
PROMPT ===== Q10 =====

ALTER TABLE faculty DROP COLUMN qualification;
DESC faculty;

PROMPT
PROMPT ===== Q11 =====

ALTER TABLE faculty ADD CONSTRAINT chk_faculty_salary CHECK (salary > 0);
UPDATE faculty SET salary = -5000 WHERE faculty_id = 'F101';

PROMPT
PROMPT ===== Q12 =====

ALTER TABLE student
    ADD CONSTRAINT chk_student_cgpa CHECK (cgpa BETWEEN 0 AND 10);
UPDATE student SET cgpa = 12 WHERE student_id = 'S101';

PROMPT
PROMPT ===== Q13 =====

ALTER TABLE event MODIFY (event_name NOT NULL);
DESC event;

PROMPT
PROMPT ===== Q14 =====

ALTER TABLE student
    ADD CONSTRAINT uq_student_contact UNIQUE (contact_number);
DESC student;

PROMPT
PROMPT ===== Q15 =====

ALTER TABLE event RENAME TO college_event;
DESC college_event;

PROMPT
PROMPT ===== Q16 =====

ALTER TABLE college_event RENAME TO event;
DESC event;

PROMPT
PROMPT ===== Q17 =====

ALTER TABLE department ADD (hod_faculty_id CHAR(5));
DESC department;

PROMPT
PROMPT ===== Q18 =====

ALTER TABLE department
    ADD CONSTRAINT fk_dept_hod FOREIGN KEY (hod_faculty_id)
    REFERENCES faculty(faculty_id);
DESC department;

PROMPT
PROMPT ===== Q19 =====

ALTER TABLE department DROP COLUMN hod_name;
DESC department;

PROMPT
PROMPT ===== Q20 =====

ALTER TABLE course DISABLE CONSTRAINT fk_course_faculty;
DESC course;

PROMPT
PROMPT ===== Q21 =====

ALTER TABLE course ENABLE CONSTRAINT fk_course_faculty;
DESC course;
