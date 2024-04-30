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


-- Insert some records into Books table.
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


-- Get a list of books borrowed by a specific member (e.g., John Doe).
SELECT Name, Title, Author
FROM Members 
JOIN Borrowed_Books ON Borrowed_Books.Member_Id=Members.Member_id
JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
WHERE Name = 'Thomas_Partey';


-- Find members who borrowed a specific book (e.g., “The Great Gatsby”).
SELECT Title, Name, Borrow_Date, Return_Date
FROM Borrowed_Books 
JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
JOIN Members ON members.Member_id=Borrowed_Books.Member_Id
WHERE Title = 'The_Heart_Of_The_Matter';


-- Update the number of available copies of a book after it’s borrowed.
UPDATE Books
SET Available_Copies=Available_Copies - 1
WHERE Book_id=553;


-- Insert a new borrowing record.
INSERT INTO Borrowed_Books
VALUES (0100023, 005519, 100080, '20231102', DATEADD(DAY, 14, '20231102'));


-- a query to find all books that are currently borrowed and overdue 
-- (i.e., not returned within 14 days from the borrow date).
-- Display the book titles and the names of members who borrowed them.
SELECT Title AS Book_Title, Name AS Member_Name
FROM Borrowed_Books
JOIN Members ON Members.Member_id=Borrowed_Books.Member_Id
JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
WHERE DATEDIFF(DAY, Borrow_Date, Return_Date)>14;


-- Find the most popular genre in the library.
-- Display the genre with the highest total number of books borrowed.
SELECT TOP 1 Genre, Title, Genre, COUNT(*) AS Total_Borrow
FROM Books
JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
GROUP BY Genre, Title
ORDER BY total_borrow DESC;


-- Calculate the average duration a book is borrowed by members.
-- Display the book title, the average duration in days, and the number of times it has been borrowed.
SELECT title, COUNT(*) AS noOftimesborrowed,
AVG(DATEDIFF(DAY, Borrow_Date, Return_Date)) Average_Duration
FROM Borrowed_Books
JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
GROUP BY Title;


-- Add a new column named fine amount to the Borrowed Books table.
-- This column will store the fine amount for overdue books.
ALTER TABLE Borrowed_Books
ADD Fine_Amount INT DEFAULT 1000;


-- a query to calculate the total fines collected from all overdue books.
SELECT SUM(Fine_Amount) FROM Borrowed_Books AS Total_Fine
WHERE DATEDIFF(DAY, Borrow_Date, Return_Date)>14


-- Find the top 5 members who have borrowed the most books.
-- Display their names and the number of books they have borrowed.
SELECT TOP 5 Name, COUNT(Borrow_id) AS Total_Borrow 
FROM Borrowed_Books
JOIN Members ON Members.Member_id=Borrowed_Books.Member_Id
GROUP BY Name
ORDER BY Total_Borrow DESC;


-- Add a UNIQUE constraint to the book id and member id columns in the Borrowed Books table
-- to prevent a member from borrowing the same book more than once simultaneously.
ALTER TABLE Borrowed_Books
ADD CONSTRAINT Unique_Borrowed
UNIQUE(Book_id, Member_id);


-- a query to find the books that are currently available for borrowing 
-- (i.e., books with at least one available copy).
-- Display the book titles and the number of available copies.
SELECT Title, Available_Copies FROM Books 
WHERE Available_Copies>= 1;


-- Calculate the late fees for each overdue book.
-- Display the book title, the name of the member who borrowed it, the number of 
-- days it is overdue, and the calculated late fee.
CREATE PROCEDURE NO_13 AS(
	SELECT Title, Name, DATEDIFF(DAY,Borrow_Date, Return_Date)-14 AS Overdue_Days,
	CASE
	WHEN DATEDIFF(DAY, Borrow_Date, Return_Date)>14
	THEN 1000*(SELECT DATEDIFF(DAY, Borrow_Date, Return_Date)-14)

	WHEN DATEDIFF(day,borrow_date,return_date)<14
	THEN 0

	ELSE 0
	END AS Late_Fee
	FROM Books
	JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
	JOIN Members ON Members.Member_id=Borrowed_Books.Member_id
);


-- Calculate the average duration in months for which books are borrowed.
-- Display the book title and the average duration in months.
SELECT COUNT(Member_id) AS NO_of_Books_Borrowed,
CASE
WHEN COUNT(Member_id)<5
THEN 'OCCASIONAL BORROWERS'

WHEN COUNT(Member_id) BETWEEN 5 AND 10
THEN 'REGULAR BORROWERS'

WHEN COUNT(Member_id)>10
THEN 'FREQUENT BORROWER'

END AS BORROWED_BEHAVIOR
FROM Borrowed_Books
GROUP BY Member_Id;


-- a query that categorizes members based on their borrowing behavior.
SELECT Name, AVG(DATEDIFF(DAY, Borrow_Date, Return_Date)) AS Average_Return_Duration
FROM Members
JOIN Borrowed_Books ON Borrowed_Books.Member_Id=Members.Member_id
GROUP BY Name
HAVING AVG(DATEDIFF(DAY, Borrowed_Date, ISNULL(Return_Date, GETDATE())))<7



-- Remove a borrowing record when a book is returned.
DELETE FROM Borrowed_Books
WHERE Return_Date IS NOT NULL;