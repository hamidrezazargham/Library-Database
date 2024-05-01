COPY (SELECT * FROM Persons) TO 'E:\university\DB\Library_Database\tests\csv files\Persons.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM Members) TO 'E:\university\DB\Library_Database\tests\csv files\Members.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM Employees) TO 'E:\university\DB\Library_Database\tests\csv files\Employees.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM Authors) TO 'E:\university\DB\Library_Database\tests\csv files\Authors.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM Books) TO 'E:\university\DB\Library_Database\tests\csv files\Books.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM Borrowed_Books) TO 'E:\university\DB\Library_Database\tests\csv files\Borrowed_Books.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM low_books) TO 'E:\university\DB\Library_Database\tests\csv files\low_books.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM borrowers) TO 'E:\university\DB\Library_Database\tests\csv files\borrowers.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM top_genre) TO 'E:\university\DB\Library_Database\tests\csv files\top_genre.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM top_borrowers) TO 'E:\university\DB\Library_Database\tests\csv files\top_borrowers.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM avg_dur) TO 'E:\university\DB\Library_Database\tests\csv files\avg_dur.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM available_books) TO 'E:\university\DB\Library_Database\tests\csv files\available_books.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT * FROM categorize) TO 'E:\university\DB\Library_Database\tests\csv files\categorize.csv' DELIMITER ',' CSV HEADER;