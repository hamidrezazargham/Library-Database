DROP PROCEDURE IF EXISTS Borrow, Return_book;


-- a procedure to insert a record into Borrowed_Books When a book is borrowed
CREATE PROCEDURE Borrow(INT, INT, DATE)
LANGUAGE plpgsql
AS $$
BEGIN
	IF available_numbers($1)>0 THEN
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