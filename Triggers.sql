DROP TRIGGER IF EXISTS borrow_trig ON Borrowed_Books;
DROP TRIGGER IF EXISTS return_trig ON Borrowed_Books;
DROP FUNCTION IF EXISTS decrease, increase;


-- a function to decrease the available_copies value when a book is borrowed
CREATE FUNCTION decrease()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE Books
	SET Available_Copies=Available_Copies-1
	WHERE Book_id=NEW.Book_Id;
	RETURN NEW;
END;
$$;

-- a trigger to decrease the amount of available copies of a book when it is borrowed.
CREATE TRIGGER borrow_trig
AFTER INSERT ON Borrowed_Books
FOR EACH ROW EXECUTE FUNCTION decrease();



-- a function to increase the available_copies value when a book is returned
CREATE FUNCTION increase()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
	IF NEW.Return_Date IS NOT NULL THEN
		UPDATE Books
		SET Available_Copies=Available_Copies+1
		WHERE Book_id=NEW.Book_Id;
	END IF;
	RETURN NEW;
END;
$$;


-- a trigger to increase the amount of available copies of a book when it is borrowed.
CREATE TRIGGER return_trig
AFTER INSERT ON Borrowed_Books
FOR EACH ROW EXECUTE FUNCTION increase();