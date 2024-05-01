DROP TABLE IF EXISTS Borrowed_Books;
DROP TABLE IF EXISTS Books, Members, Authors, Employees, Persons;



-- Persons table
CREATE TABLE Persons (
	First_Name VARCHAR(50) NOT NULL,
	Last_Name VARCHAR(50) NOT NULL,
	Email VARCHAR(100) UNIQUE,
	Phone_Number VARCHAR UNIQUE
);



-- Members Table
CREATE TABLE Members (
	Member_id INT PRIMARY KEY,
	Address TEXT,
	Join_Date DATE
) INHERITS (Persons);



-- Employees Table
CREATE TABLE Employees (
	Employee_id INT PRIMARY KEY,
	Employee_Role VARCHAR,
	Hired_Date DATE
) INHERITS (Persons);



-- Author Table
CREATE TABLE Authors (
	Author_id INT PRIMARY KEY
) INHERITS (Persons);



-- Books Table
CREATE TABLE Books (
	Book_id INT PRIMARY KEY,
	Title VARCHAR(255) NOT NULL,
	Author_Id INT NOT NULL,
	Published_Year INT,
	Genre VARCHAR(50),
	Available_Copies INT,
	FOREIGN KEY (Author_id) REFERENCES Authors(Author_id)
);



-- Borrowed books Table
CREATE TABLE Borrowed_Books (
	Borrow_id SERIAL PRIMARY KEY,
	Book_Id INT NOT NULL,
	Member_Id INT NOT NULL,
	Borrow_Date DATE NOT NULL,
	Return_Date DATE,
	FOREIGN KEY (Book_Id) REFERENCES Books(Book_Id),
	FOREIGN KEY (Member_Id) REFERENCES Members(Member_Id)
);



-- Add a UNIQUE constraint to the book id and member id columns in the Borrowed Books table
-- to prevent a member from borrowing the same book more than once simultaneously.
ALTER TABLE Borrowed_Books
ADD CONSTRAINT Unique_Borrowed
UNIQUE(Book_id, Member_id);
