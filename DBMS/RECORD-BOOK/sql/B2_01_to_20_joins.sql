-- ============================================================
-- Section B : 4.2  Joins
-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================


PROMPT
PROMPT ===== Q1 =====

SELECT b.title, p.publisher_name
FROM book b
JOIN publisher p ON p.publisher_id = b.publisher_id
ORDER BY b.book_id;

PROMPT
PROMPT ===== Q2 =====

SELECT m.full_name, m.member_type, br.branch_name
FROM member m
JOIN library_branch br ON br.branch_id = m.branch_id
ORDER BY m.member_id;

PROMPT
PROMPT ===== Q3 =====

SELECT s.full_name, s.role_name, br.branch_name
FROM staff s
JOIN library_branch br ON br.branch_id = s.branch_id
ORDER BY s.staff_id;

PROMPT
PROMPT ===== Q4 =====

SELECT b.title, a.author_name
FROM book b
JOIN book_author ba ON ba.book_id = b.book_id
JOIN author a ON a.author_id = ba.author_id
ORDER BY b.book_id, ba.author_order;

PROMPT
PROMPT ===== Q5 =====

SELECT r.reservation_id, m.full_name, b.title, r.reservation_status
FROM reservation r
JOIN member m ON m.member_id = r.member_id
JOIN book b ON b.book_id = r.book_id
ORDER BY r.reservation_id;

PROMPT
PROMPT ===== Q6 =====

SELECT f.fine_id, m.full_name, f.loan_id, f.amount, f.payment_status
FROM fine f
JOIN member m ON m.member_id = f.member_id
ORDER BY f.fine_id;

PROMPT
PROMPT ===== Q7 =====

SELECT br.branch_name, m.full_name
FROM library_branch br
LEFT JOIN member m ON m.branch_id = br.branch_id
ORDER BY br.branch_id, m.member_id;

PROMPT
PROMPT ===== Q8 =====

SELECT b.title, c.copy_id
FROM book b
LEFT JOIN book_copy c ON c.book_id = b.book_id
ORDER BY b.book_id, c.copy_id;

PROMPT
PROMPT ===== Q9 =====

SELECT m.full_name, l.loan_id
FROM member m
LEFT JOIN loan l ON l.member_id = m.member_id
ORDER BY m.member_id, l.loan_id;

PROMPT
PROMPT ===== Q10 =====

SELECT a.author_name, b.title
FROM author a
LEFT JOIN book_author ba ON ba.author_id = a.author_id
LEFT JOIN book b ON b.book_id = ba.book_id
ORDER BY a.author_id, b.title;

PROMPT
PROMPT ===== Q11 =====

SELECT p.publisher_name, b.title
FROM publisher p
LEFT JOIN book b ON b.publisher_id = p.publisher_id
ORDER BY p.publisher_id, b.book_id;

PROMPT
PROMPT ===== Q12 =====

SELECT br.branch_name, br.city, s.full_name
FROM staff s
RIGHT JOIN library_branch br ON br.branch_id = s.branch_id
ORDER BY br.branch_id, s.staff_id;

PROMPT
PROMPT ===== Q13 =====

SELECT b.title, c.copy_id, c.availability_status
FROM book b
RIGHT JOIN book_copy c ON c.book_id = b.book_id
ORDER BY c.copy_id;

PROMPT
PROMPT ===== Q14 =====

SELECT p.publisher_name, b.title, b.price
FROM publisher p
RIGHT JOIN book b ON b.publisher_id = p.publisher_id
ORDER BY b.book_id;

PROMPT
PROMPT ===== Q15 =====

SELECT br.branch_name, m.full_name
FROM library_branch br
FULL OUTER JOIN member m ON m.branch_id = br.branch_id
ORDER BY br.branch_id, m.member_id;

PROMPT
PROMPT ===== Q16 =====

SELECT b.title, r.reservation_id
FROM book b
FULL OUTER JOIN reservation r ON r.book_id = b.book_id
ORDER BY b.book_id, r.reservation_id;

PROMPT
PROMPT ===== Q17 =====

SELECT m.full_name, f.fine_id
FROM member m
FULL OUTER JOIN fine f ON f.member_id = m.member_id
ORDER BY m.member_id, f.fine_id;

PROMPT
PROMPT ===== Q18 =====

SELECT b.title, c.copy_id, l.branch_name
FROM book_copy c
NATURAL JOIN library_branch l
JOIN book b ON b.book_id = c.book_id
ORDER BY c.copy_id;

PROMPT
PROMPT ===== Q19 =====

SELECT m.full_name, b.title, c.accession_no, l.issue_date, l.loan_status
FROM loan l
JOIN member m ON m.member_id = l.member_id
JOIN book_copy c ON c.copy_id = l.copy_id
JOIN book b ON b.book_id = c.book_id
ORDER BY l.loan_id;

PROMPT
PROMPT ===== Q20 =====

SELECT b.title, p.publisher_name, a.author_name,
       ba.contribution_role
FROM book b
JOIN publisher p ON p.publisher_id = b.publisher_id
JOIN book_author ba ON ba.book_id = b.book_id
JOIN author a ON a.author_id = ba.author_id
ORDER BY b.book_id, ba.author_order;
