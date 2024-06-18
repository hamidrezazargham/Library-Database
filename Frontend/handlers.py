from funcs import *


def lost(name: str) -> str:
    response = markdown_parse(f"It seems you're lost {name}.")
    return response


def start(name: str) -> str:
    response = markdown_parse(f"Hi {name}.\nAre you a member or an employee?")
    return response

def Member_profile(first_name: str = "", last_name: str = "", email: str = "", phone: str = "", address: str = ""):
    response = bold_text("Member\n")
    response += markdown_parse(f"First name: {first_name}\n")
    response += markdown_parse(f"Last name: {last_name}\n")
    response += markdown_parse(f"Email: {email}\n")
    response += markdown_parse(f"Phone number: {phone}\n")
    response += markdown_parse(f"Address: {address}\n")
    return response

def Employee_profile(first_name: str = "", last_name: str = "", email: str = "", phone: str = "", role: str = ""):
    response = bold_text("Employee\n")
    response += markdown_parse(f"First name: {first_name}\n")
    response += markdown_parse(f"Last name: {last_name}\n")
    response += markdown_parse(f"Email: {email}\n")
    response += markdown_parse(f"Phone number: {phone}\n")
    response += markdown_parse(f"Role: {role}\n")
    return response

def Author_profile(first_name: str = "", last_name: str = "", email: str = "", phone: str = ""):
    response = bold_text("Author\n")
    response += markdown_parse(f"First name: {first_name}\n")
    response += markdown_parse(f"Last name: {last_name}\n")
    response += markdown_parse(f"Email: {email}\n")
    response += markdown_parse(f"Phone number: {phone}\n")
    return response

def Book_profile(title: str = "", author_id: str = "", pub_date: str = "", genre: str = "", copies: str = ""):
    response = bold_text("Book\n")
    response += markdown_parse(f"Title: {title}\n")
    response += markdown_parse(f"Author id: {author_id}\n")
    response += markdown_parse(f"Published year: {pub_date}\n")
    response += markdown_parse(f"Genre: {genre}\n")
    response += markdown_parse(f"Available copies: {copies}\n")
    return response
    
def Enter_first_name() -> str:
    response = markdown_parse("Enter your first name")
    return response

def Enter_last_name() -> str:
    response = markdown_parse("Enter your last name")
    return response

def Enter_email() -> str:
    response = markdown_parse("Enter your email")
    return response

def Enter_phone() -> str:
    response = markdown_parse("Enter your phone number")
    return response

def Enter_address() -> str:
    response = markdown_parse("Enter your address")
    return response

def Enter_role() -> str:
    response = markdown_parse("Enter your role")
    return response

def account_created() -> str:
    response = markdown_parse("Account created.\nHere is your profile:\n\n")
    return response

def Enter_author_id() -> str:
    response = markdown_parse("Enter author's id")
    return response

def Enter_author_first_name() -> str:
    response = markdown_parse("Enter author's first name")
    return response

def Enter_author_last_name() -> str:
    response = markdown_parse("Enter author's last name")
    return response

def Enter_author_email() -> str:
    response = markdown_parse("Enter author's email")
    return response

def Enter_author_phone() -> str:
    response = markdown_parse("Enter author's phone number")
    return response

def author_added() -> str:
    response = markdown_parse("Author added.")
    return response

def Enter_book_id() -> str:
    response = markdown_parse("Enter book's id")
    return response

def Enter_book_title() -> str:
    response = markdown_parse("Enter book's title")
    return response

def Enter_book_author_id() -> str:
    response = markdown_parse("Enter book's author id")
    return response

def Enter_book_pub_date() -> str:
    response = markdown_parse("Enter book's published year")
    return response

def Enter_book_genre() -> str:
    response = markdown_parse("Enter book's genre")
    return response

def Enter_book_copies() -> str:
    response = markdown_parse("Enter number of copies to add")
    return response

def book_added() -> str:
    response = markdown_parse("Book added.")
    return response

def members_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        print(i, data['changed_date'][i])
        if data['operation'][i] == "INSERT":
            response += markdown_parse(f"- New ")
            response += Member_profile(
                first_name=data['new_datas'][i]['first_name'],
                last_name=data['new_datas'][i]['last_name'],
                email=data['new_datas'][i]['email'],
                phone=data['new_datas'][i]['phone_number'],
                address=data['new_datas'][i]['address']
            ).replace("\n", "\n    ")
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
            
            
        else:
            response += markdown_parse(f"- {data['old_datas'][i]['first_name']} {data['new_datas'][i]['last_name']} changed their profile\n")
            response += markdown_parse(changes(data['old_datas'][i], data['new_datas'][i]))
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response

def employees_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        if data['operation'][i] == "INSERT":
            response += markdown_parse(f"- New ")
            response += Employee_profile(
                first_name=data['new_datas'][i]['first_name'],
                last_name=data['new_datas'][i]['last_name'],
                email=data['new_datas'][i]['email'],
                phone=data['new_datas'][i]['phone_number'],
                role=data['new_datas'][i]['role']
            ).replace("\n", "\n    ")
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
            
        else:
            response += markdown_parse(f"- {data['old_datas'][i]['first_name']} {data['new_datas'][i]['last_name']} changed their profile\n")
            response += markdown_parse(changes(data['old_datas'][i], data['new_datas'][i]))
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response

def authors_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        if data['operation'][i] == "INSERT":
            response += markdown_parse(f"- New ")
            response += Author_profile(
                first_name=data['new_datas'][i]['first_name'],
                last_name=data['new_datas'][i]['last_name'],
                email=data['new_datas'][i]['email'],
                phone=data['new_datas'][i]['phone_number']
            ).replace("\n", "\n    ")
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
            
        else:
            response += markdown_parse(f"- {data['old_datas'][i]['first_name']} {data['new_datas'][i]['last_name']} changed their profile\n")
            response += markdown_parse(changes(data['old_datas'][i], data['new_datas'][i]))
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response

def books_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        if data['operation'][i] == "INSERT":
            response += markdown_parse(f"- New ")
            response += Book_profile(
                title=data['new_datas'][i]['title'],
                author_id=data['new_datas'][i]['author_id'],
                pub_date=data['new_datas'][i]['published_year'],
                genre=data['new_datas'][i]['genre'],
                copies=data['new_datas'][i]['available_copies']
            ).replace("\n", "\n    ")
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
            
        else:
            response += markdown_parse(f"- {data['old_datas'][i]['title']} data has been changed\n")
            response += markdown_parse(changes(data['old_datas'][i], data['new_datas'][i]))
            response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response


def borrows_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        response += markdown_parse(f"- Member with id {data['new_datas'][i]['member_id']} borrowed a book with id {data['new_datas'][i]['book_id']}\n")
        response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response

def returns_changes(data: dict, head: int, tail: int) -> str:
    response = ""
    for i in range(head, tail):
        response += markdown_parse(f"- Member with id {data['new_datas'][i]['member_id']} returned a book with id {data['new_datas'][i]['book_id']}\n")
        response += bold_text(f"({passed_time(data['changed_date'][i])})\n\n")
    response += markdown_parse(f"\n[{head + 1} - {tail}] ({len(data['changed_date'])} logs found)")
    return response

def help_center() -> str:
    response = bold_text("View Profile - [e.g. /profile]\n")
    response += markdown_parse("Send /profile to see your profile\n\n")
    response += bold_text("Edit Profile - [e.g. /editprofile]\n")
    response += markdown_parse("Send /editprofile to edit your profile\n\n")
    response += bold_text("Add Book - [e.g. /addbook]\n")
    response += markdown_parse("Send /addbook to add a book or increase the copies amount of a book in your library. then fill the required details of the book\n\n")
    response += bold_text("Delete Book - [e.g. /delete 12 5 (book id, copies)]\n")
    response += markdown_parse("Send /delete with id of the book and the amount of copies you want to delete\n\n")
    response += bold_text("Borrow Book - [e.g. /borrow 1948 (book title)]\n")
    response += markdown_parse("send /borrow with title of the book you want to borrow\n\n")
    response += bold_text("Return Book - [e.g. /return 1948]\n")
    response += markdown_parse("Send /return with title of the book you want to return\n\n")
    response += bold_text("Add Author - [e.g. /addauthor]\n")
    response += markdown_parse("Send /addauthor to add an author then fill the required details of the author\n")
    response += bold_text("Members Log - [e.g. /memberslog]\n")
    response += markdown_parse("Send /memberslog to see members changes log\n")
    response += bold_text("Employees Log - [e.g. /employeeslog]\n")
    response += markdown_parse("Send /employeeslog to see employees changes log\n")
    response += bold_text("Authors Log - [e.g. /authorslog]\n")
    response += markdown_parse("Send /authorslog to see authors changes log\n")
    response += bold_text("Books Log - [e.g. /bookslog]\n")
    response += markdown_parse("Send /bookslog to see books changes log\n")
    response += bold_text("Borrows Log - [e.g. /borrowslog]\n")
    response += markdown_parse("Send /borrowslog to see borrows changes log\n")
    response += bold_text("Returns Log - [e.g. /returnslog]\n")
    response += markdown_parse("Send /returnslog to see returns changes log")
    return response