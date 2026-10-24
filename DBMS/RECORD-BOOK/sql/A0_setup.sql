-- ============================================================
-- Section A : one-shot setup
-- Drops and recreates the 8 record tables, then applies the
-- 20 ALTER statements, leaving the schema in the exact state
-- that the DML / Basic SQL sections expect.
--
--   DESTRUCTIVE: all rows currently in these 8 tables are lost.
--   Your other tables (DEPT, EMPLOYEE, PROJECT, EMP_PROJ, TEMP,
--   HIGH_CGPA_STUDENTS) are NOT touched.
--
-- Run from this directory:
--   sqlplus 'mca/mca'@localhost:1521/FREEPDB1 @A0_setup.sql
-- ============================================================

SET ECHO OFF
SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON
SET SERVEROUTPUT ON

PROMPT ============================================================
PROMPT 1/3  dropping the 8 record tables (if present)
PROMPT ============================================================

DECLARE
    TYPE tlist IS TABLE OF VARCHAR2(30);
    tabs tlist := tlist('EVENT_REGISTRATION', 'RESULT', 'ENROLLMENT', 'EVENT',
                        'COURSE', 'STUDENT', 'FACULTY', 'DEPARTMENT');
BEGIN
    FOR i IN 1 .. tabs.COUNT LOOP
        BEGIN
            EXECUTE IMMEDIATE 'DROP TABLE ' || tabs(i) || ' CASCADE CONSTRAINTS';
            DBMS_OUTPUT.PUT_LINE('dropped ' || tabs(i));
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE = -942 THEN
                    DBMS_OUTPUT.PUT_LINE('skipped ' || tabs(i) || ' (not present)');
                ELSE
                    RAISE;
                END IF;
        END;
    END LOOP;
END;
/

PROMPT ============================================================
PROMPT 2/3  creating the 8 tables  (Section A, question 1)
PROMPT ============================================================

@A1_01_department.sql
@A1_02_to_08_tables.sql

PROMPT ============================================================
PROMPT 3/3  applying the 20 ALTER statements  (questions 2-21)
PROMPT ============================================================

@A1_02_to_21_alter.sql

PROMPT
PROMPT ============================================================
PROMPT setup complete - schema now matches the record
PROMPT ============================================================
