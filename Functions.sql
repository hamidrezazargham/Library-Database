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
	SELECT Books.Available_Copies FROM Books INTO numbers;
	RETURN numbers;
END;
$$;