DROP VIEW IF EXISTS low_books, borrowers;


-- a view to get books with available copies lower than 5.
-- Display the book title, author, published year, genre and available copies.
CREATE VIEW low_books AS 
SELECT Title, Author, Published_Year, Genre, Available_Copies
FROM Books WHERE Available_Copies<5;


-- a view to get borrowed book and the borrowers.
-- Display the borrowed book title, borrower's name, email, borrow date and return date.
CREATE VIEW borrowers AS
SELECT Title, Name, Email, Borrow_Date, Return_Date
FROM Books
JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
JOIN Members ON Members.Member_id=Borrowed_Books.Member_id;