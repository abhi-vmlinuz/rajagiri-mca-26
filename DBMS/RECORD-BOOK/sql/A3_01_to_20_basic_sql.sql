-- ============================================================
-- Section A : Basic SQL
-- Questions 1-20  (lab exercise #3, Parts B to F)
-- Prerequisite: A3_00_seed.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100
SET FEEDBACK ON

PROMPT
PROMPT ===== Q1 =====

SELECT DISTINCT designation FROM faculty;

PROMPT
PROMPT ===== Q2 =====

SELECT DISTINCT semester FROM course;

PROMPT
PROMPT ===== Q3 =====

SELECT student_name AS Student_Name, cgpa AS Grade_Point_Average
FROM student;

PROMPT
PROMPT ===== Q4 =====

SELECT faculty_name, salary, salary * 12 AS annual_salary
FROM faculty;

PROMPT
PROMPT ===== Q5 =====

SELECT faculty_name, salary, salary * 1.10 AS increased_salary
FROM faculty;

PROMPT
PROMPT ===== Q6 =====

SELECT result_id, internal_marks, external_marks,
       internal_marks + external_marks AS total
FROM result;

PROMPT
PROMPT ===== Q7 =====

SELECT event_name, registration_fee,
       registration_fee * 1.18 AS fee_with_tax
FROM event;

PROMPT
PROMPT ===== Q8 =====

SELECT * FROM faculty WHERE salary > 50000;

PROMPT
PROMPT ===== Q9 =====

SELECT * FROM course WHERE semester = 3;

PROMPT
PROMPT ===== Q10 =====

SELECT * FROM result WHERE total_marks >= 80;

PROMPT
PROMPT ===== Q11 =====

SELECT * FROM event WHERE registration_fee > 500;

PROMPT
PROMPT ===== Q12 =====

SELECT student_id, student_name, cgpa, dept_id
FROM student WHERE cgpa BETWEEN 7 AND 9;

PROMPT
PROMPT ===== Q13 =====

SELECT course_id, course_title, semester
FROM course WHERE semester IN (1, 3, 5);

PROMPT
PROMPT ===== Q14 =====

SELECT student_id, student_name, cgpa
FROM student WHERE student_name LIKE 'A%';

PROMPT
PROMPT ===== Q15 =====

SELECT faculty_id, faculty_name, email_id
FROM faculty WHERE email_id LIKE '%@rajagiri.edu';

PROMPT
PROMPT ===== Q16 =====

SELECT student_id, student_name
FROM student WHERE cgpa IS NULL;

PROMPT
PROMPT ===== Q17 =====

SELECT UPPER(student_name) AS student_name FROM student;

PROMPT
PROMPT ===== Q18 =====

SELECT INITCAP(faculty_name) AS faculty_name FROM faculty;

PROMPT
PROMPT ===== Q19 =====

SELECT student_name, LENGTH(student_name) AS name_length
FROM student;

PROMPT
PROMPT ===== Q20 =====

SELECT COUNT(*) AS total_students FROM student;

SELECT MAX(cgpa) AS highest, MIN(cgpa) AS lowest,
       AVG(cgpa) AS average
FROM student;
