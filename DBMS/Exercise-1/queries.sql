drop table faculty;
drop table student;
drop table dept;
create table dept(
	dept_id varchar2(10) constraint dept_pkey primary key,
	dept_name varchar2(20) constraint dept_uni unique not null,
	hod_name varchar2(25),
	contact_no numeric(10),
	office_location varchar2(50)
);
create table student(
	student_id varchar2(20) constraint student_pkey primary key,
	dob date,
	gender char(1) constraint student_gender_check check(gender in ('M','F')),
	mobile_no numeric(13),
	email_id varchar2(30) constraint student_unique unique,
	admission_date date,
	cgpa numeric(4,2) constraint student_cgpa check(cgpa between 0 and 10)
);

create table faculty(
	faculty_id number(5) constraint faculty_pkey primary key,
	faculty_name varchar2(30) not null,
	qualification varchar2(50) not null,
	designation varchar2(40) not null,
	joining_date date default sysdate,
	salary number(10,2) constraint salary_check check(salary > 1000),
	email_id varchar2(20) constraint faculty_email_unique unique
);

