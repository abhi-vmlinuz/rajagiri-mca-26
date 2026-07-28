drop table emp_proj;
drop table project;
drop table employee;
drop table department;

create table department (
    	dept_no char(5) constraint dept_pk primary key not null,
    	dept_name varchar2(50),
    	location varchar2(15)
 );

create table employee (
	emp_no char(10) constraint emp_pk primary key not null,
	emp_name varchar2(30),
	dept_no char(5) references department(dept_no),
	mobile char(12),
	hire_date date,
	job varchar2(50),
	edlevel smallint,
	gender char(1) constraint emp_gender_check check (gender in ('M','F')),
	dob date,
	salary number(10,2),
	bonus number(10,2),
	comm number(10,2)
);

create table project (
	projno char(10) constraint proj_pk primary key not null,
	projName varchar2(30),
	dept_no char(5) references department(dept_no),
	resEmp char(10) references employee(emp_no),
	stdate date,
	enddate date
);

create table emp_proj (
	projno char(10) references project(projno),
	emp_no char(10) references employee(emp_no),
	empTime char(10)
);
