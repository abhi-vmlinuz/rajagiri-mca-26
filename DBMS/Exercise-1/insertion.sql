-- === PART A ====
-- DEPT INSERTIONS
insert into dept values ('D01','Computer Science','Dr Anil Kumar',987654321,'Carmel Block');
insert into dept(dept_id, dept_name, office_location) values ('D03','Bio Science','Carmel Block');
insert into dept values ('D02','MSW','Dr Reji John',987654321,'Assumption Block');
insert into dept values ('D04','Statistics','Mr Dilijith K Benny',987654321,'Assumption Block');
insert into dept values ('D05','Social Work','Mr Roshy Augustin',987654321,'Assumption Block');

-- FACULTY INSERTIONS
insert into faculty values ('F101','Dr Shiju Thomas','Ph.D','Professor',current_date,67000,'professor.shiju@edu','D01');
insert into faculty values ('F102','Meera Joseph','PhD','Assistant Professor',to_date('01-06-2022','DD-MM-YYYY'),55000,'meera@rajagiri.edu','D01');
insert all 
    into faculty values ('F103','Dr Ajay Das','Ph.D','Associate Professor',current_date,52000,'ajay@gmail.com','D01') 
    into faculty values ('F104','Mr Dilijith K Benny','MSc','Associate Professor',current_date,50000,'dilijth@gmail.com','D04') 
select * from dual;

-- STUDENT INSERTIONS
insert into student values ('S101','Akhil Raj',to_date('15-08-2005','DD-MM-YYYY'),'M',987654321,'akhil@gmail.com','D01',current_date,8.2);
insert into student(student_id,dob,gender,mobile_no,email_id,admission_date,student_name,dept_id) values ('S102',to_date('12-02-2006','DD-MM-YYYY'),'M',987654321,'abhishek@gmail.com',current_date,'Abhishek Vincent','D01');
insert into student values ('S103','Jemima Eden',to_date('17-02-2005','DD-MM-YYYY'),'F',987654321,'jemima@gmail.com','D01',current_date,9.3);

-- COURSE INSERTIONS
insert into course(course_id, course_name, course_credits, semester, dept_id, faculty_id) values ('C101','Database Management Systems',4,3,'D01','F101');
insert into course values ('C102','Object Oriented C++',4,1,'D01','F101');

-- Enrollment insertions
insert into enrollment(enrollment_id,student_id,course_id,academic_year) values ('E101','S101','C101','2026-2027');

-- result insertions
insert into result values ('R101','E101',45,50,'A','PASS',DEFAULT);

-- event insertions
insert all into event values ('E101','Euphoria',current_date,'Carmel Block','F101',100,200)
 into event values ('E102','Gyanimesh',current_date,'Darshana','F102',200,20)
 into event values ('E103','CSTAR event',to_date('27-08-2026','DD-MM-YYYY'),'Amigo','F103',60,0)
 select * from dual;
insert into event_registration values ('R101','E101','S101',current_date,'REGISTERED');

create table high_cgpa_students as select * from student where cgpa >=8;

-- === PART B ====
update student set CGPA = 8.7 where student_id = 'S101';
update student set mobile_no = 9142327534, email_id = 'test@gmail.com' where student_id = 'S101';
update faculty set salary = salary + 5000 where faculty_id = 'F101';
update faculty set salary = salary * 1.10;
update faculty set salary = salary * 1.08 where designation = 'Assistant Professor';
update dept set office_location = 'Golden Aureole Block' where dept_name like 'Compu%';
update course set course_credits = 5 where course_name like 'Data%';
update course set faculty_id = 'F102' where faculty_id  = 'F101';
update result set grade = 'A' where total_marks >= 80;
update result set result_status = 'PASS' where total_marks >= 50;
update event_registration set participation_status = 'ATTENDED' where participation_status = 'REGISTERED';
update event set registration_fee = 0 where registration_fee is null;
update enrollment set academic_year = '2026-2027';

-- === PART C ===
alter table student add address varchar2(200);
alter table student add (city varchar2(15), state varchar2(15));
alter table faculty add experience_years numeric;
alter table student modify student_name varchar2(100);
-- need a temp table to store exisitng ph.nos
alter table student add temp varchar2(15);
-- back up the values
update student set temp = to_char(mobile_no);
-- drop then rename back to mobile_no
alter table student drop column mobile_no;
alter table student rename column temp to mobile_no;
-- continuing with the questions:
alter table student rename column mobile_no to contact_number;
alter table course rename column course_name to course_title;

