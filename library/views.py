from django.shortcuts import render

# Create your views here.

import psycopg2
import json
from django.http import JsonResponse
from django.db import connection

def add_member(request):
    if request.method == "POST":
        try:
            # Extract member data from the request
            body = json.loads(request.body)
            member_id = body.get("Member_id")
            address = body.get("Address")
            join_date = body.get("Join_Date")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Connect to your PostgreSQL database
            # conn = psycopg2.connect(
            #     dbname="library",  
            #     user="13811381", 
            #     password="13811381", 
            #     host="localhost",  
            #     port=5432, 
            # )

            # Create a cursor
            # cur = conn.cursor()

            # Insert member data into the "Members" table
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO Members (Member_id, Address, Join_Date, First_Name, Last_Name, Email, Phone_Number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (member_id, address, join_date, first_name, last_name, email, phone_number))
                

            # Commit the transaction
            # conn.commit()

            # Close the cursor and connection
            # cur.close()
            # conn.close()

            return JsonResponse({"message": "Member added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding member: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    


def add_employee(request):
    if request.method == "POST":
        try:
            # Extract employee data from the request
            body = json.loads(request.body)
            employee_id = body.get("Employee_id")
            employee_role = body.get("Employee_Role")
            hired_date = body.get("Hired_Date")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Connect to your PostgreSQL database
            # conn = psycopg2.connect(
            #    dbname="library", 
            #    user="postgres", 
            #    password="13811381", 
            #   host="localhost",  
            #    port=5432, )
        

            # Create a cursor
            # cur = conn.cursor()

            # Insert employee data into the "Employees" table
            cur.execute("""
                INSERT INTO Employees (Employee_id, Employee_Role, Hired_Date, First_Name, Last_Name, Email, Phone_Number)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (employee_id, employee_role, hired_date, first_name, last_name, email, phone_number))

            # Commit the transaction
            #conn.commit()

            # Close the cursor and connection
            #cur.close()
            #conn.close()

            return JsonResponse({"message": "Employee added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding employee: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    

def add_author(request):
    if request.method == "POST":
        try:
            # Extract author data from the request
            body = json.loads(request.body)
            author_id = body.get("Author_id")
            first_name = body.get("First_Name")
            last_name = body.get("Last_Name")
            email = body.get("Email")
            phone_number = body.get("Phone_Number")

            # Connect to your PostgreSQL database
            # conn = psycopg2.connect(
            #     dbname="library",  
            #     user="13811381", 
            #     password="13811381", 
            #     host="localhost",  
            #     port=5432, 
            # )

            # Create a cursor
            # cur = conn.cursor()

            # Insert author data into the "Authors" table
            cur.execute("""
                INSERT INTO Authors (Author_id, First_Name, Last_Name, Email, Phone_Number)
                VALUES (%s, %s, %s, %s, %s);
            """, (author_id, first_name, last_name, email, phone_number))

            # Commit the transaction
            # conn.commit()

            # Close the cursor and connection
            # cur.close()
            # conn.close()

            return JsonResponse({"message": "Author added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding author: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)



def add_book(request):
    if request.method == "POST":
        try:
            # Extract book data from the request
            body = json.loads(request.body)
            book_id = body.get("Book_id")
            title = body.get("Title")
            author_id = body.get("Author_id")
            published_year = body.get("Published_Year")
            genre = body.get("Genre")

            # # Connect to your PostgreSQL database
            # conn = psycopg2.connect(
            #     dbname="library", 
            #     user="13811381", 
            #     password="13811381",  
            #     host="localhost", 
            #     port=5432,  
            # )

            # Create a cursor
            # cur = conn.cursor()

            # Check if the book already exists
            cur.execute("SELECT Available_Copies FROM Books WHERE Book_id = %s;", (book_id,))
            existing_copies = cur.fetchone()

            if existing_copies:
                # Book exists, increment Available_Copies
                cur.execute("UPDATE Books SET Available_Copies = Available_Copies + 1 WHERE Book_id = %s;", (book_id,))
            else:
                # Book doesn't exist, insert a new record
                cur.execute("""
                    INSERT INTO Books (Book_id, Title, Author_id, Published_Year, Genre, Available_Copies)
                    VALUES (%s, %s, %s, %s, %s, 1);
                """, (book_id, title, author_id, published_year, genre))

            # Commit the transaction
            # conn.commit()

            # Close the cursor and connection
            # cur.close()
            # conn.close()

            return JsonResponse({"message": "Book added successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error adding book: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)


def borrow(request):
    if request.method == "POST":
        try:
            # Extract borrowed book data from the request
            body = json.loads(request.body)
            borrow_id = body.get("Borrow_id")
            book_id = body.get("Book_id")
            member_id = body.get("Member_id")
            borrow_date = body.get("Borrow_Date")

            # Connect to your PostgreSQL database
            # conn = psycopg2.connect(
            #     dbname="library", 
            #     user="13811381", 
            #     password="13811381",  
            #     host="localhost",  
            #     port=5432, 
            # )

            # Create a cursor
            # cur = conn.cursor()

            # Call the Borrow procedure
            cur.callproc("Borrow", [book_id, member_id, borrow_date])

            # Commit the transaction
            # conn.commit()

            # Close the cursor and connection
            # cur.close()
            # conn.close()

            return JsonResponse({"message": "Book borrowed successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error borrowing book: {e}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)



def return_book(request):
    if request.method == "POST":
        try:
            # Extract data from the request
            body = json.loads(request.body)
            book_id = body.get('Book_id')
            member_id = body.get('Member_id')
            borrow_date = body.get('Borrow_Date')
            return_date = body.get('Return_Date')  # This can be None if not provided

            # Connect to the PostgreSQL database
            # conn = psycopg2.connect(dbname="library", user="13811381", password="13811381", host="localhost", port="5432")
            # cur = conn.cursor()

            # Call the Return_book procedure
            cur.callproc('Return_book', [book_id, member_id, borrow_date, return_date])

            # Commit the transaction
            # conn.commit()

            # Close the cursor and connection
            # cur.close()
            # conn.close()

            return JsonResponse({'message': 'Book borrowed successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)
    

def delete_book(request):
    try:
        # Parse the Book_id from the POST data
        book_id = request.POST.get('Book_id')

        # Fetch the book from the database
        book = Books.objects.get(Book_id=book_id)

        # Decrease the Available_Copies by 1
        book.Available_Copies -= 1
        book.save()

        # Return a success response
        return JsonResponse({'status': 'success'}, status=200)

    except Books.DoesNotExist:
        # The book does not exist
        return JsonResponse({'error': 'Book not found'}, status=404)

    except Exception as e:
        # Something else went wrong
        return JsonResponse({'error': str(e)}, status=500)
