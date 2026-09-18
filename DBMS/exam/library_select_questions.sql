-- ============================================================
-- LIBRARY_SELECT_QUESTIONS.SQL
-- Practice Questions: SELECT statements only
--   * SELECT, WHERE, ORDER BY, DISTINCT, aggregate functions,
--     GROUP BY, HAVING, date functions, string functions,
--     numeric functions and CASE may be used where appropriate.
-- ============================================================

-- 1. Display the member ID, full name, member type and city of all ACTIVE
--    members, arranged first by member type and then alphabetically by name.
select member_id,full_name,member_type,city from member where status = 'ACTIVE' order by member_type,full_name;


-- 2. List the members whose outstanding amount is between 50 and 300,
--    inclusive. Show member ID, name, outstanding amount and status in
--    descending order of outstanding amount.
select member_id,full_name,outstanding_amt,status from member where outstanding_amt between 50 and 300 order by outstanding_amt desc;

-- 3. Display all members who are either STUDENT or RESEARCHER and whose
--    maximum borrowing limit is at least 4 books. Sort by max_books descending.
select member_id,member_type from member where member_type in('RESEARCHER','STUDENT') and max_books >= 4 order by max_books desc;

-- 4. Display member name, join date and the number of complete years they have
--    been members as of SYSDATE. Show the longest-standing members first.
--    Hint: MONTHS_BETWEEN can be useful.
select full_name, trunc(months_between(sysdate,join_date)/12) as completed_years , join_date from member order by completed_years desc;

-- 5. Display the names and email addresses of members whose name contains the
--    letter 'a' anywhere, ignoring case, and whose account is ACTIVE.
select lower(full_name),email,status from member where full_name like '%a%' and status = 'ACTIVE';

-- 6. Produce a member-status summary showing each status, the number of members
--    in that status and the average outstanding amount for that status.
--    Round the average to two decimal places.
select status , count(*) as no_of_members,  round(avg(outstanding_amt),2) as average_out_amt from member group by status;

-- 7. Display cities having at least 2 registered members. Show the city,
--    number of members and total outstanding amount for that city.
--    Arrange by number of members descending.
select city,count(*) as no_of_members, sum(outstanding_amt) as total_out_amt from member group by city having count(member_id) >= 2 order by no_of_members;
-- 8. Display staff name, role, shift and salary for staff earning from
--    32,000 to 56,000 inclusive, excluding GENERAL shift staff.
--    Sort from highest to lowest salary.
select role_name,full_name,salary from staff where salary between 32000 and 56000 and shift_name != 'GENERAL' order by salary desc;
-- 9. For each shift in the STAFF table, display the number of employees,
--    minimum salary, maximum salary and average salary.
--    Round average salary to two decimal places.
select shift_name,count(*) as no_of_employees, max(salary) as maximum_sal, min(salary) as minimum_sal, round(avg(salary),2) as average_salary from staff group by shift_name;

-- 10. Display staff members hired before 1 January 2020 whose salary is above
--     50,000. Show staff ID, name, hire date and salary.
select staff_id,full_name,hire_date,salary from staff where hire_date < to_date('01-01-2020','DD-MM-YYYY') and salary > 50000;

    -- 11. Display each publisher's name, country and age in years in 2026
    --     (2026 - established_year). Show the oldest publishers first.
select publisher_name,country,(extract(year from sysdate) - established_year) as age from publisher order by age desc;

-- 12. Display countries that have at least two publishers in the database.
--     Show country and number of publishers.
select country,count(*) as no_of_publishers from publisher group by country having count(publisher_id) >= 2;

-- 13. Display authors born before 1960 who have received at least 2 awards.
--     Show author name, nationality, birth year and awards count, ordered by
--     awards count descending and then birth year ascending.
select author_name,nationality,birth_year,awards_count from author where birth_year < 1960 and awards_count >= 2 order by awards_count desc,birth_year asc;

-- 14. For each nationality in AUTHOR, display the number of authors and the
--     total number of awards received. Include only nationalities whose total
--     awards count is at least 5.
select nationality,count(*) as no_of_authors,sum(awards_count) as total_awards from author group by nationality having sum(awards_count) >= 5;

-- 15. Display book ID, title, category, publication year and price for books
--     published from 2014 onward with price above 700. Sort by price descending.
select book_id,title,category,publication_year,price from book where publication_year >= 2014 and price > 700 order by price desc;

-- 16. Display books whose title contains either the word 'Data' or the word
--     'Learning', ignoring case. Show title, category, year, pages and rating.
select title,category,publication_year,pages,rating from book where lower(title) like '%data%' or lower(title) like '%learning%';

-- 17. Display books with more than 500 pages and a rating of at least 4.5.
--     Add a computed column named PRICE_PER_100_PAGES showing the approximate
--     price per 100 pages, rounded to two decimals.
select title,pages,rating,round((price/pages)*100,2) as price_per_100_pages from book where pages > 500 and rating >= 4.5;

-- 18. Display the category-wise number of books, average price and average
--     rating. Show only categories containing at least 2 books.
--     Round averages to two decimals.
select category, count(*) as no_of_books, round(avg(price),2) as avg_price, round(avg(rating),2) as avg_rating from book group by category having count(book_id) > 2;

-- 19. Display publication years in which at least 2 books in the BOOK table
--     were published. Show the year, number of books and average price.
select publication_year, count(*) as no_of_books, round(avg(price),2) as avg_price from book group by publication_year having count(book_id) >= 2;

-- 20. Categorise every book using a CASE expression:
--       price < 400             -> 'BUDGET'
--       price between 400-799   -> 'STANDARD'
--       price >= 800            -> 'PREMIUM'
--     Display book title, price and the computed price category.
--     Sort by price descending.
select title,price, case when pages < 400 then 'BUDGET' when pages between 400 and 799 then 'STANDARD' when price >= 800 then 'PREMIUM' end as price_category from book order by price desc;

-- 21. Display all physical copies purchased during 2024 or 2025.
--     Show copy ID, accession number, purchase date, purchase price,
--     condition and availability status.
select copy_id,accession_no,purchase_date,purchase_price,condition_status,availability_status from book_copy where extract(year from purchase_date) in (2024,2025);
-- alternatively:
select copy_id, accession_no,purchase_date,purchase_price,condition_status,availability_status from book_copy where purchase_date between to_date('01-01-2024','DD-MM-YYYY') and to_date('31-12-2025','DD-MM-YYYY');

-- 22. Display the number of book copies in each availability status.
--     Show only statuses having at least 2 copies, ordered by count descending.
select availability_status, count(*) as no_of_copies from book_copy group by availability_status having count(copy_id) >= 2 order by no_of_copies desc;

-- 23. Display each condition status from BOOK_COPY together with the number of
--     copies and average purchase price. Round the average price to two decimals.


-- 24. Display currently unreturned loans (return_date IS NULL) that were issued
--     before 20 August 2026. Show loan ID, member ID, issue date, due date,
--     renewal count and loan status.


-- 25. For every loan, display loan ID, issue date, due date, return date and a
--     calculated column DAYS_ALLOWED equal to due_date - issue_date.
--     Sort by DAYS_ALLOWED descending and then loan ID.


-- 26. Display a summary of loans by loan_status showing the number of loans,
--     average renewal count and earliest issue date for each status.


-- 27. Display returned loans where the book was returned after the due date.
--     Show loan ID, member ID, due date, return date and the number of days late
--     calculated as return_date - due_date.


-- 28. Display reservations made during August 2026 that are still WAITING.
--     Show reservation ID, member ID, book ID, reservation date, expiry date
--     and priority number. Arrange by priority number and then reservation date.


-- 29. Display reservation-status counts, but include only statuses occurring
--     at least 2 times. Sort from most frequent to least frequent.


-- 30. Display fines that are not fully settled, i.e. payment_status is UNPAID
--     or PARTIAL. Show fine ID, member ID, reason, amount, amount paid and a
--     computed BALANCE_AMOUNT = amount - amount_paid. Sort by balance descending.



-- 31. From FINE, produce a reason-wise summary containing:
--     reason, number of fines, total amount charged, total amount paid and
--     total balance outstanding. Show reasons with total charged >= 100.


-- 32. Display the top-level borrowing pattern in LOAN by month of issue.
--     Show month as YYYY-MM, number of loans and average renewal count,
--     ordered chronologically.
--     Hint: TO_CHAR(issue_date, 'YYYY-MM').


-- 33. From MEMBER, display ACTIVE members whose membership expires within the
--     next 365 days from SYSDATE. Show name, member type, expiry date and the
--     approximate number of days remaining.


-- ============================================================
-- END OF QUESTION SET
-- ============================================================
