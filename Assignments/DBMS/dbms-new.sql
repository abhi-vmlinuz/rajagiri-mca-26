-- 1. department table
create table department (
    deptno char(5) primary key,
    deptname varchar2(35),
    location varchar2(15)
);

-- 2. employee table
create table employee (
    empno char(10) primary key check (empno like 'e%'),
    empname varchar2(30),
    deptno char(5) references department(deptno),
    mobile char(12),
    hiredate date,
    job varchar2(15),
    edlevel smallint,
    gender char(1) check (gender in ('m', 'f')),
    dob date,
    salary number(10,2) check (salary > 0),
    bonus number(10,2),
    comm number(10,2)
);

-- 3. project table
create table project (
    projno char(10) primary key,
    projname varchar2(30),
    deptno char(5) references department(deptno),
    resemp char(10) references employee(empno),
    stdate date,
    enddate date
);

-- 4. emp_proj table
create table emp_proj (
    projno char(10) references project(projno),
    empno char(10) references employee(empno),
    emptime char(10),
    constraint pk_emp_proj primary key (projno, empno)
);
