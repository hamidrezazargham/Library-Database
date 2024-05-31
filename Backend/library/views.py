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
                query = f"""
                    INSERT INTO Employees (Employee_id, Employee_Role, Hired_Date, First_Name, Last_Name, Email, Phone_Number)
                    VALUES ({employee_id}, '{employee_role}', '{hired_date}', '{first_name}', '{last_name}', '{email}', '{phone_number}');
                """
                cur.execute(query)

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
            # borrow_id = body.get("Borrow_id")
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
            # borrow_date = body.get('Borrow_Date')
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