from datetime import datetime

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


def changes(old_data: dict, new_data: dict) -> str:
    response = ""
    for key in old_data.keys():
        if old_data[key] != new_data[key]:
            response += f"    {key}: {old_data[key]} -> {new_data[key]}\n"
    return response

def passed_time(time: str) -> str:
    delta = datetime.now() - datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    if delta.days > 0:
        return f"{delta.days} {'day' if delta.days == 1 else 'days'} ago"
    hours = delta.seconds // (60 * 60)
    if hours > 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    minutes = delta.seconds // 60
    if minutes > 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    return f"{delta.seconds} {'second' if delta.seconds == 1 else 'seconds'} ago"