-- ============================================================
-- ONE-TIME CLEANUP  --  DESTRUCTIVE
-- Drops the 7 record tables that already exist in your schema
-- (with whatever rows they currently hold) so that the CREATE
-- statements in A1_02_to_08_tables.sql can run.
--
-- Your legacy DEPT table and its data are NOT touched.
-- Run this only after you have decided you do not need the
-- current contents of these 7 tables.
-- ============================================================

DROP TABLE event_registration CASCADE CONSTRAINTS;
DROP TABLE result CASCADE CONSTRAINTS;
DROP TABLE enrollment CASCADE CONSTRAINTS;
DROP TABLE event CASCADE CONSTRAINTS;
DROP TABLE course CASCADE CONSTRAINTS;
DROP TABLE student CASCADE CONSTRAINTS;
DROP TABLE faculty CASCADE CONSTRAINTS;
