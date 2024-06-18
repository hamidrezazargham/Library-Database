import logging
import traceback
import html
import json
from datetime import datetime

from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from handlers import *
import telegram_funcs as tf
import error_handlers
import data as Data
import stickers
import emojies
import db_scripts


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# start conversation states
SET_ROLE = 0
FIRST_NAME, LAST_NAME, EMAIL, PHONE, OTHER = range(1, 6)
SET_ID = 0
TITLE, AUTHOR_ID, PUB_DATE, GENRE, COPIES = range(1, 6)
LOAD_NEWS = "load_news"
NEWS_EXPIRED = "news_expired"
MEMBER = "Member"
EMPLOYEE = "Employee"

ACTIVE, EXPIRED = range(2)

LIST_LENGTH = 10
MEMBERS_LIST_LENGTH = 4


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    
    # update_str = update.to_dict() if isinstance(update, Update) else str(update)
    # action = json.dumps(update_str, indent=2, ensure_ascii=False)
    # message = (
    #     "An exception was raised while handling an update\n"
    #     f"<pre>update = {html.escape(action)}"
    #     "</pre>\n\n"
    #     f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    #     f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    #     f"<pre>{html.escape(tb_string)}</pre>"
    # )
    
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    
    response = error_handlers.something_went_wrong()
    await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['oops'])
        
    # Finally, send the message
    await context.bot.send_message(
        chat_id=Data.DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )
    

async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    user_ids = db_scripts.get_user_ids()
    
    if user.id in user_ids:
        logger.info("%s restarted a private chat with the bot", username)
        response = error_handlers.restart()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['not funny'])
        return ConversationHandler.END
    
        
    context.user_data['First_Name'] = user.first_name if user.first_name is not None else ""
    context.user_data['Last_Name'] = user.last_name if user.last_name is not None else ""
    logger.info("%s started a private chat with the bot", username)
    keyboard = [
        [InlineKeyboardButton(text=MEMBER, callback_data=MEMBER)],
        [InlineKeyboardButton(text=EMPLOYEE, callback_data=EMPLOYEE)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = start(user.first_name)

    await tf.send_message(update, response, reply_markup=reply_markup)
    return SET_ROLE


async def member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    context.user_data['role'] = MEMBER
    context.user_data['Member_id'] = user.id
    logger.info("%s set %s as their role", username, MEMBER)
    
    response = Enter_email()
    
    await query.edit_message_text(response, parse_mode="MarkdownV2")
    return EMAIL
    
    
async def employee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    context.user_data['role'] = EMPLOYEE
    context.user_data['Employee_id'] = user.id
    logger.info("%s set %s as their role", username, EMPLOYEE)
    
    response = Enter_email()
    
    await query.edit_message_text(response, parse_mode="MarkdownV2")
    return EMAIL


async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    logger.info("%s wants to edit their profile", username)
    
    response = Enter_first_name()
    
    await tf.send_message(update, response)
    return FIRST_NAME


async def set_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    first_name = update.effective_message.text
    context.user_data['First_Name'] = first_name
    logger.info("%s entered %s as their first name", username, first_name)
    
    response = Enter_last_name()
    await tf.send_message(update, response)
    
    return LAST_NAME


async def set_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    last_name = update.effective_message.text
    context.user_data['Last_Name'] = last_name
    logger.info("%s entered %s as their last name", username, last_name)
    
    response = Enter_email()
    await tf.send_message(update, response)
    
    return EMAIL


async def set_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    email = update.effective_message.text
    context.user_data['Email'] = email
    logger.info("%s entered %s as their email", username, email)
    
    response = Enter_phone()
    await tf.send_message(update, response)
    
    return PHONE


async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    phone = update.effective_message.text
    context.user_data['Phone_Number'] = phone
    logger.info("%s entered %s as their phone number", username, phone)
    
    response = Enter_address() if context.user_data.get('role') == MEMBER else Enter_role()
    await tf.send_message(update, response)
    
    return OTHER


async def set_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data['role'] == MEMBER:
        address = update.effective_message.text
        context.user_data['Address'] = address
        context.user_data['Join_Date'] = datetime.utcnow().strftime("%Y-%m-%d")
        logger.info("%s entered %s as their address", username, address)
        
        response = Member_profile(
            first_name=context.user_data['First_Name'],
            last_name=context.user_data['Last_Name'],
            email=context.user_data['Email'],
            phone=context.user_data['Phone_Number'],
            address=context.user_data['Address']
        )
        
        res = db_scripts.add_member(context.user_data)
        
    else:
        role = update.effective_message.text
        context.user_data['Employee_Role'] = role
        context.user_data['Hired_Date'] = datetime.utcnow().strftime("%Y-%m-%d")
        logger.info("%s entered %s as their employee role", username, role)
        
        response = Employee_profile(
            first_name=context.user_data['First_Name'],
            last_name=context.user_data['Last_Name'],
            email=context.user_data['Email'],
            phone=context.user_data['Phone_Number'],
            role=context.user_data['Employee_Role']
        )
        
        res = db_scripts.add_employee(context.user_data)
        
    if res.status_code == 200:
        response = account_created() + response
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
    else:
        response = error_handlers.start_again()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
    
    return ConversationHandler.END


async def lost_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """lost message"""
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name

    logger.info("%s is talking nonesense", username)
    response = lost(user.first_name)

    await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['making fun'])
    return None


async def add_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    context.user_data['new_author'] = {}
    logger.info("%s wants to add an author", username)
    
    response = Enter_author_id()
    await tf.send_message(update, response)
    
    return SET_ID


async def set_author_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    author_id = int(update.effective_message.text)
    context.user_data['new_author']['Author_id'] = author_id
    logger.info("%s entered %s as author's id", username, author_id)
    
    response = Enter_author_first_name()
    await tf.send_message(update, response)
    
    return FIRST_NAME


async def author_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    first_name = update.effective_message.text
    context.user_data['new_author']['First_Name'] = first_name
    logger.info("%s entered %s as author's first name", username, first_name)
    
    response = Enter_author_last_name()
    await tf.send_message(update, response)
    
    return LAST_NAME


async def author_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    last_name = update.effective_message.text
    context.user_data['new_author']['Last_Name'] = last_name
    logger.info("%s entered %s as author's last name", username, last_name)
    
    response = Enter_author_email()
    await tf.send_message(update, response)
    
    return EMAIL


async def author_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    email = update.effective_message.text
    context.user_data['new_author']['Email'] = email
    logger.info("%s entered %s as author's email", username, email)
    
    response = Enter_author_phone()
    await tf.send_message(update, response)
    
    return PHONE


async def author_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    phone = update.effective_message.text
    context.user_data['new_author']['Phone_Number'] = phone
    logger.info("%s entered %s as author's phone number", username, phone)
    
    res = db_scripts.add_author(context.user_data['new_author'])
    
    if res.status_code == 200:
        response = author_added()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
    else:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
    
    return ConversationHandler.END


async def add_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END

    context.user_data['new_book'] = {}
    logger.info("%s wants to add a book", username)
    
    response = Enter_book_id()
    await tf.send_message(update, response)
    
    return SET_ID


async def set_book_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    book_id = int(update.effective_message.text)
    context.user_data['new_book']['Book_id'] = book_id
    logger.info("%s entered %s as book's id", username, book_id)
    
    response = Enter_book_title()
    await tf.send_message(update, response)
    
    return TITLE


async def book_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    title = update.effective_message.text
    context.user_data['new_book']['Title'] = title
    logger.info("%s entered %s as book's title", username, title)
    
    response = Enter_book_author_id()
    await tf.send_message(update, response)
    
    return AUTHOR_ID


async def book_author_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    author_id = int(update.effective_message.text)
    context.user_data['new_book']['Author_id'] = author_id
    logger.info("%s entered %s as book's last name", username, author_id)
    
    response = Enter_book_pub_date()
    await tf.send_message(update, response)
    
    return PUB_DATE


async def book_pub_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    pub_date = update.effective_message.text
    context.user_data['new_book']['Published_Year'] = pub_date
    logger.info("%s entered %s as book's published year", username, pub_date)
    
    response = Enter_book_genre()
    await tf.send_message(update, response)
    
    return GENRE


async def book_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    genre = update.effective_message.text
    context.user_data['new_book']['Genre'] = genre
    logger.info("%s entered %s as book's genre", username, genre)
    
    response = Enter_book_copies()
    await tf.send_message(update, response)
    
    return COPIES


async def book_copies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    copies = update.effective_message.text
    context.user_data['new_book']['Copies'] = copies
    logger.info("%s entered %s as book's copies number", username, copies)
    
    res = db_scripts.add_book(context.user_data['new_book'])
    
    if res.status_code == 200:
        response = book_added()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
    else:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
    
    return ConversationHandler.END


async def borrow_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != MEMBER:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return None

    com = update.effective_message.text.split()
    if len(com) == 1:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        return None
    
    title = ' '.join(com[1:])
    logger.info("%s wants to borrow a book: %s", username, title)
    
    res = db_scripts.search_book(title)
    if res.status_code != 200:
        response = error_handlers.book_not_found()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        return None
        
    book = json.loads(res.text)
    if book['Copies'] > 0:
        borrow = {
            "Book_id": int(book['Book_id']),
            "Member_id": user.id,
            "Borrow_Date": datetime.utcnow().strftime("%Y-%m-%d")
        }
        
        res = db_scripts.borrow(borrow)
        if res.status_code == 200:
            response = "Done"
            await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
        else:
            response = error_handlers.something_went_wrong()
            await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        
        return None
    
    response = error_handlers.book_not_found()
    await tf.send_message(update, response)
    return None


async def return_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != MEMBER:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return None

    com = update.effective_message.text.split()
    if len(com) == 1:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        return None
    
    title = ' '.join(com[1:])
    logger.info("%s wants to return a book: %s", username, title)
    
    res = db_scripts.search_book(title)
    if res.status_code != 200:
        response = error_handlers.book_not_found()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        return None
        
    book = json.loads(res.text)
    borrow = {
        "Book_id": int(book['Book_id']),
        "Member_id": user.id,
        "Return_Date": datetime.utcnow().strftime("%Y-%m-%d")
    }
    logger.info("%s wants to return a book: %s", username, borrow)
    res = db_scripts.return_book(borrow)
    if res.status_code == 200:
        response = "Done"
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
    else:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])

    return None


async def delete_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return None

    com = update.effective_message.text.split()
    if len(com) < 3:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])
        return None
    
    book = {
        "Book_id": int(com[1]),
        "Copies": int(com[2])
    }
    logger.info("%s wants to delete some books: %s", username, book)
    res = db_scripts.delete_book(book)
    if res.status_code == 200:
        response = "Done"
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['mission accomplished'])
    else:
        response = error_handlers.something_went_wrong()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['panic'])

    return None


async def expired(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """expired conversation"""
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name

    logger.info("%s requests for an expired conversation", username)
    query = update.callback_query

    await query.answer(text=error_handlers.CONVERSATION_EXPIRED)
    await query.edit_message_reply_markup(reply_markup=None)
    return None


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name

    logger.info("%s wants help", username)
    
    response = help_center()
    await tf.send_message(update, response)
    
    
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name

    logger.info("%s wants to see their profile", username)
    
    if context.user_data['role'] == MEMBER:
        response = Member_profile(
            first_name=context.user_data['First_Name'],
            last_name=context.user_data['Last_Name'],
            email=context.user_data['Email'],
            phone=context.user_data['Phone_Number'],
            address=context.user_data['Address']
        )
    else:
        response = Employee_profile(
            first_name=context.user_data['First_Name'],
            last_name=context.user_data['Last_Name'],
            email=context.user_data['Email'],
            phone=context.user_data['Phone_Number'],
            role=context.user_data['Employee_Role']
        )
    await tf.send_message(update, response)


async def members_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['members_log_ind'] = head
    
    data = db_scripts.members_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see members log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= MEMBERS_LIST_LENGTH:
        logger.info("%s want to see members log - just one page", username)
        response = members_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_members'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = members_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def members_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['members_log_ind'] + MEMBERS_LIST_LENGTH
    logger.info("%s - members log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.members_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_members')]
    ]
    if head + MEMBERS_LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_members'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['members_log_ind'] = head
    response = members_changes(data, head, min(head + MEMBERS_LIST_LENGTH, data_length))
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def members_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['members_log_ind'] - MEMBERS_LIST_LENGTH
    logger.info("%s - members log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.members_log()
    
    keyboard = [
        []
    ]
    if head - MEMBERS_LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_members'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_members'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['members_log_ind'] = head
    response = members_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def employees_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['employees_log_ind'] = head
    
    data = db_scripts.employees_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see employees log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= MEMBERS_LIST_LENGTH:
        logger.info("%s want to see employees log - just one page", username)
        response = employees_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_employees'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = employees_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def employees_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['employees_log_ind'] + MEMBERS_LIST_LENGTH
    logger.info("%s - employees log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.employees_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_employees')]
    ]
    if head + MEMBERS_LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_employees'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    response = employees_changes(data, head, min(head + MEMBERS_LIST_LENGTH, data_length))
    context.user_data['employees_log_ind'] = head
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def employees_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['employees_log_ind'] - MEMBERS_LIST_LENGTH
    logger.info("%s - employees log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.employees_log()
    
    keyboard = [
        []
    ]
    if head - MEMBERS_LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_employees'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_employees'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['employees_log_ind'] = head
    response = employees_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def authors_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['authors_log_ind'] = head
    
    data = db_scripts.authors_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see authors log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= MEMBERS_LIST_LENGTH:
        logger.info("%s want to see authors log - just one page", username)
        response = authors_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_authors'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = authors_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def authors_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['authors_log_ind'] + MEMBERS_LIST_LENGTH
    logger.info("%s - authors log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.authors_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_authors')]
    ]
    if head + MEMBERS_LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_authors'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['authors_log_ind'] = head
    response = authors_changes(data, head, min(head + MEMBERS_LIST_LENGTH, data_length))
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def authors_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['authors_log_ind'] - MEMBERS_LIST_LENGTH
    logger.info("%s - authors log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.authors_log()
    
    keyboard = [
        []
    ]
    if head - MEMBERS_LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_authors'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_authors'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['authors_log_ind'] = head
    response = authors_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def books_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['books_log_ind'] = head
    
    data = db_scripts.books_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see books log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= MEMBERS_LIST_LENGTH:
        logger.info("%s want to see books log - just one page", username)
        response = books_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_books'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = books_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def books_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['books_log_ind'] + MEMBERS_LIST_LENGTH
    logger.info("%s - books log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.books_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_books')]
    ]
    if head + MEMBERS_LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_books'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['books_log_ind'] = head
    response = books_changes(data, head, min(head + MEMBERS_LIST_LENGTH, data_length))
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def books_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['books_log_ind'] - MEMBERS_LIST_LENGTH
    logger.info("%s - books log conversation - [%s : %s]",
                username, head, head + MEMBERS_LIST_LENGTH)
    data = db_scripts.books_log()
    
    keyboard = [
        []
    ]
    if head - MEMBERS_LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_books'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_books'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['books_log_ind'] = head
    response = books_changes(data, head, head + MEMBERS_LIST_LENGTH)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def borrows_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['borrows_log_ind'] = head
    
    data = db_scripts.borrows_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see borrows log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= LIST_LENGTH:
        logger.info("%s want to see borrows log - just one page", username)
        response = borrows_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_borrows'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['borrows_log_ind'] = head
    response = borrows_changes(data, head, head + LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def borrows_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['borrows_log_ind'] + LIST_LENGTH
    logger.info("%s - borrows log conversation - [%s : %s]",
                username, head, head + LIST_LENGTH)
    data = db_scripts.borrows_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_borrows')]
    ]
    if head + LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_borrows'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['borrows_log_ind'] = head
    response = borrows_changes(data, head, min(head + LIST_LENGTH, data_length))
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def borrows_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['borrows_log_ind'] - LIST_LENGTH
    logger.info("%s - borrows log conversation - [%s : %s]",
                username, head, head + LIST_LENGTH)
    data = db_scripts.borrows_log()
    
    keyboard = [
        []
    ]
    if head - LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_borrows'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_borrows'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['borrows_log_ind'] = head
    response = borrows_changes(data, head, head + LIST_LENGTH)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def returns_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    
    if context.user_data.get('role') != EMPLOYEE:
        response = error_handlers.access_denied()
        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['bite me'])
        
        return ConversationHandler.END
    
    head = 0
    context.user_data['returns_log_ind'] = head
    
    data = db_scripts.returns_log()
    data_length = len(data['changed_date'])
    if data_length == 0:
        logger.info("%s want to see returns log - no logs found", username)
        response = error_handlers.no_logs()

        await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['disappointed'])
        return ConversationHandler.END
    
    if data_length <= LIST_LENGTH:
        logger.info("%s want to see returns log - just one page", username)
        response = returns_changes(data, head, data_length)

        await tf.send_message(update, response)
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton(
                emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_returns'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = returns_changes(data, head, head + LIST_LENGTH)
    await tf.send_message(update, response, reply_markup=reply_markup)
    return ACTIVE


async def returns_log_next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['returns_log_ind'] + LIST_LENGTH
    logger.info("%s - returns log conversation - [%s : %s]",
                username, head, head + LIST_LENGTH)
    data = db_scripts.returns_log()
    data_length = len(data['changed_date'])
    
    keyboard = [
        [InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_returns')]
    ]
    if head + LIST_LENGTH < data_length:
        keyboard[0].append(InlineKeyboardButton(
            emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_returns'))

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['returns_log_ind'] = head
    response = returns_changes(data, head, min(head + LIST_LENGTH, data_length))
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE


async def returns_log_previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    query = update.callback_query
    await query.answer()
    
    head = context.user_data['returns_log_ind'] - LIST_LENGTH
    logger.info("%s - returns log conversation - [%s : %s]",
                username, head, head + LIST_LENGTH)
    data = db_scripts.returns_log()
    
    keyboard = [
        []
    ]
    if head - LIST_LENGTH >= 0:
        keyboard[0].append(InlineKeyboardButton(
            emojies.LEFTPOINTING_DOUBLE_TRIANGLE, callback_data='pre_returns'))
    keyboard[0].append(InlineKeyboardButton(
        emojies.RIGHTPOINTING_DOUBLE_TRIANGLE, callback_data='next_returns'))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['returns_log_ind'] = head
    response = returns_changes(data, head, head + LIST_LENGTH)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return ACTIVE



def main() -> None:
    application = Application.builder().token(Data.BOT_API_KEY).build()
    
    start_conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_private_chat),
            CommandHandler('editprofile', edit_profile),
        ],
        states={
            SET_ROLE: [
                CallbackQueryHandler(member, pattern=f"^{MEMBER}$"),
                CallbackQueryHandler(employee, pattern=f"^{EMPLOYEE}$")
            ],
            FIRST_NAME: [
                MessageHandler(filters.ALL, set_first_name)
            ],
            LAST_NAME: [
                MessageHandler(filters.ALL, set_last_name)
            ],
            EMAIL: [
                MessageHandler(filters.ALL, set_email)
            ],
            PHONE: [
                MessageHandler(filters.ALL, set_phone)
            ],
            OTHER: [
                MessageHandler(filters.ALL, set_other)
            ]
        },
        fallbacks=[
            CommandHandler('start', start_private_chat),
            CommandHandler('editprofile', edit_profile),
        ]
    )
    application.add_handler(start_conversation_handler)
    
    add_author_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('addauthor', add_author)],
        states={
            SET_ID: [
                MessageHandler(filters.ALL, set_author_id)
            ],
            FIRST_NAME: [
                MessageHandler(filters.ALL, author_first_name)
            ],
            LAST_NAME: [
                MessageHandler(filters.ALL, author_last_name)
            ],
            EMAIL: [
                MessageHandler(filters.ALL, author_email)
            ],
            PHONE: [
                MessageHandler(filters.ALL, author_phone)
            ]
        },
        fallbacks=[
            CommandHandler('addauthor', add_author)
        ]
    )
    application.add_handler(add_author_conversation_handler)
    
    add_book_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('addbook', add_book)],
        states={
            SET_ID: [
                MessageHandler(filters.ALL, set_book_id)
            ],
            TITLE: [
                MessageHandler(filters.ALL, book_title)
            ],
            AUTHOR_ID: [
                MessageHandler(filters.ALL, book_author_id)
            ],
            PUB_DATE: [
                MessageHandler(filters.ALL, book_pub_date)
            ],
            GENRE: [
                MessageHandler(filters.ALL, book_genre)
            ],
            COPIES: [
                MessageHandler(filters.ALL, book_copies)
            ]
        },
        fallbacks=[
            CommandHandler('addbook', add_book)
        ]
    )
    application.add_handler(add_book_conversation_handler)
    
    members_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('memberslog', members_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(members_log_next_page, pattern="^next_members$"),
                CallbackQueryHandler(members_log_previous_page, pattern="^pre_members$")
            ]
        },
        fallbacks=[
            CommandHandler('memberslog', members_log),
        ]
    )
    application.add_handler(members_changes_conversation_handler)
    
    employees_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('employeeslog', employees_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(employees_log_next_page, pattern="^next_employees$"),
                CallbackQueryHandler(employees_log_previous_page, pattern="^pre_employees$")
            ]
        },
        fallbacks=[
            CommandHandler('employeeslog', employees_log),
        ]
    )
    application.add_handler(employees_changes_conversation_handler)
    
    authors_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('authorslog', authors_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(authors_log_next_page, pattern="^next_authors$"),
                CallbackQueryHandler(authors_log_previous_page, pattern="^pre_authors$")
            ]
        },
        fallbacks=[
            CommandHandler('authorslog', authors_log),
        ]
    )
    application.add_handler(authors_changes_conversation_handler)
    
    books_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('bookslog', books_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(books_log_next_page, pattern="^next_books$"),
                CallbackQueryHandler(books_log_previous_page, pattern="^pre_books$")
            ]
        },
        fallbacks=[
            CommandHandler('bookslog', books_log),
        ]
    )
    application.add_handler(books_changes_conversation_handler)
    
    borrows_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('borrowslog', borrows_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(borrows_log_next_page, pattern="^next_borrows$"),
                CallbackQueryHandler(borrows_log_previous_page, pattern="^pre_borrows$")
            ]
        },
        fallbacks=[
            CommandHandler('borrowslog', borrows_log),
        ]
    )
    application.add_handler(borrows_changes_conversation_handler)
    
    returns_changes_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('returnslog', returns_log)],
        states={
            ACTIVE: [
                CallbackQueryHandler(returns_log_next_page, pattern="^next_returns$"),
                CallbackQueryHandler(returns_log_previous_page, pattern="^pre_returns$")
            ]
        },
        fallbacks=[
            CommandHandler('returnslog', returns_log),
        ]
    )
    application.add_handler(returns_changes_conversation_handler)
    
    application.add_handler(CommandHandler('borrow', borrow_book))
    application.add_handler(CommandHandler('return', return_book))
    application.add_handler(CommandHandler('delete', delete_book))
    application.add_handler(CommandHandler('profile', profile))
    application.add_handler(CommandHandler('help', help))
    
    
    # Interpret any other command or text message as a start of a private chat.
    # This will record the user as being in a private chat with bot.
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, lost_path))
    application.add_handler(CallbackQueryHandler(expired))
    
    
    # ...and the error handler
    application.add_error_handler(error_handler)
    
    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=1)
    

if __name__ == "__main__":
    main()