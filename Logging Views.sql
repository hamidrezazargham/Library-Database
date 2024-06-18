DROP TABLE IF EXISTS members_changes, employees_changes, authors_changes,
 books_changes, borrowed_books_changes, returned_books_changes

-- View to display changes made on the current date
-- CREATE VIEW daily_changes AS
-- SELECT
--     audit_id,
--     table_name,
--     operation,
--     old_data,
--     new_data,
--     changed_by,
--     changed_at
-- FROM audit_table
-- WHERE changed_at::DATE = CURRENT_DATE;

-- View to display changes made to the Members table
CREATE VIEW members_changes AS
SELECT
    Member_id
    operation,
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Members', operation in ("INSERT", "UPDATE");

-- View to display changes made to the Employees table
CREATE VIEW employees_changes AS
SELECT
    Member_id
    operation,
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Employees', operation in ("INSERT", "UPDATE");

-- View to display changes made to the Authors table
CREATE VIEW authors_changes AS
SELECT
    Member_id
    operation,
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Authors', operation = "INSERT";

-- View to display changes made to the Books table
CREATE VIEW books_changes AS
SELECT
    operation,
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Books', operation in ("INSERT", "UPDATE");;

-- View to display changes made to the Borrowed_Books table
CREATE VIEW borrowed_books_changes AS
SELECT
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Borrowed_Books', operation = "INSERT";

-- View to display changes made to the returned_books table
CREATE VIEW returned_books_changes AS
SELECT
    old_data,
    new_data,
    changed_at
FROM audit_table
WHERE table_name = 'Borrowed_Books', operation = "UPDATE";
