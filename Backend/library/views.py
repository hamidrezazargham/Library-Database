from django.http import JsonResponse
from django.db import connection
import logging

def add_member(request):
    if request.method == "POST":
        try:
            # Extract member data from the request
            body = request.POST
            member_id = body.get("Member_id")
            address = body.get("Address")
            join_date = body.get("Join_Date")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Insert member data into the "Members" table
            with connection.cursor() as cur:
                query = f"SELECT Member_id FROM Members WHERE Member_id = {member_id};"
                cur.execute(query)
                existing_member = cur.fetchone()
                
                if existing_member:
                    query = f"""
                        UPDATE Members
                        SET Address='{address}', First_Name='{first_name}', Last_Name='{last_name}', Email='{email}', Phone_Number='{phone_number}'
                        WHERE Member_id = {member_id};
                    """
                    cur.execute(query)
                
                else:
                    query = f"""
                        INSERT INTO Members (Member_id, Address, Join_Date, First_Name, Last_Name, Email, Phone_Number)
                        VALUES ({member_id}, '{address}', '{join_date}', '{first_name}', '{last_name}', '{email}', '{phone_number}');
                    """
                    cur.execute(query)
                

            return JsonResponse({"message": "Member added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding member: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    


def add_employee(request):
    if request.method == "POST":
        try:
            # Extract employee data from the request
            body = request.POST
            employee_id = body.get("Employee_id")
            employee_role = body.get("Employee_Role")
            hired_date = body.get("Hired_Date")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Insert employee data into the "Employees" table
            with connection.cursor() as cur:
                query = f"SELECT Employee_id FROM Employees WHERE Employee_id = {employee_id};"
                cur.execute(query)
                existing_member = cur.fetchone()
                
                if existing_member:
                    query = f"""
                        UPDATE Employees
                        SET Employee_Role='{employee_role}', First_Name='{first_name}', Last_Name='{last_name}', Email='{email}', Phone_Number='{phone_number}'
                        WHERE Employee_id = {employee_id};
                    """
                    cur.execute(query)
                
                else:
                    query = f"""
                        INSERT INTO Employees (Employee_id, Employee_Role, Hired_Date, First_Name, Last_Name, Email, Phone_Number)
                        VALUES ({employee_id}, '{employee_role}', '{hired_date}', '{first_name}', '{last_name}', '{email}', '{phone_number}');
                    """
                    cur.execute(query)

            return JsonResponse({"message": "Employee added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding employee: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    

def add_author(request):
    if request.method == "POST":
        try:
            # Extract author data from the request
            body = request.POST
            author_id = body.get("Author_id")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Insert author data into the "Authors" table
            with connection.cursor() as cur:
                query = f"""
                    INSERT INTO Authors (Author_id, First_Name, Last_Name, Email, Phone_Number)
                    VALUES ({author_id}, '{first_name}', '{last_name}', '{email}', '{phone_number}');
                """
                cur.execute(query)


            return JsonResponse({"message": "Author added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding author: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)



def add_book(request):
    if request.method == "POST":
        try:
            # Extract book data from the request
            body = request.POST
            book_id = body.get("Book_id")
            title = body.get("Title")
            author_id = body.get("Author_id")
            published_year = body.get("Published_Year")
            genre = body.get("Genre")
            copies = body.get("Copies")

            # Check if the book already exists
            with connection.cursor() as cur:
                query = f"SELECT Available_Copies FROM Books WHERE Book_id = {book_id};"
                cur.execute(query)
                existing_copies = cur.fetchone()

                if existing_copies:
                    # Book exists, increment Available_Copies
                    query = f"UPDATE Books SET Available_Copies = Available_Copies + {copies} WHERE Book_id = {book_id};"
                    cur.execute(query)
                else:
                    # Book doesn't exist, insert a new record
                    query = f"""
                        INSERT INTO Books (Book_id, Title, Author_id, Published_Year, Genre, Available_Copies)
                        VALUES ({book_id}, '{title}', {author_id}, '{published_year}', '{genre}', {copies});
                    """
                    cur.execute(query)

            return JsonResponse({"message": "Book added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding book: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)


def search_book(request, title):
    with connection.cursor() as cur:
        query = f"SELECT Available_Copies, Book_id FROM Books WHERE Title = '{title}';"
        cur.execute(query)
        book = cur.fetchone()
    if book:
        return JsonResponse({"Book_id": book[1], "Copies": book[0]}, status=200)
    else:
        return JsonResponse({"message": "Book not found!"}, status=500)


def borrow(request):
    if request.method == "POST":
        try:
            # Extract borrowed book data from the request
            body = request.POST
            book_id = body.get("Book_id")
            member_id = body.get("Member_id")
            borrow_date = body.get("Borrow_Date")

            # Call the Borrow procedure
            with connection.cursor() as cur:
                query = f"CALL Borrow({book_id}, {member_id}, '{borrow_date}');"
                cur.execute(query)

            return JsonResponse({"message": "Book borrowed successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error borrowing book: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)



def return_book(request):
    if request.method == "POST":
        try:
            # Extract data from the request
            body = request.POST
            book_id = body.get('Book_id')
            member_id = body.get('Member_id')
            return_date = body.get('Return_Date')  # This can be None if not provided

            # Call the Return_book procedure
            with connection.cursor() as cur:
                query = f"CALL Return_book({book_id}, {member_id}, '{return_date}');"
                cur.execute(query)
                

            return JsonResponse({'message': 'Book borrowed successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)
    


def delete_book(request):
    if request.method == "POST":
        try:
            # Extract book data from the request
            body = request.POST
            book_id = body.get("Book_id")
            copies = int(body.get("Copies"))

            # Check if the book already exists
            with connection.cursor() as cur:
                query = f"SELECT Available_Copies FROM Books WHERE Book_id = {book_id};"
                cur.execute(query)
                existing_copies = cur.fetchone()

                if existing_copies:
                    # Book exists, decrement Available_Copies
                    query = f"UPDATE Books SET Available_Copies = {max(existing_copies[0] - copies, 0)} WHERE Book_id = {book_id};"
                    cur.execute(query)
                else:
                    # Book doesn't exist
                    return JsonResponse({'error': 'Book not found'}, status=404)

            return JsonResponse({"message": "Book deleted successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error deleting book: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    

def get_users(request):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT member_id FROM Members;")
            rows = cur.fetchall()
            user_ids = [row[0] for row in rows]
            cur.execute("SELECT employee_id FROM Employees;")
            rows = cur.fetchall()
            user_ids += [row[0] for row in rows]
        res = {
            'users': user_ids
        }
        
        return JsonResponse(res, status=200)
    
    except Exception as e:
        # Something else went wrong
        return JsonResponse({'error': str(e)}, status=500)
    

def add_member_logs(member_id, first_name, last_name):
    try:

        # Call the member_log stored procedure
        #cur.callproc('Member_logs', (member_id, first_name, last_name))

        # Call the Member_logs procedure
        with connection.cursor() as cur:
                query = f"CALL Member_logs({member_id}, {first_name}, '{last_name}');"
                cur.execute(query)

        # Log the addition
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        logging.info(f"Member added: ID={member_id}, Name={first_name} {last_name}")

        return True  # Successfully logged

    except Exception as e:
        # Handle exceptions (e.g., connection errors)
        logging.error(f"Error logging member: {e}")
        return False



def add_employee_logs(employee_id, first_name, last_name):
    try:

        # Call the stored procedure 
        #cur.callproc('Employee_logs', (employee_id, first_name, last_name))

        # Call the Employee_logs procedure
        with connection.cursor() as cur:
                query = f"CALL Employee_logs({employee_id}, {first_name}, '{last_name}');"
                cur.execute(query)

        # Log the addition
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        logging.info(f"Employee added: ID={employee_id}, Name={first_name} {last_name}")

        return True  # Successfully logged

    except Exception as e:
        # Handle exceptions (e.g., connection errors)
        logging.error(f"Error logging employee: {e}")
        return False



def add_book_logs(book_id, title, genre):
    try:

        # Call the stored procedure for logging
        #cur.callproc('book_log', (book_id, title, genre))

        # Call the book_log procedure
        with connection.cursor() as cur:
                query = f"CALL book_log({book_id}, {title}, '{genre}');"
                cur.execute(query)

        # Log the addition
        logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
        logging.info(f"Book added: ID={book_id}, Title='{title}', Genre='{genre}'")

        return True  # Successfully logged

    except Exception as e:
        # Handle exceptions (e.g., connection errors)
        logging.error(f"Error logging member: {e}")
        return False
    


def add_author_logs(author_id, first_name, last_name):
    try:

        # Call the stored procedure for logging
        #cur.callproc('author_log', (author_id, first_name, last_name))

        # Call the author_log procedure
        with connection.cursor() as cur:
                query = f"CALL author_log({author_id}, {first_name}, '{last_name}');"
                cur.execute(query)

        # Log the addition
        logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
        logging.info(f"Author added: ID={author_id}, Name={first_name} {last_name}")


        return True  # Successfully logged

    except Exception as e:
        # Handle exceptions (e.g., connection errors)
        logging.error(f"Error logging member: {e}")
        return False



def delete_book_logs(book_id, title, genre):
    try:

        # Call the stored procedure for logging (assuming it exists)
        #cur.callproc('Delete_book_log', (book_id, title, genre))

        # Call the Delete_book_log procedure
        with connection.cursor() as cur:
                query = f"CALL Delete_book_log({book_id}, {title}, '{genre}');"
                cur.execute(query)

        # Log the deletion
        logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
        logging.info(f"Book deleted: ID={book_id}, Title='{title}', Genre='{genre}'")

        return True  # Successfully logged

    except Exception as e:
        print(f"Error: {e}")
        return False

