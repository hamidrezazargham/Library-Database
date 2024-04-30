DROP TABLE IF EXISTS Borrowed_Books;
DROP TABLE IF EXISTS Books, Members;


-- Books Table
CREATE TABLE Books (
	Book_id INT PRIMARY KEY,
	Title VARCHAR(255) NOT NULL,
	Author VARCHAR(255) NOT NULL,
	Published_Year INT,
	Genre VARCHAR(50),
	Available_Copies INT
);


-- Members Table
CREATE TABLE Members (
	Member_id INT PRIMARY KEY,
	Name VARCHAR(100) NOT NULL,
	Email VARCHAR(100) UNIQUE,
	Phone_Number VARCHAR,
	Address TEXT,
	Join_Date DATE
);


-- Borrowed books Table
CREATE TABLE Borrowed_Books (
	Borrow_id INT PRIMARY KEY,
	Book_Id INT,
	Member_Id INT,
	Borrow_Date DATE,
	Return_Date DATE,
	FOREIGN KEY (Book_Id) REFERENCES Books(Book_Id),
	FOREIGN KEY (Member_Id) REFERENCES Members(Member_Id)
);


-- Insert some records into each table.
INSERT INTO Books (Book_Id, Title, Author, Published_Year, Genre, Available_Copies) 
VALUES (00551, 'The_Great_Gatsby', 'F_Scott_Fitzgerald', '19250410', 'Tragedy', '1'),
	(00552, 'ULYSSES', 'James_Joyce', '19220202', 'Modernist_Novel', '1'),
	(00553, 'Lolita', 'Vladimir_Nabokov', '19552001', 'Novel', '1'),
	(00554, 'Brave_New_World', 'Aldous_Huxley', '19320505', 'Science_Fiction_Dystopian_Fiction', '1'),
	(00555, 'The_Sound_And_The_Fury', 'William_Faulkner', '19290103', 'Southern_Gothic', '1'),
	(00556, 'Catch22', 'Joseph_Heller', '19611010', 'Dark_Comedy', '1'),
	(00557, 'The_Grapes_Of_Wrath', 'John_Steinbeck', '19391404', 'Novel', '1'),
	(00558, 'I_Claudius', 'Robert_Graves', '19340810', 'Historical', '1'),
	(00559, 'To_The_Lighthouse', 'Virginia_Woolf', '19270505', 'Modernism', '1'),
	(05510, 'Slaughterhouse_Five', 'Kurt_Vonnegut', '19693103', 'War_Novel', '1'),
	(05511, 'Invisible_Man', 'Ralph_Ellison', '19521404', 'African_American_Literature', '1'),
	(05512, 'Native_Son', 'Richard_Wright', '19400103', 'Social_Protest', '1'),
	(05513, 'USA_Trilogy', 'John_Dos_Passos', '19300405', 'Political_Fiction', '1'),
	(05514, 'A_Passage_To_India', 'E_M_Forster', '19240406', 'Novel', '1'),
	(05515, 'Tender_Is_The_Night', 'F_Scott_Fitzgerald', '19341204', 'Tragedy', '1'),
	(05516, 'Animal_Farm', 'George_Orwell', '19451708', 'Political_Satire', '1'),
	(05517, 'The_Golden_Bowl', 'Henry_James', '19041011', 'Philosophy', '1'),
	(05518, 'A_Handful_Of_Dust', 'Evelyn_Waugh', '19340603', 'Fiction', '1'),
	(05519, 'As_I_Lay_Dying', 'William_Faulkner', '19300302', 'Black_Comedy', '1'),
	(05520, 'The_Heart_Of_The_Matter', 'Graham_Greene', '19480302', 'Nove', '1');
	
INSERT INTO Members (Member_id, Name, Email, Join_Date) 
VALUES (1, 'John Doe', 'john.doe@example.com', '2024-01-01'),
	(2, 'Jane Smith', 'jane.smith@example.com', '2024-01-02'),
	(3, 'Robert Johnson', 'robert.johnson@example.com', '2024-01-03'),
	(4, 'Michael Williams', 'michael.williams@example.com', '2024-01-04'),
	(5, 'Sarah Brown', 'sarah.brown@example.com', '2024-01-05'),
	(6, 'Jessica Davis', 'jessica.davis@example.com', '2024-01-06'),
	(7, 'Thomas Miller', 'thomas.miller@example.com', '2024-01-07'),
	(8, 'Susan Wilson', 'susan.wilson@example.com', '2024-01-08'),
	(9, 'James Moore', 'james.moore@example.com', '2024-01-09'),
	(10, 'Patricia Taylor', 'patricia.taylor@example.com', '2024-01-10'),
	(11, 'Richard Anderson', 'richard.anderson@example.com', '2024-01-11'),
	(12, 'Linda Thomas', 'linda.thomas@example.com', '2024-01-12'),
	(13, 'Charles Jackson', 'charles.jackson@example.com', '2024-01-13'),
	(14, 'Elizabeth White', 'elizabeth.white@example.com', '2024-01-14'),
	(15, 'Christopher Harris', 'christopher.harris@example.com', '2024-01-15'),
	(16, 'Jennifer Martin', 'jennifer.martin@example.com', '2024-01-16'),
	(17, 'Joseph Thompson', 'joseph.thompson@example.com', '2024-01-17'),
	(18, 'Margaret Garcia', 'margaret.garcia@example.com', '2024-01-18'),
	(19, 'William Martinez', 'william.martinez@example.com', '2024-01-19'),
	(20, 'Mary Robinson', 'mary.robinson@example.com', '2024-01-20');

	
	
-- Add a new column named fine amount to the Borrowed Books table.
-- This column will store the fine amount for overdue books.
ALTER TABLE Borrowed_Books
ADD Fine_Amount INT DEFAULT 1000;


-- Add a UNIQUE constraint to the book id and member id columns in the Borrowed Books table
-- to prevent a member from borrowing the same book more than once simultaneously.
ALTER TABLE Borrowed_Books
ADD CONSTRAINT Unique_Borrowed
UNIQUE(Book_id, Member_id);
