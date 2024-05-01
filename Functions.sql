DROP FUNCTION IF EXISTS get_late_fee, available_numbers, Books_Late_Fee, Members_Late_Fee, books_borrowed_by, members_borrowed;


-- a function to calculate late fee
CREATE FUNCTION get_late_fee(DATE, DATE)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
	Late_Fee INT;
BEGIN
	SELECT
	CASE
	WHEN ($2 - $1)>14
	THEN 1000*(SELECT ($2 - $1)-14)
	ELSE 0
	END INTO Late_Fee;
	
	RETURN Late_Fee;
END;
$$;


-- a function to get available copies of a book
CREATE FUNCTION available_numbers(INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
	numbers INT;
BEGIN
	SELECT Books.Available_Copies FROM Books INTO numbers;
	RETURN numbers;
END;
$$;



-- Calculate the late fees for each overdue book.
-- Display the book title, the name and contact information of the member who borrowed it, the number of 
-- days it is overdue, and the calculated late fee.
CREATE FUNCTION Books_Late_Fee()
RETURNS TABLE(
	Title VARCHAR, 
	Member TEXT, 
	Email VARCHAR, 
	Phone_Number VARCHAR, 
	Overdue_Days INT,
	Late_Fee INT
)
LANGUAGE plpgsql 
AS $$
BEGIN
	RETURN QUERY
	(
		SELECT Books.Title, Members.First_Name || ' ' || Members.Last_Name, Members.Email, Members.Phone_Number, (Return_Date - Borrow_Date)-14 AS Overdue_Days,
		get_late_fee(Borrow_Date, Return_Date)
		FROM Books
		JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
		JOIN Members ON Members.Member_id=Borrowed_Books.Member_id
	);
END;
$$;



-- Calculate the late fees for each members borrowed book.
-- Display the member name, the title of the borrowed book, the number of 
-- days it is overdue, and the calculated late fee.
CREATE FUNCTION Members_Late_Fee(VARCHAR)
RETURNS TABLE (
	Member TEXT,
	Email VARCHAR,
	Phone_Number VARCHAR,
	Title VARCHAR,
	Borrow_Date DATE,
	Return_Date DATE,
	Overdue_Days INT,
	Late_Fee INT
)
LANGUAGE plpgsql 
AS $$
BEGIN
	RETURN QUERY
	(
		SELECT Members.First_Name || ' ' || Members.Last_Name AS Member, Members.Email, Members.Phone_Number, Books.Title, 
		Borrowed_Books.Borrow_Date, Borrowed_Books.Return_Date, (Borrowed_Books.Return_Date - Borrowed_Books.Borrow_Date)-14 AS Overdue_Days,
		get_late_fee(Borrowed_Books.Borrow_Date, Borrowed_Books.Return_Date) AS Late_Fee
		FROM Books
		JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
		JOIN Members ON Members.Member_id=Borrowed_Books.Member_id
		WHERE Member=$1
	);
END;
$$;



-- Get a list of books borrowed by a specific member (e.g., John Doe).
-- display the member name and contact information, borrowed books titles, borrow dates and return dates.
CREATE Function books_borrowed_by(VARCHAR)
RETURNS TABLE (
	Member TEXT,
	Email VARCHAR,
	Phone_Number VARCHAR,
	Title VARCHAR,
	Borrow_Date DATE,
	Return_Date DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	(
		SELECT First_Name || ' ' || Last_Name AS Member, Members.Email, Members.Phone_Number, Books.Title,
		Borrowed_Books.Borrow_Date, Borrowed_Books.Return_Date
		FROM Members 
		JOIN Borrowed_Books ON Borrowed_Books.Member_Id=Members.Member_id
		JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
		WHERE Member=$1
	);
END;
$$;



-- Find members who borrowed a specific book (e.g., “The Great Gatsby”).
-- display borrower's name and contact information, borrowed book's title, borrow date and return date.
CREATE FUNCTION members_borrowed(VARCHAR)
RETURNS TABLE (
	Title VARCHAR,
	Member TEXT,
	Email VARCHAR,
	Phone_Number VARCHAR,
	Borrow_Date DATE,
	Return_Date DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	(
		SELECT Books.Title, First_Name || ' ' || Last_Name AS Member, Members.Email, Members.Phone_Number, 
		Borrowed_Books.Borrow_Date, Borrowed_Books.Return_Date
		FROM Borrowed_Books 
		JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
		JOIN Members ON members.Member_id=Borrowed_Books.Member_Id
		WHERE Books.Title=$1
	);
END;
$$;