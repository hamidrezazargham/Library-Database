DROP PROCEDURE IF EXISTS Borrow, Return_book, Books_Late_Fee, Members_Late_Fee, books_borrowed_by, members_borrowed;


-- a procedure to insert a record into Borrowed_Books When a book is borrowed
CREATE PROCEDURE Borrow(INT, INT, DATE)
LANGUAGE plpgsql
AS $$
BEGIN
	IF available_numbers(Book_id)>0 THEN
	INSERT INTO Borrowed_Books(Book_Id, Member_Id, Borrow_Date)
	VALUES ($1, $2, $3);
	ELSE
	SELECT 'Book is not Available';
	END IF;
END;
$$;


-- a procedure to update the return date of a record in Borrowed_Books table When a book is returned
CREATE PROCEDURE Return_book(INT, INT, DATE)
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE Borrowed_Books
	SET Return_Date=$3
	WHERE Book_Id=$1 AND Member_Id=$2;
END;
$$;



-- Calculate the late fees for each overdue book.
-- Display the book title, the name of the member who borrowed it, the number of 
-- days it is overdue, and the calculated late fee.
CREATE PROCEDURE Books_Late_Fee()
LANGUAGE plpgsql 
AS $$
BEGIN
	SELECT Title, Name, (Return_Date - Borrow_Date)-14 AS Overdue_Days,
	get_late_fee(Borrow_Date, Return_Date) AS Late_Fee
	FROM Books
	JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
	JOIN Members ON Members.Member_id=Borrowed_Books.Member_id;
END;
$$;


-- Calculate the late fees for each members borrowed book.
-- Display the member name, the title of the borrowed book, the number of 
-- days it is overdue, and the calculated late fee.
CREATE PROCEDURE Members_Late_Fee(INT)
LANGUAGE plpgsql 
AS $$
BEGIN
	SELECT Name, Title, (Return_Date - Borrow_Date)-14 AS Overdue_Days,
	get_late_fee(Borrow_Date, Return_Date) AS Late_Fee
	FROM Books
	JOIN Borrowed_Books ON Borrowed_Books.Book_Id=Books.Book_id
	JOIN Members ON Members.Member_id=Borrowed_Books.Member_id
	WHERE Members.Member_id=$1;
END;
$$;


-- Get a list of books borrowed by a specific member (e.g., John Doe).
CREATE PROCEDURE books_borrowed_by(VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
	SELECT Name, Title, Author
	FROM Members 
	JOIN Borrowed_Books ON Borrowed_Books.Member_Id=Members.Member_id
	JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
	WHERE Name=$1;
END;
$$;


-- Find members who borrowed a specific book (e.g., “The Great Gatsby”).
CREATE PROCEDURE members_borrowed(VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
	SELECT Title, Name, Borrow_Date, Return_Date
	FROM Borrowed_Books 
	JOIN Books ON Books.Book_id=Borrowed_Books.Book_Id
	JOIN Members ON members.Member_id=Borrowed_Books.Member_Id
	WHERE Title=$1;
END;
$$;


