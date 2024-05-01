-- Persons table
SELECT * FROM Persons;


-- Members table
SELECT * FROM Members;


-- Employees table
SELECT * FROM Employees;


-- Authors table
SELECT * FROM Authors;


-- Books table
SELECT * FROM Books;


-- Borrowed_Books table
SELECT * FROM Borrowed_Books;


-- get books with available copies lower than 5.
SELECT * FROM low_books;


-- a view to get borrowed book and the borrowers.
SELECT * FROM borrowers;


-- Find the most popular genre in the library.
SELECT * FROM top_genre;


-- Find the top 5 members who have borrowed the most books.
SELECT * FROM top_borrowers;


-- average duration a book is borrowed by members.
SELECT * FROM avg_dur;


-- Find the books that are currently available for borrowing 
-- (i.e., books with at least one available copy).
SELECT * FROM available_books;


-- Categorize members by their behavior
SELECT * FROM categorize;