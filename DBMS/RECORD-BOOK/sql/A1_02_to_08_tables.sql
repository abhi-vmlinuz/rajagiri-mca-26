-- ============================================================
-- Section A : Basic DDL Commands
-- Tables 2-8 : STUDENT, FACULTY, COURSE, ENROLLMENT,
--              RESULT, EVENT, EVENT_REGISTRATION
-- Prerequisite: DEPARTMENT (run A1_01_department.sql first)
-- Run as      : sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================

SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON

PROMPT
PROMPT ===== TABLE 2 : STUDENT =====

CREATE TABLE student (
    student_id     CHAR(5)       PRIMARY KEY,
    student_name   VARCHAR2(50)  NOT NULL,
    dob            DATE,
    gender         CHAR(1)       CHECK (gender IN ('M', 'F')),
    mobile_number  VARCHAR2(10),
    email_id       VARCHAR2(50)  UNIQUE,
    dept_id        VARCHAR2(10)  REFERENCES department(dept_id),
    admission_date DATE,
    cgpa           NUMBER(4,2)   CHECK (cgpa BETWEEN 0 AND 10)
);

DESC student;

PROMPT
PROMPT ===== TABLE 3 : FACULTY =====

CREATE TABLE faculty (
    faculty_id    CHAR(5)       PRIMARY KEY,
    faculty_name  VARCHAR2(50)  NOT NULL,
    qualification VARCHAR2(30),
    designation   VARCHAR2(30),
    joining_date  DATE,
    salary        NUMBER(10,2)  CHECK (salary > 0),
    email_id      VARCHAR2(50)  UNIQUE,
    dept_id       VARCHAR2(10)  REFERENCES department(dept_id)
);

DESC faculty;

PROMPT
PROMPT ===== TABLE 4 : COURSE =====

CREATE TABLE course (
    course_id   CHAR(5)       PRIMARY KEY,
    course_name VARCHAR2(50)  NOT NULL,
    credits     NUMBER(1)     CHECK (credits BETWEEN 1 AND 6),
    semester    NUMBER(1)     CHECK (semester BETWEEN 1 AND 8),
    dept_id     VARCHAR2(10)  REFERENCES department(dept_id),
    faculty_id  CHAR(5)
        CONSTRAINT fk_course_faculty REFERENCES faculty(faculty_id)
);

DESC course;

PROMPT
PROMPT ===== TABLE 5 : ENROLLMENT =====

CREATE TABLE enrollment (
    enrollment_id   CHAR(5)      PRIMARY KEY,
    student_id      CHAR(5)      REFERENCES student(student_id),
    course_id       CHAR(5)      REFERENCES course(course_id),
    enrollment_date DATE         DEFAULT SYSDATE,
    academic_year   VARCHAR2(9),
    UNIQUE (student_id, course_id)
);

DESC enrollment;

PROMPT
PROMPT ===== TABLE 6 : RESULT =====

CREATE TABLE result (
    result_id      CHAR(5)       PRIMARY KEY,
    enrollment_id  CHAR(5)       REFERENCES enrollment(enrollment_id),
    internal_marks NUMBER(5,2)   CHECK (internal_marks BETWEEN 0 AND 50),
    external_marks NUMBER(5,2)   CHECK (external_marks BETWEEN 0 AND 50),
    total_marks    NUMBER(6,2),
    grade          CHAR(1)
        CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    result_status  VARCHAR2(10)  CHECK (result_status IN ('PASS', 'FAIL'))
);

DESC result;

PROMPT
PROMPT ===== TABLE 7 : EVENT =====

CREATE TABLE event (
    event_id         CHAR(5)       PRIMARY KEY,
    event_name       VARCHAR2(50),
    event_date       DATE,
    venue            VARCHAR2(50),
    faculty_id       CHAR(5)       REFERENCES faculty(faculty_id),
    max_participants NUMBER(5)     CHECK (max_participants > 0),
    registration_fee NUMBER(8,2)   CHECK (registration_fee >= 0)
);

DESC event;

PROMPT
PROMPT ===== TABLE 8 : EVENT_REGISTRATION =====

CREATE TABLE event_registration (
    registration_id      CHAR(5)       PRIMARY KEY,
    event_id             CHAR(5)       REFERENCES event(event_id),
    student_id           CHAR(5)       REFERENCES student(student_id),
    registration_date    DATE          DEFAULT SYSDATE,
    participation_status VARCHAR2(15)
        CHECK (participation_status IN ('REGISTERED', 'ATTENDED', 'ABSENT'))
);

DESC event_registration;
