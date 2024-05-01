-- get late fee
SELECT get_late_fee('2024-01-02', '2024-01-19');


-- get amount of available copies of a book by book_id
SELECT available_numbers(10);


-- calculate the late fees for each overdue book.
SELECT * FROM books_late_fee();


-- calculate the late fees for each members borrowed book.
SELECT * FROM Members_Late_Fee('Jim Smith');


-- Get a list of books borrowed by a specific member (e.g., John Doe).
SELECT * FROM books_borrowed_by('John Doe');


-- Find members who borrowed a specific book (e.g., “The Great Gatsby”).
SELECT * FROM members_borrowed('The Great Gatsby');