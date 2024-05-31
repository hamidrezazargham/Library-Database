from funcs import *
import emojies
import utils


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


