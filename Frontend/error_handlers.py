from funcs import *


CONVERSATION_EXPIRED = "This session has been expired"

def restart() -> str:
    response = markdown_parse(f"You already started the bot!")
    return response

def something_went_wrong() -> str:
    response = markdown_parse("Somthing went wrong! Please try again.")
    return response

def start_again() -> str:
    response = markdown_parse("Somthing went wrong! Please /start again.")
    return response

def access_denied() -> str:
    response = markdown_parse("You can't do that!")
    return response

def book_not_found() -> str:
    response = markdown_parse("I couldn't find your book!")
    return response