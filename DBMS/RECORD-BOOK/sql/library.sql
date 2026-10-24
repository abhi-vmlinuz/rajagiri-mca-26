-- ============================================================
-- LIBRARY.SQL
-- Oracle SQL Library Ecosystem
-- Creates tables, constraints, indexes, and sample data.
-- Designed for Oracle 12c+ and Oracle SQL Developer.
-- ============================================================

-- Optional cleanup section.
-- Run these DROP statements manually only if the tables already exist.
-- DROP TABLE FINE CASCADE CONSTRAINTS;
-- DROP TABLE RESERVATION CASCADE CONSTRAINTS;
-- DROP TABLE LOAN CASCADE CONSTRAINTS;
-- DROP TABLE BOOK_COPY CASCADE CONSTRAINTS;
-- DROP TABLE BOOK_AUTHOR CASCADE CONSTRAINTS;
-- DROP TABLE BOOK CASCADE CONSTRAINTS;
-- DROP TABLE AUTHOR CASCADE CONSTRAINTS;
-- DROP TABLE PUBLISHER CASCADE CONSTRAINTS;
-- DROP TABLE STAFF CASCADE CONSTRAINTS;
-- DROP TABLE MEMBER CASCADE CONSTRAINTS;
-- DROP TABLE LIBRARY_BRANCH CASCADE CONSTRAINTS;

-- ============================================================
-- 1. LIBRARY_BRANCH
-- ============================================================
CREATE TABLE LIBRARY_BRANCH (
    branch_id       NUMBER(4)       CONSTRAINT pk_library_branch PRIMARY KEY,
    branch_name     VARCHAR2(100)   CONSTRAINT nn_branch_name NOT NULL,
    city            VARCHAR2(60)    CONSTRAINT nn_branch_city NOT NULL,
    phone           VARCHAR2(20),
    email           VARCHAR2(120),
    opening_year    NUMBER(4),
    floor_area_sqft NUMBER(8),
    CONSTRAINT uq_branch_email UNIQUE (email),
    CONSTRAINT ck_branch_year CHECK (opening_year BETWEEN 1900 AND 2100),
    CONSTRAINT ck_branch_area CHECK (floor_area_sqft > 0)
);

-- ============================================================
-- 2. MEMBER
-- ============================================================
CREATE TABLE MEMBER (
    member_id       NUMBER(6)       CONSTRAINT pk_member PRIMARY KEY,
    full_name       VARCHAR2(100)   CONSTRAINT nn_member_name NOT NULL,
    member_type     VARCHAR2(20)    CONSTRAINT nn_member_type NOT NULL,
    gender          CHAR(1),
    date_of_birth   DATE,
    join_date       DATE            DEFAULT SYSDATE,
    expiry_date     DATE,
    email           VARCHAR2(120),
    phone           VARCHAR2(20),
    city            VARCHAR2(60),
    status          VARCHAR2(15)    DEFAULT 'ACTIVE',
    max_books       NUMBER(2)       DEFAULT 4,
    outstanding_amt NUMBER(8,2)     DEFAULT 0,
    branch_id       NUMBER(4)       CONSTRAINT nn_member_branch NOT NULL,
    CONSTRAINT uq_member_email UNIQUE (email),
    CONSTRAINT ck_member_type CHECK (member_type IN ('STUDENT','FACULTY','PUBLIC','RESEARCHER')),
    CONSTRAINT ck_member_gender CHECK (gender IN ('M','F','O')),
    CONSTRAINT ck_member_status CHECK (status IN ('ACTIVE','EXPIRED','SUSPENDED')),
    CONSTRAINT ck_member_max_books CHECK (max_books BETWEEN 1 AND 20),
    CONSTRAINT ck_member_outstanding CHECK (outstanding_amt >= 0),
    CONSTRAINT fk_member_branch FOREIGN KEY (branch_id)
        REFERENCES LIBRARY_BRANCH(branch_id)
);

-- ============================================================
-- 3. STAFF
-- ============================================================
CREATE TABLE STAFF (
    staff_id        NUMBER(5)       CONSTRAINT pk_staff PRIMARY KEY,
    full_name       VARCHAR2(100)   CONSTRAINT nn_staff_name NOT NULL,
    role_name       VARCHAR2(40)    CONSTRAINT nn_staff_role NOT NULL,
    hire_date       DATE            CONSTRAINT nn_staff_hire NOT NULL,
    salary          NUMBER(10,2)    CONSTRAINT nn_staff_salary NOT NULL,
    shift_name      VARCHAR2(15),
    email           VARCHAR2(120),
    branch_id       NUMBER(4)       CONSTRAINT nn_staff_branch NOT NULL,
    CONSTRAINT uq_staff_email UNIQUE (email),
    CONSTRAINT ck_staff_salary CHECK (salary > 0),
    CONSTRAINT ck_staff_shift CHECK (shift_name IN ('MORNING','EVENING','GENERAL')),
    CONSTRAINT fk_staff_branch FOREIGN KEY (branch_id)
        REFERENCES LIBRARY_BRANCH(branch_id)
);

-- ============================================================
-- 4. PUBLISHER
-- ============================================================
CREATE TABLE PUBLISHER (
    publisher_id    NUMBER(5)       CONSTRAINT pk_publisher PRIMARY KEY,
    publisher_name  VARCHAR2(120)   CONSTRAINT nn_publisher_name NOT NULL,
    country         VARCHAR2(60),
    city            VARCHAR2(60),
    website         VARCHAR2(150),
    established_year NUMBER(4),
    CONSTRAINT uq_publisher_name UNIQUE (publisher_name),
    CONSTRAINT ck_publisher_year CHECK (established_year BETWEEN 1400 AND 2100)
);

-- ============================================================
-- 5. AUTHOR
-- ============================================================
CREATE TABLE AUTHOR (
    author_id       NUMBER(6)       CONSTRAINT pk_author PRIMARY KEY,
    author_name     VARCHAR2(120)   CONSTRAINT nn_author_name NOT NULL,
    nationality     VARCHAR2(60),
    birth_year      NUMBER(4),
    primary_genre   VARCHAR2(50),
    awards_count    NUMBER(3)       DEFAULT 0,
    CONSTRAINT ck_author_birth CHECK (birth_year BETWEEN 1500 AND 2100),
    CONSTRAINT ck_author_awards CHECK (awards_count >= 0)
);

-- ============================================================
-- 6. BOOK
-- ============================================================
CREATE TABLE BOOK (
    book_id          NUMBER(7)       CONSTRAINT pk_book PRIMARY KEY,
    isbn             VARCHAR2(20)    CONSTRAINT nn_book_isbn NOT NULL,
    title            VARCHAR2(180)   CONSTRAINT nn_book_title NOT NULL,
    category         VARCHAR2(50)    CONSTRAINT nn_book_category NOT NULL,
    language_name    VARCHAR2(30)    DEFAULT 'English',
    publication_year NUMBER(4),
    edition_no       NUMBER(3)       DEFAULT 1,
    pages            NUMBER(5),
    price            NUMBER(9,2),
    rating           NUMBER(3,1),
    publisher_id     NUMBER(5)       CONSTRAINT nn_book_publisher NOT NULL,
    CONSTRAINT uq_book_isbn UNIQUE (isbn),
    CONSTRAINT ck_book_year CHECK (publication_year BETWEEN 1500 AND 2100),
    CONSTRAINT ck_book_edition CHECK (edition_no >= 1),
    CONSTRAINT ck_book_pages CHECK (pages > 0),
    CONSTRAINT ck_book_price CHECK (price >= 0),
    CONSTRAINT ck_book_rating CHECK (rating BETWEEN 0 AND 5),
    CONSTRAINT fk_book_publisher FOREIGN KEY (publisher_id)
        REFERENCES PUBLISHER(publisher_id)
);

-- ============================================================
-- 7. BOOK_AUTHOR
-- Many-to-many bridge between BOOK and AUTHOR.
-- ============================================================
CREATE TABLE BOOK_AUTHOR (
    book_id          NUMBER(7),
    author_id        NUMBER(6),
    author_order     NUMBER(2) DEFAULT 1,
    contribution_role VARCHAR2(30) DEFAULT 'AUTHOR',
    CONSTRAINT pk_book_author PRIMARY KEY (book_id, author_id),
    CONSTRAINT ck_author_order CHECK (author_order >= 1),
    CONSTRAINT ck_contribution_role CHECK (
        contribution_role IN ('AUTHOR','EDITOR','CO-AUTHOR','TRANSLATOR')
    ),
    CONSTRAINT fk_ba_book FOREIGN KEY (book_id)
        REFERENCES BOOK(book_id),
    CONSTRAINT fk_ba_author FOREIGN KEY (author_id)
        REFERENCES AUTHOR(author_id)
);

-- ============================================================
-- 8. BOOK_COPY
-- Physical copy of a book held by a branch.
-- ============================================================
CREATE TABLE BOOK_COPY (
    copy_id          NUMBER(8)       CONSTRAINT pk_book_copy PRIMARY KEY,
    book_id          NUMBER(7)       CONSTRAINT nn_copy_book NOT NULL,
    branch_id        NUMBER(4)       CONSTRAINT nn_copy_branch NOT NULL,
    accession_no     VARCHAR2(30)    CONSTRAINT nn_accession NOT NULL,
    shelf_code       VARCHAR2(20),
    purchase_date    DATE,
    purchase_price   NUMBER(9,2),
    condition_status VARCHAR2(20)    DEFAULT 'GOOD',
    availability_status VARCHAR2(20) DEFAULT 'AVAILABLE',
    CONSTRAINT uq_copy_accession UNIQUE (accession_no),
    CONSTRAINT ck_copy_price CHECK (purchase_price >= 0),
    CONSTRAINT ck_copy_condition CHECK (
        condition_status IN ('NEW','GOOD','FAIR','DAMAGED')
    ),
    CONSTRAINT ck_copy_availability CHECK (
        availability_status IN ('AVAILABLE','ISSUED','RESERVED','LOST','REPAIR')
    ),
    CONSTRAINT fk_copy_book FOREIGN KEY (book_id)
        REFERENCES BOOK(book_id),
    CONSTRAINT fk_copy_branch FOREIGN KEY (branch_id)
        REFERENCES LIBRARY_BRANCH(branch_id)
);

-- ============================================================
-- 9. LOAN
-- ============================================================
CREATE TABLE LOAN (
    loan_id          NUMBER(9)       CONSTRAINT pk_loan PRIMARY KEY,
    copy_id          NUMBER(8)       CONSTRAINT nn_loan_copy NOT NULL,
    member_id        NUMBER(6)       CONSTRAINT nn_loan_member NOT NULL,
    issued_by        NUMBER(5)       CONSTRAINT nn_loan_staff NOT NULL,
    issue_date       DATE            CONSTRAINT nn_issue_date NOT NULL,
    due_date         DATE            CONSTRAINT nn_due_date NOT NULL,
    return_date      DATE,
    renewal_count    NUMBER(2)       DEFAULT 0,
    loan_status      VARCHAR2(15)    DEFAULT 'ISSUED',
    CONSTRAINT ck_loan_dates CHECK (due_date >= issue_date),
    CONSTRAINT ck_renewal_count CHECK (renewal_count BETWEEN 0 AND 5),
    CONSTRAINT ck_loan_status CHECK (
        loan_status IN ('ISSUED','RETURNED','OVERDUE','LOST')
    ),
    CONSTRAINT fk_loan_copy FOREIGN KEY (copy_id)
        REFERENCES BOOK_COPY(copy_id),
    CONSTRAINT fk_loan_member FOREIGN KEY (member_id)
        REFERENCES MEMBER(member_id),
    CONSTRAINT fk_loan_staff FOREIGN KEY (issued_by)
        REFERENCES STAFF(staff_id)
);

-- ============================================================
-- 10. RESERVATION
-- ============================================================
CREATE TABLE RESERVATION (
    reservation_id  NUMBER(9)       CONSTRAINT pk_reservation PRIMARY KEY,
    member_id       NUMBER(6)       CONSTRAINT nn_res_member NOT NULL,
    book_id         NUMBER(7)       CONSTRAINT nn_res_book NOT NULL,
    reservation_date DATE           CONSTRAINT nn_res_date NOT NULL,
    expiry_date     DATE,
    priority_no     NUMBER(3)       DEFAULT 1,
    reservation_status VARCHAR2(15) DEFAULT 'WAITING',
    CONSTRAINT ck_res_priority CHECK (priority_no >= 1),
    CONSTRAINT ck_res_dates CHECK (expiry_date IS NULL OR expiry_date >= reservation_date),
    CONSTRAINT ck_res_status CHECK (
        reservation_status IN ('WAITING','FULFILLED','CANCELLED','EXPIRED')
    ),
    CONSTRAINT fk_res_member FOREIGN KEY (member_id)
        REFERENCES MEMBER(member_id),
    CONSTRAINT fk_res_book FOREIGN KEY (book_id)
        REFERENCES BOOK(book_id)
);

-- ============================================================
-- 11. FINE
-- ============================================================
CREATE TABLE FINE (
    fine_id          NUMBER(9)       CONSTRAINT pk_fine PRIMARY KEY,
    loan_id          NUMBER(9)       CONSTRAINT nn_fine_loan NOT NULL,
    member_id        NUMBER(6)       CONSTRAINT nn_fine_member NOT NULL,
    fine_date        DATE            CONSTRAINT nn_fine_date NOT NULL,
    reason           VARCHAR2(40)    CONSTRAINT nn_fine_reason NOT NULL,
    amount           NUMBER(8,2)     CONSTRAINT nn_fine_amount NOT NULL,
    amount_paid      NUMBER(8,2)     DEFAULT 0,
    payment_status   VARCHAR2(15)    DEFAULT 'UNPAID',
    payment_date     DATE,
    CONSTRAINT ck_fine_amount CHECK (amount >= 0),
    CONSTRAINT ck_fine_paid CHECK (amount_paid >= 0 AND amount_paid <= amount),
    CONSTRAINT ck_fine_reason CHECK (
        reason IN ('LATE RETURN','LOST BOOK','DAMAGE','OTHER')
    ),
    CONSTRAINT ck_payment_status CHECK (
        payment_status IN ('UNPAID','PARTIAL','PAID','WAIVED')
    ),
    CONSTRAINT fk_fine_loan FOREIGN KEY (loan_id)
        REFERENCES LOAN(loan_id),
    CONSTRAINT fk_fine_member FOREIGN KEY (member_id)
        REFERENCES MEMBER(member_id)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_book_title ON BOOK(title);
CREATE INDEX idx_book_category ON BOOK(category);
CREATE INDEX idx_member_city ON MEMBER(city);
CREATE INDEX idx_loan_status ON LOAN(loan_status);
CREATE INDEX idx_res_status ON RESERVATION(reservation_status);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- LIBRARY_BRANCH
INSERT INTO LIBRARY_BRANCH VALUES (101, 'Central Library', 'Kochi', '0484-2201001', 'central@library.org', 1985, 18500);
INSERT INTO LIBRARY_BRANCH VALUES (102, 'Riverside Branch', 'Aluva', '0484-2622002', 'riverside@library.org', 1998, 9200);
INSERT INTO LIBRARY_BRANCH VALUES (103, 'Knowledge Hub', 'Kakkanad', '0484-2423003', 'knowledge@library.org', 2012, 12600);
INSERT INTO LIBRARY_BRANCH VALUES (104, 'Community Library', 'Thrippunithura', '0484-2774004', 'community@library.org', 2005, 7800);

-- MEMBER
INSERT INTO MEMBER VALUES (1001, 'Aarav Menon', 'STUDENT', 'M', DATE '2004-08-14', DATE '2024-06-10', DATE '2027-06-09', 'aarav.m@example.com', '9000001001', 'Kochi', 'ACTIVE', 4, 0, 101);
INSERT INTO MEMBER VALUES (1002, 'Diya Nair', 'STUDENT', 'F', DATE '2005-02-02', DATE '2024-07-01', DATE '2027-06-30', 'diya.n@example.com', '9000001002', 'Aluva', 'ACTIVE', 4, 35, 102);
INSERT INTO MEMBER VALUES (1003, 'Meera Thomas', 'FACULTY', 'F', DATE '1988-11-23', DATE '2022-01-15', DATE '2027-01-14', 'meera.t@example.com', '9000001003', 'Kakkanad', 'ACTIVE', 8, 0, 103);
INSERT INTO MEMBER VALUES (1004, 'Rohan Joseph', 'PUBLIC', 'M', DATE '1991-05-17', DATE '2023-09-11', DATE '2026-09-10', 'rohan.j@example.com', '9000001004', 'Kochi', 'ACTIVE', 3, 120, 101);
INSERT INTO MEMBER VALUES (1005, 'Ananya Pillai', 'RESEARCHER', 'F', DATE '1997-03-09', DATE '2021-08-20', DATE '2027-08-19', 'ananya.p@example.com', '9000001005', 'Thrippunithura', 'ACTIVE', 10, 0, 104);
INSERT INTO MEMBER VALUES (1006, 'Nikhil Raj', 'STUDENT', 'M', DATE '2003-12-30', DATE '2023-06-05', DATE '2026-06-04', 'nikhil.r@example.com', '9000001006', 'Aluva', 'EXPIRED', 4, 75, 102);
INSERT INTO MEMBER VALUES (1007, 'Sara Mathew', 'FACULTY', 'F', DATE '1982-07-18', DATE '2020-02-10', DATE '2028-02-09', 'sara.m@example.com', '9000001007', 'Kochi', 'ACTIVE', 8, 0, 101);
INSERT INTO MEMBER VALUES (1008, 'Vivek Krishnan', 'PUBLIC', 'M', DATE '1979-09-27', DATE '2025-01-05', DATE '2026-01-04', 'vivek.k@example.com', '9000001008', 'Kakkanad', 'EXPIRED', 3, 0, 103);
INSERT INTO MEMBER VALUES (1009, 'Ishita Rao', 'STUDENT', 'F', DATE '2004-04-12', DATE '2024-06-10', DATE '2027-06-09', 'ishita.r@example.com', '9000001009', 'Kochi', 'ACTIVE', 4, 10, 101);
INSERT INTO MEMBER VALUES (1010, 'Adil Khan', 'RESEARCHER', 'M', DATE '1994-01-15', DATE '2019-10-01', DATE '2027-09-30', 'adil.k@example.com', '9000001010', 'Kakkanad', 'ACTIVE', 10, 250, 103);
INSERT INTO MEMBER VALUES (1011, 'Liya George', 'STUDENT', 'F', DATE '2005-06-26', DATE '2025-06-12', DATE '2028-06-11', 'liya.g@example.com', '9000001011', 'Thrippunithura', 'ACTIVE', 4, 0, 104);
INSERT INTO MEMBER VALUES (1012, 'Harish Kumar', 'PUBLIC', 'M', DATE '1975-10-04', DATE '2022-11-20', DATE '2026-11-19', 'harish.k@example.com', '9000001012', 'Aluva', 'SUSPENDED', 3, 480, 102);
INSERT INTO MEMBER VALUES (1013, 'Neha Varma', 'FACULTY', 'F', DATE '1990-02-19', DATE '2023-03-03', DATE '2028-03-02', 'neha.v@example.com', '9000001013', 'Kakkanad', 'ACTIVE', 8, 0, 103);
INSERT INTO MEMBER VALUES (1014, 'Joel Antony', 'STUDENT', 'M', DATE '2002-08-08', DATE '2022-06-15', DATE '2026-06-14', 'joel.a@example.com', '9000001014', 'Kochi', 'EXPIRED', 4, 60, 101);
INSERT INTO MEMBER VALUES (1015, 'Fathima Noor', 'RESEARCHER', 'F', DATE '1996-12-01', DATE '2024-04-18', DATE '2027-04-17', 'fathima.n@example.com', '9000001015', 'Aluva', 'ACTIVE', 10, 20, 102);

-- STAFF
INSERT INTO STAFF VALUES (501, 'Lakshmi Menon', 'Chief Librarian', DATE '2010-06-01', 72000, 'GENERAL', 'lakshmi@library.org', 101);
INSERT INTO STAFF VALUES (502, 'Arun Das', 'Assistant Librarian', DATE '2018-08-16', 48000, 'MORNING', 'arun@library.org', 101);
INSERT INTO STAFF VALUES (503, 'Jency Paul', 'Librarian', DATE '2016-01-20', 55000, 'GENERAL', 'jency@library.org', 102);
INSERT INTO STAFF VALUES (504, 'Rahul Dev', 'Library Assistant', DATE '2022-07-04', 32000, 'EVENING', 'rahul@library.org', 102);
INSERT INTO STAFF VALUES (505, 'Priya Raman', 'Librarian', DATE '2017-09-11', 56000, 'GENERAL', 'priya@library.org', 103);
INSERT INTO STAFF VALUES (506, 'Manu Suresh', 'Library Assistant', DATE '2021-11-08', 34000, 'MORNING', 'manu@library.org', 103);
INSERT INTO STAFF VALUES (507, 'Elsa John', 'Librarian', DATE '2019-05-13', 52000, 'GENERAL', 'elsa@library.org', 104);
INSERT INTO STAFF VALUES (508, 'Akhil Babu', 'Library Assistant', DATE '2023-02-01', 30000, 'EVENING', 'akhil@library.org', 104);

-- PUBLISHER
INSERT INTO PUBLISHER VALUES (201, 'Pearson Education', 'United Kingdom', 'London', 'https://www.pearson.com', 1844);
INSERT INTO PUBLISHER VALUES (202, 'Penguin Random House', 'United States', 'New York', 'https://www.penguinrandomhouse.com', 2013);
INSERT INTO PUBLISHER VALUES (203, 'O''Reilly Media', 'United States', 'Sebastopol', 'https://www.oreilly.com', 1978);
INSERT INTO PUBLISHER VALUES (204, 'HarperCollins', 'United States', 'New York', 'https://www.harpercollins.com', 1989);
INSERT INTO PUBLISHER VALUES (205, 'Oxford University Press', 'United Kingdom', 'Oxford', 'https://global.oup.com', 1586);
INSERT INTO PUBLISHER VALUES (206, 'MIT Press', 'United States', 'Cambridge', 'https://mitpress.mit.edu', 1962);
INSERT INTO PUBLISHER VALUES (207, 'DC Books', 'India', 'Kottayam', 'https://www.dcbooks.com', 1974);
INSERT INTO PUBLISHER VALUES (208, 'Springer', 'Germany', 'Berlin', 'https://www.springer.com', 1842);

-- AUTHOR
INSERT INTO AUTHOR VALUES (301, 'George Orwell', 'British', 1903, 'Dystopian Fiction', 3);
INSERT INTO AUTHOR VALUES (302, 'Jane Austen', 'British', 1775, 'Classic Fiction', 2);
INSERT INTO AUTHOR VALUES (303, 'Robert C. Martin', 'American', 1952, 'Software Engineering', 1);
INSERT INTO AUTHOR VALUES (304, 'Yuval Noah Harari', 'Israeli', 1976, 'History', 4);
INSERT INTO AUTHOR VALUES (305, 'A. P. J. Abdul Kalam', 'Indian', 1931, 'Biography', 8);
INSERT INTO AUTHOR VALUES (306, 'Arundhati Roy', 'Indian', 1961, 'Literary Fiction', 6);
INSERT INTO AUTHOR VALUES (307, 'Thomas H. Cormen', 'American', 1956, 'Computer Science', 2);
INSERT INTO AUTHOR VALUES (308, 'Charles E. Leiserson', 'American', 1953, 'Computer Science', 2);
INSERT INTO AUTHOR VALUES (309, 'Ronald L. Rivest', 'American', 1947, 'Computer Science', 5);
INSERT INTO AUTHOR VALUES (310, 'Clifford Stein', 'American', 1965, 'Computer Science', 1);
INSERT INTO AUTHOR VALUES (311, 'Andrew S. Tanenbaum', 'Dutch-American', 1944, 'Computer Science', 3);
INSERT INTO AUTHOR VALUES (312, 'K. R. Meera', 'Indian', 1970, 'Malayalam Fiction', 7);

-- BOOK
INSERT INTO BOOK VALUES (4001, '9780451524935', '1984', 'Fiction', 'English', 1949, 1, 328, 399, 4.6, 202);
INSERT INTO BOOK VALUES (4002, '9780141439518', 'Pride and Prejudice', 'Fiction', 'English', 1813, 3, 480, 450, 4.7, 202);
INSERT INTO BOOK VALUES (4003, '9780132350884', 'Clean Code', 'Computer Science', 'English', 2008, 1, 464, 899, 4.5, 201);
INSERT INTO BOOK VALUES (4004, '9780062316097', 'Sapiens', 'History', 'English', 2014, 1, 498, 699, 4.4, 204);
INSERT INTO BOOK VALUES (4005, '9788173711466', 'Wings of Fire', 'Biography', 'English', 1999, 1, 180, 350, 4.8, 207);
INSERT INTO BOOK VALUES (4006, '9780670087115', 'The God of Small Things', 'Fiction', 'English', 1997, 2, 352, 499, 4.2, 202);
INSERT INTO BOOK VALUES (4007, '9780262046305', 'Introduction to Algorithms', 'Computer Science', 'English', 2022, 4, 1312, 1099, 4.7, 206);
INSERT INTO BOOK VALUES (4008, '9780133591620', 'Modern Operating Systems', 'Computer Science', 'English', 2014, 4, 1136, 950, 4.5, 201);
INSERT INTO BOOK VALUES (4009, '9789355423481', 'Aarachar', 'Fiction', 'Malayalam', 2012, 5, 552, 525, 4.6, 207);
INSERT INTO BOOK VALUES (4010, '9780199535569', 'The Picture of Dorian Gray', 'Fiction', 'English', 1890, 2, 304, 375, 4.3, 205);
INSERT INTO BOOK VALUES (4011, '9781491950357', 'Designing Data-Intensive Applications', 'Computer Science', 'English', 2017, 1, 616, 999, 4.8, 203);
INSERT INTO BOOK VALUES (4012, '9781492078005', 'Learning SQL', 'Computer Science', 'English', 2020, 3, 384, 799, 4.4, 203);
INSERT INTO BOOK VALUES (4013, '9780198829191', 'Artificial Intelligence: A Modern Approach', 'Computer Science', 'English', 2021, 4, 1168, 1199, 4.6, 201);
INSERT INTO BOOK VALUES (4014, '9780061120084', 'To Kill a Mockingbird', 'Fiction', 'English', 1960, 1, 336, 499, 4.8, 204);
INSERT INTO BOOK VALUES (4015, '9789356291522', 'India 2020', 'Technology', 'English', 1998, 2, 336, 325, 4.1, 204);
INSERT INTO BOOK VALUES (4016, '9780262035613', 'Deep Learning', 'Computer Science', 'English', 2016, 1, 800, 1050, 4.5, 206);
INSERT INTO BOOK VALUES (4017, '9780192802385', 'A Brief History of Time', 'Science', 'English', 1988, 2, 256, 425, 4.6, 205);
INSERT INTO BOOK VALUES (4018, '9789356290990', 'The Alchemist', 'Fiction', 'English', 1988, 1, 208, 299, 4.5, 204);
INSERT INTO BOOK VALUES (4019, '9783030808969', 'Machine Learning with Python', 'Computer Science', 'English', 2022, 2, 540, 875, 4.2, 208);
INSERT INTO BOOK VALUES (4020, '9789355421128', 'Qabar', 'Fiction', 'Malayalam', 2020, 1, 248, 280, 4.1, 207);

-- BOOK_AUTHOR
INSERT INTO BOOK_AUTHOR VALUES (4001, 301, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4002, 302, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4003, 303, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4004, 304, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4005, 305, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4006, 306, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4007, 307, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4007, 308, 2, 'CO-AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4007, 309, 3, 'CO-AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4007, 310, 4, 'CO-AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4008, 311, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4009, 312, 1, 'AUTHOR');
INSERT INTO BOOK_AUTHOR VALUES (4015, 305, 1, 'AUTHOR');

-- BOOK_COPY
INSERT INTO BOOK_COPY VALUES (6001, 4001, 101, 'ACC-C-0001', 'FIC-A1', DATE '2023-01-10', 340, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6002, 4001, 102, 'ACC-R-0001', 'FIC-B1', DATE '2024-02-18', 360, 'NEW', 'ISSUED');
INSERT INTO BOOK_COPY VALUES (6003, 4002, 101, 'ACC-C-0002', 'FIC-A2', DATE '2022-08-14', 420, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6004, 4003, 101, 'ACC-C-0003', 'CS-C1', DATE '2023-06-01', 840, 'GOOD', 'ISSUED');
INSERT INTO BOOK_COPY VALUES (6005, 4003, 103, 'ACC-K-0001', 'CS-A1', DATE '2024-07-12', 880, 'NEW', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6006, 4004, 104, 'ACC-T-0001', 'HIS-A1', DATE '2023-09-20', 640, 'GOOD', 'RESERVED');
INSERT INTO BOOK_COPY VALUES (6007, 4005, 102, 'ACC-R-0002', 'BIO-A1', DATE '2021-01-25', 300, 'FAIR', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6008, 4006, 101, 'ACC-C-0004', 'FIC-A3', DATE '2022-11-04', 460, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6009, 4007, 103, 'ACC-K-0002', 'CS-A2', DATE '2024-08-05', 1040, 'NEW', 'ISSUED');
INSERT INTO BOOK_COPY VALUES (6010, 4007, 101, 'ACC-C-0005', 'CS-C2', DATE '2023-12-02', 1010, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6011, 4008, 104, 'ACC-T-0002', 'CS-B1', DATE '2022-05-18', 900, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6012, 4009, 104, 'ACC-T-0003', 'MAL-A1', DATE '2025-01-20', 500, 'NEW', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6013, 4010, 102, 'ACC-R-0003', 'FIC-B2', DATE '2020-03-11', 320, 'FAIR', 'REPAIR');
INSERT INTO BOOK_COPY VALUES (6014, 4011, 103, 'ACC-K-0003', 'CS-A3', DATE '2025-02-10', 940, 'NEW', 'ISSUED');
INSERT INTO BOOK_COPY VALUES (6015, 4012, 101, 'ACC-C-0006', 'CS-C3', DATE '2024-04-09', 750, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6016, 4013, 103, 'ACC-K-0004', 'CS-A4', DATE '2025-06-15', 1120, 'NEW', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6017, 4014, 102, 'ACC-R-0004', 'FIC-B3', DATE '2021-10-01', 430, 'GOOD', 'ISSUED');
INSERT INTO BOOK_COPY VALUES (6018, 4015, 101, 'ACC-C-0007', 'TEC-A1', DATE '2019-09-19', 275, 'FAIR', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6019, 4016, 103, 'ACC-K-0005', 'CS-A5', DATE '2024-10-22', 980, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6020, 4017, 104, 'ACC-T-0004', 'SCI-A1', DATE '2022-01-17', 390, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6021, 4018, 101, 'ACC-C-0008', 'FIC-A4', DATE '2020-08-08', 260, 'FAIR', 'LOST');
INSERT INTO BOOK_COPY VALUES (6022, 4019, 102, 'ACC-R-0005', 'CS-B2', DATE '2025-03-24', 830, 'NEW', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6023, 4020, 104, 'ACC-T-0005', 'MAL-A2', DATE '2024-12-12', 250, 'GOOD', 'AVAILABLE');
INSERT INTO BOOK_COPY VALUES (6024, 4011, 101, 'ACC-C-0009', 'CS-C4', DATE '2025-05-02', 960, 'NEW', 'RESERVED');

-- LOAN
INSERT INTO LOAN VALUES (7001, 6002, 1002, 503, DATE '2026-08-20', DATE '2026-09-03', NULL, 0, 'ISSUED');
INSERT INTO LOAN VALUES (7002, 6004, 1001, 502, DATE '2026-08-12', DATE '2026-08-26', NULL, 1, 'OVERDUE');
INSERT INTO LOAN VALUES (7003, 6009, 1005, 505, DATE '2026-08-24', DATE '2026-09-07', NULL, 0, 'ISSUED');
INSERT INTO LOAN VALUES (7004, 6014, 1010, 506, DATE '2026-08-01', DATE '2026-08-15', NULL, 2, 'OVERDUE');
INSERT INTO LOAN VALUES (7005, 6017, 1004, 504, DATE '2026-08-22', DATE '2026-09-05', NULL, 0, 'ISSUED');
INSERT INTO LOAN VALUES (7006, 6001, 1003, 501, DATE '2026-07-02', DATE '2026-07-23', DATE '2026-07-20', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7007, 6003, 1007, 502, DATE '2026-06-11', DATE '2026-07-02', DATE '2026-07-05', 1, 'RETURNED');
INSERT INTO LOAN VALUES (7008, 6007, 1009, 503, DATE '2026-07-18', DATE '2026-08-01', DATE '2026-08-01', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7009, 6008, 1011, 501, DATE '2026-07-21', DATE '2026-08-04', DATE '2026-08-03', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7010, 6010, 1013, 505, DATE '2026-05-02', DATE '2026-05-23', DATE '2026-05-30', 1, 'RETURNED');
INSERT INTO LOAN VALUES (7011, 6011, 1006, 507, DATE '2026-04-14', DATE '2026-04-28', DATE '2026-05-04', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7012, 6012, 1015, 507, DATE '2026-03-05', DATE '2026-03-26', DATE '2026-03-20', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7013, 6013, 1008, 504, DATE '2026-02-01', DATE '2026-02-15', DATE '2026-02-22', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7014, 6015, 1001, 502, DATE '2026-01-12', DATE '2026-01-26', DATE '2026-01-26', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7015, 6018, 1014, 501, DATE '2025-12-10', DATE '2025-12-24', DATE '2026-01-03', 0, 'RETURNED');
INSERT INTO LOAN VALUES (7016, 6021, 1012, 503, DATE '2026-06-01', DATE '2026-06-15', NULL, 0, 'LOST');

-- RESERVATION
INSERT INTO RESERVATION VALUES (8001, 1003, 4007, DATE '2026-08-25', DATE '2026-09-08', 1, 'WAITING');
INSERT INTO RESERVATION VALUES (8002, 1009, 4004, DATE '2026-08-26', DATE '2026-09-09', 2, 'WAITING');
INSERT INTO RESERVATION VALUES (8003, 1011, 4011, DATE '2026-08-28', DATE '2026-09-11', 1, 'WAITING');
INSERT INTO RESERVATION VALUES (8004, 1005, 4003, DATE '2026-07-15', DATE '2026-07-29', 1, 'FULFILLED');
INSERT INTO RESERVATION VALUES (8005, 1002, 4013, DATE '2026-06-18', DATE '2026-07-02', 3, 'CANCELLED');
INSERT INTO RESERVATION VALUES (8006, 1015, 4009, DATE '2026-05-10', DATE '2026-05-24', 1, 'EXPIRED');
INSERT INTO RESERVATION VALUES (8007, 1007, 4016, DATE '2026-08-29', DATE '2026-09-12', 2, 'WAITING');
INSERT INTO RESERVATION VALUES (8008, 1010, 4019, DATE '2026-08-30', DATE '2026-09-13', 1, 'WAITING');

-- FINE
INSERT INTO FINE VALUES (9001, 7002, 1001, DATE '2026-08-27', 'LATE RETURN', 90, 0, 'UNPAID', NULL);
INSERT INTO FINE VALUES (9002, 7004, 1010, DATE '2026-08-16', 'LATE RETURN', 250, 100, 'PARTIAL', DATE '2026-08-25');
INSERT INTO FINE VALUES (9003, 7007, 1007, DATE '2026-07-05', 'LATE RETURN', 30, 30, 'PAID', DATE '2026-07-05');
INSERT INTO FINE VALUES (9004, 7010, 1013, DATE '2026-05-30', 'LATE RETURN', 70, 70, 'PAID', DATE '2026-05-31');
INSERT INTO FINE VALUES (9005, 7011, 1006, DATE '2026-05-04', 'LATE RETURN', 60, 0, 'WAIVED', NULL);
INSERT INTO FINE VALUES (9006, 7013, 1008, DATE '2026-02-22', 'LATE RETURN', 70, 70, 'PAID', DATE '2026-02-25');
INSERT INTO FINE VALUES (9007, 7015, 1014, DATE '2026-01-03', 'LATE RETURN', 100, 40, 'PARTIAL', DATE '2026-01-10');
INSERT INTO FINE VALUES (9008, 7016, 1012, DATE '2026-06-20', 'LOST BOOK', 480, 0, 'UNPAID', NULL);

COMMIT;

-- ============================================================
-- END OF LIBRARY.SQL
-- ============================================================
