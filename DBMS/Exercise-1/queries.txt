-- === PART A ===
select * from employee;
select empno,empname,dob,salary from employee where salary > 30000;
select empname,deptno from employee order by deptno desc, empname desc;
select distinct edlevel from employee order by edlevel desc;
select e.empno, p.projno 
from employee e
join project p on e.empno = p.respemp
where e.empno <= 'E0100'
order by e.empno;

-- list employee name, salary, and bonus of all male employees. [source: 1]
select empname, salary, bonus 
from employee 
where gender = 'M';

-- list employee name, salary, and commission for all employees with a salary greater than 20,000 and hired after 2004. [source: 1]
select empname, salary, comm 
from employee 
where salary > 20000 
  and hire_date > to_date('2004-12-31', 'YYYY-MM-DD');

-- list employee name, salary, bonus, and commission for all employees with a salary greater than 22,000 and a bonus of 400, or for all employees with a bonus of 500 and a commission lower than 1,900. the list should be ordered by employee name. [source: 1]
select empname, salary, bonus, comm 
from employee 
where (salary > 22000 and bonus = 400) 
   or (bonus = 500 and comm < 1900)
order by empname;

-- list employee name, salary, bonus, and commission for all employees with a salary greater than 22,000, a bonus of 400 or 500, and a commission less than 1,900. the list should be ordered by employee name. [source: 1]
select empname, salary, bonus, comm 
from employee 
where salary > 22000 
  and bonus in (400, 500) 
  and comm < 1900
order by empname;

-- list employee number, name, salary, and bonus for all employees that have a bonus ranging from 800 to 1,000. sort the report by employee number within bonus, lowest bonus first. [source: 1]
select empno, empname, salary, bonus 
from employee 
where bonus between 800 and 1000
order by bonus asc, empno asc;

-- list employee number, name, salary, and department number for all employees in departments a00 through c01 (inclusive). order the results alphabetically by employee name and employee number. [source: 1]
select empno, empname, salary, deptno 
from employee 
where deptno between 'A00' and 'C01'
order by empname asc, empno asc;

-- list all projects that have support as part of the project name. order the results by project number. [source: 1]
select projno, projname 
from project 
where projname like '%SUPPORT%'
order by projno;

-- list all departments that have a 1 as the middle character in the department number. order the results by department number. [source: 1]
select deptno, deptname 
from dept 
where deptno like '_1_'
order by deptno;

-- list the names and salary of the five highest paid employees. [source: 1]
select empname, salary 
from (
    select empname, salary 
    from employee 
    order by salary desc
) 
where rownum <= 5;

