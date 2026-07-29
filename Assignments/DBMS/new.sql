-- 1. Department Table
CREATE TABLE Department (
    DeptNo CHAR(5) PRIMARY KEY,
    DeptName VARCHAR2(35),
    Location VARCHAR2(15)
);

-- 2. Employee Table
CREATE TABLE Employee (
    EmpNo CHAR(10) PRIMARY KEY CHECK (EmpNo LIKE 'E%'),
    EmpName VARCHAR2(30),
    DeptNo CHAR(5) REFERENCES Department(DeptNo),
    Mobile CHAR(12),
    HireDate DATE,
    Job VARCHAR2(15),
    EdLevel SMALLINT,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F')),
    DOB DATE,
    Salary NUMBER(10,2) CHECK (Salary > 0),
    Bonus NUMBER(10,2),
    Comm NUMBER(10,2)
);

-- 3. Project Table
CREATE TABLE Project (
    ProjNo CHAR(10) PRIMARY KEY,
    ProjName VARCHAR2(30),
    DeptNo CHAR(5) REFERENCES Department(DeptNo),
    ResEmp CHAR(10) REFERENCES Employee(EmpNo),
    StDate DATE,
    EndDate DATE
);

-- 4. Emp_Proj Table
CREATE TABLE Emp_Proj (
    ProjNo CHAR(10) REFERENCES Project(ProjNo),
    EmpNo CHAR(10) REFERENCES Employee(EmpNo),
    EmpTime CHAR(10),
    CONSTRAINT pk_emp_proj PRIMARY KEY (ProjNo, EmpNo)
);
