-- Borrow a book (Book_id, Member_id, Borrow_Date)
CALL Borrow(2, 2, '2024-01-01');


-- Return a book (Book_id, Member_id, Borrow_Date)
CALL Return_book(2, 2, '2024-01-17');