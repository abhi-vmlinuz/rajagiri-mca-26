-- ============================================================
-- Section A : sample data used by the Basic SQL section
-- Run after A2_01_to_20_dml.sql and before A3_01_to_20_basic_sql.sql
-- ============================================================

SET LINESIZE 120
SET PAGESIZE 100

INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D02', 'Electronics', 'Block B', '9876500002');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D03', 'Mechanical', 'Block C', '9876500003');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D04', 'Civil', 'Block D', '9876500004');
INSERT INTO department (dept_id, dept_name, office_location, contact_number) VALUES
  ('D05', 'Information Tech', 'Block E', '9876500005');

INSERT INTO faculty VALUES
  ('F104', 'Suresh Menon', 'Professor', TO_DATE('12-07-2008','DD-MM-YYYY'), 95000, 'suresh@rajagiri.edu', 'D02', 18);
INSERT INTO faculty VALUES
  ('F105', 'Latha Nair', 'Associate Professor', TO_DATE('05-08-2015','DD-MM-YYYY'), 72000, 'latha@rajagiri.edu', 'D03', 11);
INSERT INTO faculty VALUES
  ('F106', 'Vinod Kumar', 'Assistant Professor', TO_DATE('18-01-2020','DD-MM-YYYY'), 48000, 'vinod@gmail.com', 'D04', 6);
INSERT INTO faculty VALUES
  ('F107', 'Priya Sharma', 'Assistant Professor', TO_DATE('02-03-2021','DD-MM-YYYY'), 52000, 'priya@rajagiri.edu', 'D05', 5);
INSERT INTO faculty VALUES
  ('F108', 'arun das', 'Assistant Professor', TO_DATE('15-06-2023','DD-MM-YYYY'), 45000, 'arun@yahoo.com', 'D01', 3);

INSERT INTO student VALUES
  ('S103', 'Anjali Menon', TO_DATE('11-02-2006','DD-MM-YYYY'), 'F', '9876501236', 'anjali@rajagiri.edu', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 9.1, 'Kochi', 'Kerala');
INSERT INTO student VALUES
  ('S104', 'Arjun Nair', TO_DATE('19-05-2005','DD-MM-YYYY'), 'M', '9876501237', 'arjun@gmail.com', 'D02', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.4, 'Thrissur', 'Kerala');
INSERT INTO student VALUES
  ('S105', 'Aparna Pillai', TO_DATE('23-09-2006','DD-MM-YYYY'), 'F', '9876501238', 'aparna@gmail.com', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 7.2, 'Alappuzha', 'Kerala');
INSERT INTO student VALUES
  ('S106', 'Rahul Varma', TO_DATE('07-12-2005','DD-MM-YYYY'), 'M', '9876501239', 'rahul@gmail.com', 'D03', TO_DATE('01-08-2025','DD-MM-YYYY'), 6.5, 'Kottayam', 'Kerala');
INSERT INTO student VALUES
  ('S107', 'Sneha George', TO_DATE('30-01-2006','DD-MM-YYYY'), 'F', '9876501240', 'sneha@gmail.com', 'D02', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.9, 'Ernakulam', 'Kerala');
INSERT INTO student VALUES
  ('S108', 'Aditya Kumar', TO_DATE('14-07-2005','DD-MM-YYYY'), 'M', '9876501241', 'aditya@gmail.com', 'D04', TO_DATE('01-08-2025','DD-MM-YYYY'), 5.8, 'Palakkad', 'Kerala');
INSERT INTO student VALUES
  ('S109', 'Meera Krishnan', TO_DATE('02-04-2006','DD-MM-YYYY'), 'F', '9876501242', 'meera.k@rajagiri.edu', 'D01', TO_DATE('01-08-2025','DD-MM-YYYY'), 9.6, 'Kochi', 'Kerala');
INSERT INTO student VALUES
  ('S110', 'Anoop Joseph', TO_DATE('27-10-2005','DD-MM-YYYY'), 'M', '9876501243', 'anoop@gmail.com', 'D05', TO_DATE('01-08-2025','DD-MM-YYYY'), 7.8, 'Idukki', 'Kerala');
INSERT INTO student VALUES
  ('S111', 'Divya Ramesh', TO_DATE('08-06-2006','DD-MM-YYYY'), 'F', '9876501244', 'divya@gmail.com', 'D03', TO_DATE('01-08-2025','DD-MM-YYYY'), 8.0, 'Kollam', 'Kerala');
INSERT INTO student VALUES
  ('S112', 'Kiran Mathew', TO_DATE('16-03-2005','DD-MM-YYYY'), 'M', '9876501245', 'kiran@gmail.com', 'D04', TO_DATE('01-08-2025','DD-MM-YYYY'), 6.9, 'Thiruvananthapuram', 'Kerala');

INSERT INTO course VALUES
  ('C103', 'Data Structures', 4, 3, 'D01', 'F106');
INSERT INTO course VALUES
  ('C104', 'Digital Electronics', 3, 1, 'D02', 'F104');
INSERT INTO course VALUES
  ('C105', 'Thermodynamics', 4, 3, 'D03', 'F105');
INSERT INTO course VALUES
  ('C106', 'Surveying', 3, 5, 'D04', 'F106');
INSERT INTO course VALUES
  ('C107', 'Operating Systems', 4, 5, 'D01', 'F107');
INSERT INTO course VALUES
  ('C108', 'Computer Networks', 3, 7, 'D01', 'F108');
INSERT INTO course VALUES
  ('C109', 'Software Engineering', 4, 5, 'D01', 'F101');
INSERT INTO course VALUES
  ('C110', 'Web Technologies', 2, 1, 'D05', 'F107');

INSERT INTO enrollment VALUES ('E102', 'S103', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E103', 'S104', 'C104', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E104', 'S105', 'C103', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E105', 'S106', 'C105', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E106', 'S107', 'C107', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E107', 'S108', 'C108', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E108', 'S109', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E109', 'S110', 'C110', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E110', 'S111', 'C106', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E111', 'S112', 'C109', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E112', 'S103', 'C104', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E113', 'S107', 'C101', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E114', 'S109', 'C107', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');
INSERT INTO enrollment VALUES ('E115', 'S111', 'C103', TO_DATE('05-08-2025','DD-MM-YYYY'), '2025-2026');

INSERT INTO result VALUES ('R102', 'E102', 45, 40, 85, 'A', 'PASS');
INSERT INTO result VALUES ('R103', 'E103', 38, 35, 73, 'B', 'PASS');
INSERT INTO result VALUES ('R104', 'E104', 42, 38, 80, 'A', 'PASS');
INSERT INTO result VALUES ('R105', 'E105', 25, 20, 45, 'F', 'FAIL');
INSERT INTO result VALUES ('R106', 'E106', 30, 28, 58, 'C', 'PASS');
INSERT INTO result VALUES ('R107', 'E107', 48, 45, 93, 'A', 'PASS');
INSERT INTO result VALUES ('R108', 'E108', 35, 30, 65, 'B', 'PASS');
INSERT INTO result VALUES ('R109', 'E109', 20, 15, 35, 'F', 'FAIL');
INSERT INTO result VALUES ('R110', 'E110', 40, 42, 82, 'A', 'PASS');
INSERT INTO result VALUES ('R111', 'E111', 28, 25, 53, 'C', 'PASS');
INSERT INTO result VALUES ('R112', 'E112', 44, 41, 85, 'A', 'PASS');
INSERT INTO result VALUES ('R113', 'E113', 33, 32, 65, 'B', 'PASS');
INSERT INTO result VALUES ('R114', 'E114', 22, 18, 40, 'F', 'FAIL');
INSERT INTO result VALUES ('R115', 'E115', 46, 44, 90, 'A', 'PASS');

INSERT INTO event VALUES ('EV04', 'Cultural Fest', TO_DATE('10-02-2026','DD-MM-YYYY'), 'Open Ground', 'F105', 500, 750);
INSERT INTO event VALUES ('EV05', 'Sports Meet', TO_DATE('20-01-2026','DD-MM-YYYY'), 'Sports Complex', 'F106', 200, 0);
INSERT INTO event VALUES ('EV06', 'Alumni Meet', TO_DATE('05-12-2025','DD-MM-YYYY'), 'Main Auditorium', 'F104', 80, 1500);

INSERT INTO event_registration VALUES ('REG02', 'EV01', 'S103', TO_DATE('10-03-2026','DD-MM-YYYY'), 'REGISTERED');
INSERT INTO event_registration VALUES ('REG03', 'EV01', 'S104', TO_DATE('10-03-2026','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG04', 'EV03', 'S105', TO_DATE('15-11-2025','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG05', 'EV04', 'S107', TO_DATE('01-02-2026','DD-MM-YYYY'), 'REGISTERED');
INSERT INTO event_registration VALUES ('REG06', 'EV04', 'S109', TO_DATE('02-02-2026','DD-MM-YYYY'), 'ATTENDED');
INSERT INTO event_registration VALUES ('REG07', 'EV06', 'S103', TO_DATE('28-11-2025','DD-MM-YYYY'), 'ATTENDED');

COMMIT;
