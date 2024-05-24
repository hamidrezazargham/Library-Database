import data
from datetime import datetime
import numpy as np



def markdown_parse(text) -> str:
    text = str(text)
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, fr"\{char}")
    return text


def bold_text(text: str, parse: bool = True) -> str:
    if parse:
        return f"*{markdown_parse(text)}*"
    return f"*{text}*"


def inline_link(text: str, url: str, parse: bool = True) -> str:
    if parse:
        return f"[{markdown_parse(text)}]({url})"
    return f"[{text}]({url})"


def italic_text(text: str, parse: bool = True) -> str:
    if parse:
        return f"_{markdown_parse(text)}_"
    return f"_{text}_"


def underline(text: str, parse: bool = True) -> str:
    if parse:
        return f"__{markdown_parse(text)}__"
    return f"__{text}__"


def strikethrough(text: str, parse: bool = True) -> str:
    if parse:
        return f"~{markdown_parse(text)}~"
    return f"~{text}~"


def spoiler_text(text: str, parse: bool = True) -> str:
    if parse:
        return f"||{markdown_parse(text)}||"
    return f"||{text}||"


def telegram_link(chat_id: str):
    return f"t.me/{chat_id}"


def none_handler(inp) -> str:
    return str(inp).replace("None", " _ ").replace("nan", " _ ")

def is_none(inp) -> bool:
    inp = str(inp)
    return (("None" in inp) or ("nan" in inp))