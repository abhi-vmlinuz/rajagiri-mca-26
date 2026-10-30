-- ============================================================
-- Section A : Basic DML Commands
-- Questions 1-20  (lab exercise Parts A, B and D)
-- Prerequisite: A1_01_department.sql, A1_02_to_08_tables.sql,
--               A1_02_to_21_alter.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100
SET FEEDBACK ON

PROMPT
PROMPT ===== Q1 =====

INSERT INTO department (dept_id, dept_name, office_location, contact_number)
VALUES ('D01', 'Computer Science', 'Carmel Block', '9876543210');

SELECT * FROM department;

PROMPT
PROMPT ===== Q2 =====

INSERT INTO student (student_id, student_name, dob, gender, contact_number,
                     email_id, dept_id, admission_date, cgpa)
VALUES ('S101', 'Akhil Raj', TO_DATE('15-08-2005', 'DD-MM-YYYY'), 'M',
        '9876501234', 'akhil@gmail.com', 'D01', SYSDATE, 8.2);

SELECT * FROM student;

PROMPT
PROMPT ===== Q3 =====

INSERT INTO student (student_id, student_name, dob, gender, contact_number,
                     email_id, dept_id, admission_date)
VALUES ('S102', 'Neha Thomas', TO_DATE('22-03-2006', 'DD-MM-YYYY'), 'F',
        '9876501235', 'neha@gmail.com', 'D01', SYSDATE);

SELECT * FROM student;

PROMPT
PROMPT ===== Q4 =====

INSERT ALL
  INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,
                email_id, dept_id)
  VALUES ('F102', 'Ravi Kumar', 'Assistant Professor', TO_DATE('10-07-2024','DD-MM-YYYY'),
          25000, 'ravi@rajagiri.edu', 'D01')
  INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,
                email_id, dept_id)
  VALUES ('F103', 'Anita Thomas', 'Professor', TO_DATE('01-06-2011','DD-MM-YYYY'),
          90000, 'anita@rajagiri.edu', 'D01')
SELECT * FROM dual;

SELECT * FROM faculty;

PROMPT
PROMPT ===== Q5 =====

INSERT INTO faculty (faculty_id, faculty_name, designation, joining_date, salary,
                     email_id, dept_id)
VALUES ('F101', 'Meera Joseph', 'Assistant Professor', TO_DATE('01-06-2022','DD-MM-YYYY'),
        55000, 'meera@rajagiri.edu', 'D01');

SELECT * FROM faculty;

PROMPT
PROMPT ===== Q6 =====

INSERT INTO course (course_id, course_title, credits, semester, dept_id, faculty_id)
VALUES ('C101', 'Database Management Systems', 4, 3, 'D01', 'F101');

SELECT * FROM course;

PROMPT
PROMPT ===== Q7 =====

INSERT INTO course
VALUES ('C102', 'Operating Systems', 3, 8, 'D01', 'F102');

SELECT * FROM course;

PROMPT
PROMPT ===== Q8 =====

INSERT INTO enrollment (enrollment_id, student_id, course_id, academic_year)
VALUES ('E101', 'S101', 'C101', '2025-2026');

SELECT * FROM enrollment;

PROMPT
PROMPT ===== Q9 =====

INSERT INTO result (result_id, enrollment_id, internal_marks, external_marks,
                    total_marks, grade, result_status)
VALUES ('R101', 'E101', 18, 22, 18 + 22, 'F', 'FAIL');

SELECT * FROM result;

PROMPT
PROMPT ===== Q10 =====

INSERT ALL
  INTO event VALUES ('EV01', 'Tech Fest', TO_DATE('15-03-2026','DD-MM-YYYY'),
                     'Main Auditorium', 'F101', 150, 200)
  INTO event VALUES ('EV02', 'Workshop on AI', TO_DATE('10-04-2024','DD-MM-YYYY'),
                     'Seminar Hall', 'F102', 50, NULL)
  INTO event VALUES ('EV03', 'National Seminar', TO_DATE('20-11-2025','DD-MM-YYYY'),
                     'Seminar Hall', 'F103', 300, 100)
SELECT * FROM dual;

SELECT * FROM event;

PROMPT
PROMPT ===== Q11 =====

INSERT INTO event_registration (registration_id, event_id, student_id,
                               participation_status)
VALUES ('REG01', 'EV01', 'S101', 'ABSENT');

SELECT * FROM event_registration;

PROMPT
PROMPT ===== Q12 =====

UPDATE student SET cgpa = 8.7 WHERE student_id = 'S101';

SELECT student_id, cgpa FROM student WHERE student_id = 'S101';

PROMPT
PROMPT ===== Q13 =====

UPDATE faculty SET salary = salary * 1.10;

SELECT faculty_id, faculty_name, salary FROM faculty;

PROMPT
PROMPT ===== Q14 =====

UPDATE department SET office_location = 'Golden Aureole Block'
WHERE dept_name = 'Computer Science';

SELECT dept_id, dept_name, office_location FROM department
WHERE dept_name = 'Computer Science';

PROMPT
PROMPT ===== Q15 =====

UPDATE course SET credits = 5
WHERE course_title = 'Database Management Systems';

SELECT course_id, course_title, credits FROM course
WHERE course_title = 'Database Management Systems';

PROMPT
PROMPT ===== Q16 =====

UPDATE result
SET result_status = CASE WHEN total_marks >= 50 THEN 'PASS' ELSE 'FAIL' END;

SELECT result_id, total_marks, result_status FROM result;

PROMPT
PROMPT ===== Q17 =====

DELETE FROM course WHERE semester = 8;

PROMPT
PROMPT ===== Q18 =====

DELETE FROM result WHERE result_status = 'FAIL';

PROMPT
PROMPT ===== Q19 =====

DELETE FROM event_registration WHERE participation_status = 'ABSENT';

PROMPT
PROMPT ===== Q20 =====

DELETE FROM event WHERE registration_fee IS NULL OR registration_fee = 0;

COMMIT;
