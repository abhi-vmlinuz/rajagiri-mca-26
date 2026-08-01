-- DEPT INSERTIONS
insert into dept values ('D01','Computer Science','Dr Anil Kumar',987654321,'Carmel Block');
insert into dept(dept_id, dept_name, office_location) values ('D03','Bio Science','Carmel Block');
insert into dept values ('D02','MSW','Dr Reji John',987654321,'Assumption Block');
insert into dept values ('D04','Statistics','Mr Dilijith K Benny',987654321,'Assumption Block');
insert into dept values ('D05','Social Work','Mr Roshy Augustin',987654321,'Assumption Block');

-- FACULTY INSERTIONS (Must be inserted before Student/Course for Foreign Keys)
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
