from funcs import *
import utils
import emojies


def restart(name: str) -> str:
    response = markdown_parse(f"You already started the bot {name}.")
    return response