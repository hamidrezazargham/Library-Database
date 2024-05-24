from funcs import *
import emojies
import utils


def lost(name: str) -> str:
    response = markdown_parse(f"It seems you're lost {name}.")
    return response


def start(name: str) -> str:
    response = markdown_parse(f"Hi {name}.\nAre you a member or an employee?")
    return response

def Member_info(first_name: str = "", last_name: str = "", email: str = "", phone: str = "", address: str = ""):
    response = bold_text("Member\n\n")
    response += markdown_parse(f"First name: {first_name}\n")
    response += markdown_parse(f"Last name: {last_name}\n")
    response += markdown_parse(f"Email: {email}\n")
    response += markdown_parse(f"Phone number: {phone}\n")
    response += markdown_parse(f"Address: {address}\n")