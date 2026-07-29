drop table Emp_Proj;
drop table project;
drop table employee;
drop table department;
create table department(
	DeptNo char(5) constraint dept_pkey primary key not null,
	DeptName varchar2(35),
	hod_name varchar2(25),
	location varchar2(50)
);
create table employee(
	EmpNo char(10) constraint employee_pkey primary key check (EmpNo like 'E%'),
	EmpName varchar2(30),
	DeptNo char(5) references department(DeptNo),
	Mobile char(12),
	Hire_date date,
	Job varchar2(15),
	Edlevel smallint,
	gender char(1) constraint employee_gender_check check(gender in ('M','F')),
	dob date,
	salary number(10,2) constraint employee_salary_check check ( salary > 0 ),
	bonus number(10,2),
	comm number(10,2)
);

create table project(
	ProjNo char(10) constraint project_pkey primary key not null,
	ProjName varchar2(30) ,
	DeptNo char(5) references department(DeptNo),
	ResEmp char(10) references employee(EmpNo),
	StDate date,
	EndDate date
);

create table Emp_Proj(
	ProjNo char(10) references project(ProjNo),
	EmpNo char(10) references employee(EmpNo),
	EmpTime char(10)
);
