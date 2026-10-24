-- ============================================================
-- Section B : 4.4  TCL and DCL Commands
-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1
-- ============================================================


PROMPT
PROMPT ===== Q1 =====

UPDATE book SET price = price * 1.10
WHERE publisher_id = 201;
COMMIT;

PROMPT
PROMPT ===== Q2 =====

UPDATE member SET status = 'ACTIVE'
WHERE member_id = 1006 AND status = 'EXPIRED';
COMMIT;

PROMPT
PROMPT ===== Q3 =====

UPDATE book_copy SET availability_status = 'REPAIR'
WHERE copy_id = 6001;
COMMIT;

PROMPT
PROMPT ===== Q4 =====

UPDATE book SET price = 500 WHERE book_id = 4001;
SAVEPOINT price_update;
UPDATE book SET price = 900 WHERE book_id = 4001;
ROLLBACK TO price_update;

PROMPT
PROMPT ===== Q5 =====

UPDATE member SET status = 'SUSPENDED' WHERE member_id = 1007;
SAVEPOINT member_update;
UPDATE book SET price = 1200 WHERE book_id = 4007;
ROLLBACK TO member_update;
COMMIT;

PROMPT
PROMPT ===== Q6 =====

UPDATE book SET price = 420 WHERE book_id = 4002;
SAVEPOINT second_update;
UPDATE book SET price = 780 WHERE book_id = 4005;
ROLLBACK TO second_update;

PROMPT
PROMPT ===== Q7 =====

GRANT SELECT ON book TO libuser;

PROMPT
PROMPT ===== Q8 =====

GRANT SELECT ON book_details TO libuser;

PROMPT
PROMPT ===== Q9 =====

GRANT SELECT, INSERT ON member TO libuser;

PROMPT
PROMPT ===== Q10 =====

GRANT SELECT, UPDATE, DELETE ON book_copy TO libuser;

PROMPT
PROMPT ===== Q11 =====

GRANT SELECT ON member_branch_details TO libuser;

PROMPT
PROMPT ===== Q12 =====

REVOKE SELECT ON book FROM libuser;

PROMPT
PROMPT ===== Q13 =====

REVOKE INSERT ON member FROM libuser;

PROMPT
PROMPT ===== Q14 =====

REVOKE UPDATE, DELETE ON book_copy FROM libuser;

PROMPT
PROMPT ===== Q15 =====

REVOKE ALL ON book_details FROM libuser;
