-- ============================================================
-- Section A : Basic DDL Commands
-- Table 1    : DEPARTMENT
-- Run as     : sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================

SET LINESIZE 80
SET PAGESIZE 100
SET FEEDBACK ON

CREATE TABLE department (
    dept_id         VARCHAR2(10)  PRIMARY KEY,
    dept_name       VARCHAR2(20)  NOT NULL UNIQUE,
    hod_name        VARCHAR2(50),
    office_location VARCHAR2(50),
    contact_number  VARCHAR2(15)
);

DESC department;
