DROP FUNCTION IF EXISTS get_late_fee, available_numbers, decrease, increase;


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
	SELECT Books.Available_Copies INTO numbers;
	RETURN numbers;
END;
$$;


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


-- a function to increase the available_copies value when a book is returned
CREATE FUNCTION increase()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE Books
	SET Available_Copies=Available_Copies+1
	WHERE Book_id=NEW.Book_Id;
	RETURN NEW;
END;
$$;