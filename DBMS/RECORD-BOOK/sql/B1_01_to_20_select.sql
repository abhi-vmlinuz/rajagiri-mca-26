-- ============================================================
-- Section B : 4.1  Select Queries
-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================


PROMPT
PROMPT ===== Q1 =====

SELECT member_id, full_name, member_type, city
FROM member
WHERE status = 'ACTIVE'
ORDER BY member_type, full_name;

PROMPT
PROMPT ===== Q2 =====

SELECT member_id, full_name, outstanding_amt, status
FROM member
WHERE outstanding_amt BETWEEN 50 AND 300
ORDER BY outstanding_amt DESC;

PROMPT
PROMPT ===== Q3 =====

SELECT member_id, full_name, member_type, max_books
FROM member
WHERE member_type IN ('RESEARCHER', 'STUDENT')
  AND max_books >= 4
ORDER BY max_books DESC;

PROMPT
PROMPT ===== Q4 =====

SELECT full_name, join_date,
       TRUNC(MONTHS_BETWEEN(SYSDATE, join_date) / 12) AS completed_years
FROM member
ORDER BY completed_years DESC;

PROMPT
PROMPT ===== Q5 =====

SELECT LOWER(full_name) AS name, email
FROM member
WHERE LOWER(full_name) LIKE '%a%'
  AND status = 'ACTIVE';

PROMPT
PROMPT ===== Q6 =====

SELECT status, COUNT(*) AS no_of_members,
       ROUND(AVG(outstanding_amt), 2) AS average_out_amt
FROM member
GROUP BY status;

PROMPT
PROMPT ===== Q7 =====

SELECT city, COUNT(*) AS no_of_members,
       SUM(outstanding_amt) AS total_out_amt
FROM member
GROUP BY city
HAVING COUNT(member_id) >= 2
ORDER BY no_of_members DESC;

PROMPT
PROMPT ===== Q8 =====

SELECT full_name, role_name, shift_name, salary
FROM staff
WHERE salary BETWEEN 32000 AND 56000
  AND shift_name != 'GENERAL'
ORDER BY salary DESC;

PROMPT
PROMPT ===== Q9 =====

SELECT shift_name, COUNT(*) AS no_of_employees,
       MIN(salary) AS min_salary, MAX(salary) AS max_salary,
       ROUND(AVG(salary), 2) AS avg_salary
FROM staff
GROUP BY shift_name
ORDER BY shift_name;

PROMPT
PROMPT ===== Q10 =====

SELECT staff_id, full_name, hire_date, salary
FROM staff
WHERE hire_date < TO_DATE('01-01-2020', 'DD-MM-YYYY')
  AND salary > 50000
ORDER BY staff_id;

PROMPT
PROMPT ===== Q11 =====

SELECT publisher_name, country,
       (EXTRACT(YEAR FROM SYSDATE) - established_year) AS age
FROM publisher
ORDER BY age DESC;

PROMPT
PROMPT ===== Q12 =====

SELECT country, COUNT(*) AS no_of_publishers
FROM publisher
GROUP BY country
HAVING COUNT(publisher_id) >= 2
ORDER BY country;

PROMPT
PROMPT ===== Q13 =====

SELECT author_name, nationality, birth_year, awards_count
FROM author
WHERE birth_year < 1960
  AND awards_count >= 2
ORDER BY awards_count DESC, birth_year;

PROMPT
PROMPT ===== Q14 =====

SELECT nationality, COUNT(*) AS no_of_authors,
       SUM(awards_count) AS total_awards
FROM author
GROUP BY nationality
HAVING SUM(awards_count) >= 5
ORDER BY nationality;

PROMPT
PROMPT ===== Q15 =====

SELECT book_id, title, category, publication_year, price
FROM book
WHERE publication_year >= 2014
  AND price > 700
ORDER BY price DESC;

PROMPT
PROMPT ===== Q16 =====

SELECT title, category, publication_year, pages, rating
FROM book
WHERE LOWER(title) LIKE '%data%'
   OR LOWER(title) LIKE '%learning%'
ORDER BY book_id;

PROMPT
PROMPT ===== Q17 =====

SELECT title, pages, rating,
       ROUND((price / pages) * 100, 2) AS price_per_100_pages
FROM book
WHERE pages > 500
  AND rating >= 4.5
ORDER BY pages DESC;

PROMPT
PROMPT ===== Q18 =====

SELECT category, COUNT(*) AS no_of_books,
       ROUND(AVG(price), 2) AS avg_price,
       ROUND(AVG(rating), 2) AS avg_rating
FROM book
GROUP BY category
HAVING COUNT(book_id) >= 2
ORDER BY category;

PROMPT
PROMPT ===== Q19 =====

SELECT publication_year, COUNT(*) AS no_of_books,
       ROUND(AVG(price), 2) AS avg_price
FROM book
GROUP BY publication_year
HAVING COUNT(book_id) >= 2
ORDER BY publication_year;

PROMPT
PROMPT ===== Q20 =====

SELECT title, price,
       CAST(CASE WHEN price < 400 THEN 'BUDGET'
                 WHEN price BETWEEN 400 AND 799 THEN 'STANDARD'
                 WHEN price >= 800 THEN 'PREMIUM'
            END AS VARCHAR2(14)) AS price_category
FROM book
ORDER BY price DESC;
