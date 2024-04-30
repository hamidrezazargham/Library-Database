-- Inserting data into Members table
INSERT INTO Members (Member_id, Address, Join_Date, First_Name, Last_Name, Email, Phone_Number) VALUES
(1, '123 Main St', '2024-01-01', 'John', 'Doe', 'john.doe@example.com', '1234567890'),
(2, '456 Maple Ave', '2024-01-02', 'Jane', 'Doe', 'jane.doe@example.com', '0987654321'),
(3, '789 Oak Dr', '2024-01-03', 'Jim', 'Smith', 'jim.smith@example.com', '2345678901'),
(4, '321 Pine Ln', '2024-01-04', 'Jill', 'Johnson', 'jill.johnson@example.com', '3456789012'),
(5, '654 Elm St', '2024-01-05', 'Jack', 'Jones', 'jack.jones@example.com', '4567890123'),
(6, '987 Willow Rd', '2024-01-06', 'Jenny', 'Davis', 'jenny.davis@example.com', '5678901234'),
(7, '147 Cedar Ct', '2024-01-07', 'Joe', 'Miller', 'joe.miller@example.com', '6789012345'),
(8, '258 Spruce Pl', '2024-01-08', 'Jess', 'Wilson', 'jess.wilson@example.com', '7890123456'),
(9, '369 Birch Pkwy', '2024-01-09', 'Jeff', 'Taylor', 'jeff.taylor@example.com', '8901234567'),
(10, '480 Redwood Blvd', '2024-01-10', 'Julie', 'Anderson', 'julie.anderson@example.com', '9012345678'),
(11, '591 Dogwood Ln', '2024-01-11', 'Jerry', 'Thomas', 'jerry.thomas@example.com', '0123456789'),
(12, '602 Holly Dr', '2024-01-12', 'Janet', 'Jackson', 'janet.jackson@example.com', '1234509876'),
(13, '713 Magnolia Ave', '2024-01-13', 'Jacob', 'White', 'jacob.white@example.com', '2345609871'),
(14, '824 Jasmine Rd', '2024-01-14', 'Jasmine', 'Harris', 'jasmine.harris@example.com', '3456709812'),
(15, '935 Ivy Ct', '2024-01-15', 'James', 'Martin', 'james.martin@example.com', '4567809123'),
(16, '046 Rose Pl', '2024-01-16', 'Joan', 'Thompson', 'joan.thompson@example.com', '5678091234'),
(17, '157 Tulip Pkwy', '2024-01-17', 'Jean', 'Garcia', 'jean.garcia@example.com', '6780912345'),
(18, '268 Daisy Blvd', '2024-01-18', 'Jill', 'Martinez', 'jill.martinez@example.com', '7809123456'),
(19, '379 Violet Ln', '2024-01-19', 'Judy', 'Robinson', 'judy.robinson@example.com', '8091234567'),
(20, '480 Sunflower Dr', '2024-01-20', 'June', 'Clark', 'june.clark@example.com', '0912345678');



-- Inserting data into Employees table
INSERT INTO Employees (Employee_id, Employee_Role, Hired_Date, First_Name, Last_Name, Email, Phone_Number) VALUES
(1, 'Librarian', '2024-01-01', 'John', 'Doe', 'john.doe@example.com', '1234567890'),
(2, 'Assistant Librarian', '2024-01-02', 'Jane', 'Doe', 'jane.doe@example.com', '0987654321'),
(3, 'Library Technician', '2024-01-03', 'Jim', 'Smith', 'jim.smith@example.com', '2345678901'),
(4, 'Library Clerk', '2024-01-04', 'Jill', 'Johnson', 'jill.johnson@example.com', '3456789012'),
(5, 'Cataloging Librarian', '2024-01-05', 'Jack', 'Jones', 'jack.jones@example.com', '4567890123'),
(6, 'Reference Librarian', '2024-01-06', 'Jenny', 'Davis', 'jenny.davis@example.com', '5678901234'),
(7, 'Children’s Librarian', '2024-01-07', 'Joe', 'Miller', 'joe.miller@example.com', '6789012345'),
(8, 'Circulation Librarian', '2024-01-08', 'Jess', 'Wilson', 'jess.wilson@example.com', '7890123456'),
(9, 'Acquisitions Librarian', '2024-01-09', 'Jeff', 'Taylor', 'jeff.taylor@example.com', '8901234567'),
(10, 'Archivist', '2024-01-10', 'Julie', 'Anderson', 'julie.anderson@example.com', '9012345678'),
(11, 'Digital Librarian', '2024-01-11', 'Jerry', 'Thomas', 'jerry.thomas@example.com', '0123456789'),
(12, 'Law Librarian', '2024-01-12', 'Janet', 'Jackson', 'janet.jackson@example.com', '1234509876'),
(13, 'Medical Librarian', '2024-01-13', 'Jacob', 'White', 'jacob.white@example.com', '2345609871'),
(14, 'Music Librarian', '2024-01-14', 'Jasmine', 'Harris', 'jasmine.harris@example.com', '3456709812'),
(15, 'Research Librarian', '2024-01-15', 'James', 'Martin', 'james.martin@example.com', '4567809123'),
(16, 'School Librarian', '2024-01-16', 'Joan', 'Thompson', 'joan.thompson@example.com', '5678091234'),
(17, 'Serials Librarian', '2024-01-17', 'Jean', 'Garcia', 'jean.garcia@example.com', '6780912345'),
(18, 'Special Collections Librarian', '2024-01-18', 'Jill', 'Martinez', 'jill.martinez@example.com', '7809123456'),
(19, 'Systems Librarian', '2024-01-19', 'Judy', 'Robinson', 'judy.robinson@example.com', '8091234567'),
(20, 'Technical Services Librarian', '2024-01-20', 'June', 'Clark', 'june.clark@example.com', '0912345678');



-- Inserting data into Authors table
INSERT INTO Authors (Author_id, First_Name, Last_Name, Email, Phone_Number) VALUES
(1, 'George', 'Orwell', 'george.orwell@example.com', '1234567890'),
(2, 'Harper', 'Lee', 'harper.lee@example.com', '0987654321'),
(3, 'J.K.', 'Rowling', 'jk.rowling@example.com', '2345678901'),
(4, 'J.R.R.', 'Tolkien', 'jrr.tolkien@example.com', '3456789012'),
(5, 'F. Scott', 'Fitzgerald', 'f.scott.fitzgerald@example.com', '4567890123'),
(6, 'Ernest', 'Hemingway', 'ernest.hemingway@example.com', '5678901234'),
(7, 'Mark', 'Twain', 'mark.twain@example.com', '6789012345'),
(8, 'Charles', 'Dickens', 'charles.dickens@example.com', '7890123456'),
(9, 'Jane', 'Austen', 'jane.austen@example.com', '8901234567'),
(10, 'Leo', 'Tolstoy', 'leo.tolstoy@example.com', '9012345678'),
(11, 'Emily', 'Bronte', 'emily.bronte@example.com', '0123456789'),
(12, 'Virginia', 'Woolf', 'virginia.woolf@example.com', '1234509876'),
(13, 'Oscar', 'Wilde', 'oscar.wilde@example.com', '2345609871'),
(14, 'Agatha', 'Christie', 'agatha.christie@example.com', '3456709812'),
(15, 'Arthur', 'Conan Doyle', 'arthur.conan.doyle@example.com', '4567809123'),
(16, 'Stephen', 'King', 'stephen.king@example.com', '5678091234'),
(17, 'J.D.', 'Salinger', 'jd.salinger@example.com', '6780912345'),
(18, 'Haruki', 'Murakami', 'haruki.murakami@example.com', '7809123456'),
(19, 'Gabriel', 'Garcia Marquez', 'gabriel.garcia.marquez@example.com', '8091234567'),
(20, 'Franz', 'Kafka', 'franz.kafka@example.com', '0912345678');



-- Inserting data into Books table
INSERT INTO Books (Book_id, Title, Author_id, Published_Year, Genre, Available_Copies) VALUES
(1, '1984', 1, 1949, 'Dystopian', 10),
(2, 'To Kill a Mockingbird', 2, 1960, 'Southern Gothic', 15),
(3, 'Harry Potter and the Philosopher''s Stone', 3, 1997, 'Fantasy', 20),
(4, 'The Hobbit', 4, 1937, 'Fantasy', 25),
(5, 'The Great Gatsby', 5, 1925, 'Novel', 10),
(6, 'The Old Man and the Sea', 6, 1952, 'Novel', 15),
(7, 'Adventures of Huckleberry Finn', 7, 1884, 'Novel', 20),
(8, 'A Tale of Two Cities', 8, 1859, 'Historical Novel', 25),
(9, 'Pride and Prejudice', 9, 1813, 'Novel', 30),
(10, 'War and Peace', 10, 1869, 'Historical Novel', 35),
(11, 'Wuthering Heights', 11, 1847, 'Novel', 40),
(12, 'To the Lighthouse', 12, 1927, 'Novel', 45),
(13, 'The Picture of Dorian Gray', 13, 1890, 'Philosophical Novel', 50),
(14, 'And Then There Were None', 14, 1939, 'Mystery Novel', 55),
(15, 'The Hound of the Baskervilles', 15, 1902, 'Mystery Novel', 60),
(16, 'The Shining', 16, 1977, 'Horror Novel', 65),
(17, 'The Catcher in the Rye', 17, 1951, 'Novel', 70),
(18, 'Norwegian Wood', 18, 1987, 'Novel', 75),
(19, 'One Hundred Years of Solitude', 19, 1967, 'Magic Realism', 80),
(20, 'The Metamorphosis', 20, 1915, 'Novella', 85);