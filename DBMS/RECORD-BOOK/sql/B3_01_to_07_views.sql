-- ============================================================
-- Section B : 4.3  Views
-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================


PROMPT
PROMPT ===== Q1 =====

CREATE VIEW book_details AS
SELECT book_id, title, publisher_id, price
FROM book;

PROMPT
PROMPT ===== Q2 =====

CREATE VIEW member_details AS
SELECT member_id, full_name, member_type, status
FROM member;

PROMPT
PROMPT ===== Q3 =====

CREATE VIEW member_branch_details AS
SELECT m.full_name, m.member_type, br.branch_name, br.city
FROM member m
JOIN library_branch br ON br.branch_id = m.branch_id;

PROMPT
PROMPT ===== Q4 =====

CREATE VIEW book_publisher_details AS
SELECT b.title, p.publisher_name, b.price
FROM book b
JOIN publisher p ON p.publisher_id = b.publisher_id;

PROMPT
PROMPT ===== Q5 =====

CREATE VIEW loan_details AS
SELECT m.full_name, b.title, l.issue_date, l.due_date, l.loan_status
FROM loan l
JOIN member m ON m.member_id = l.member_id
JOIN book_copy c ON c.copy_id = l.copy_id
JOIN book b ON b.book_id = c.book_id;

PROMPT
PROMPT ===== Q6 =====

SELECT full_name, branch_name
FROM member_branch_details
ORDER BY full_name;

PROMPT
PROMPT ===== Q7 =====

SELECT title, publisher_name, price
FROM book_publisher_details
WHERE price > 500
ORDER BY price DESC;
