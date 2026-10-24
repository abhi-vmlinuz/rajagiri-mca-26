-- ============================================================
-- Section B / 4.3 : cleanup before re-running B3_01_to_07_views.sql
-- Drops the five views created by that script so the CREATE VIEW
-- statements run cleanly a second time.
-- Run as: sqlplus 'mca/mca'@localhost:1521/FREEPDB1 @B0_cleanup_views.sql
-- ============================================================
SET ECHO OFF
BEGIN
    FOR r IN (SELECT view_name FROM user_views
              WHERE view_name IN ('BOOK_DETAILS', 'MEMBER_DETAILS',
                                  'MEMBER_BRANCH_DETAILS',
                                  'BOOK_PUBLISHER_DETAILS', 'LOAN_DETAILS')) LOOP
        EXECUTE IMMEDIATE 'DROP VIEW ' || r.view_name;
    END LOOP;
END;
/
