import logging
import traceback
import html
import json
from datetime import datetime

from telegram.constants import ParseMode
from telegram import Chat, Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
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
import db_scripts


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# logging.basicConfig(
#     filename="botlog.log", encoding='utf-8',
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# start conversation states
SET_ROLE = 0
MEMBER_FIRST_NAME, MEMBER_LAST_NAME, MEMBER_EMAIL, MEMBER_PHONE, MEMBER_ADDRESS = range(1, 6)
EMPLOYEE_FIRST_NAME, EMPLOYEE_LAST_NAME, EMPLOYEE_ROLE, EMPLOYEE_EMAIL, EMPLOYEE_PHONE = range(6, 11)
LOAD_NEWS = "load_news"
NEWS_EXPIRED = "news_expired"


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
        await tf.send_message(update, response)
    
        
    logger.info("%s started a private chat with the bot", username)
    keyboard = [
        [InlineKeyboardButton(text="Member", callback_data="add_member")],
        [InlineKeyboardButton(text="Emmployee", callback_data="add_employee")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    response = start(user.first_name)

    await tf.send_message(update, response, reply_markup=reply_markup)
    return SET_ROLE


async def set_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name


async def lost_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """lost message"""
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    logger.info("%s is talking nonesense", username)
    response = lost(user.first_name)

    await tf.send_message(update, response, sticker=stickers.BLACK_CHERRY['making fun'])
    return None


async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    member = {
        "Member_id": int(com[1]),
        "First_Name": com[2],
        "Last_Name": com[3],
        "Email": com[4],
        "Phone_Number": com[5],
        "Address": com[6],
        "Join_Date": com[7]
    }
    logger.info("%s wants to add member: %s", username, member)
    res = db_scripts.add_member(member)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


async def add_employee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    employee = {
        "Employee_id": int(com[1]),
        "First_Name": com[2],
        "Last_Name": com[3],
        "Email": com[4],
        "Phone_Number": com[5],
        "Employee_Role": com[6]
    }
    logger.info("%s wants to add employee: %s", username, employee)
    res = db_scripts.add_employee(employee)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


async def add_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    author = {
        "Author_id": int(com[1]),
        "First_Name": com[2],
        "Last_Name": com[3],
        "Email": com[4],
        "Phone_Number": com[5]
    }
    logger.info("%s wants to add author: %s", username, author)
    res = db_scripts.add_author(author)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


async def add_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    book = {
        "Book_id": int(com[1]),
        "Title": com[2],
        "Author_id": int(com[3]),
        "Published_Year": com[4],
        "Genre": com[5],
        "Copies": int(com[6])
    }
    logger.info("%s wants to add book: %s", username, book)
    res = db_scripts.add_book(book)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


async def borrow_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    borrow = {
        "Book_id": com[1],
        "Member_id": com[2],
        "Borrow_Date": com[3]
    }
    logger.info("%s wants to borrow a book: %s", username, borrow)
    res = db_scripts.borrow(borrow)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


async def return_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    borrow = {
        "Book_id": com[1],
        "Member_id": com[2],
        "Return_Date": com[3]
    }
    logger.info("%s wants to return a book: %s", username, borrow)
    res = db_scripts.borrow(borrow)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None

async def delete_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username is not None else user.full_name
    # user_ids = db_scripts.get_user_ids()
    
    # if user.id not in user_ids:
    #     logger.info("%s started a private chat with the bot", username)
    #     return await start_private_chat(update, context)

    com = update.effective_message.text.split()
    book = {
        "Book_id": int(com[1]),
        "Copies": int(com[2])
    }
    logger.info("%s wants to delete book: %s", username, book)
    res = db_scripts.delete_book(book)
    if res.status_code == 200:
        response = "Done"
    else:
        response = "Somthing Went Wrong!"

    await tf.send_message(update, response)
    return None


def main() -> None:
    application = Application.builder().token(data.BOT_API_KEY).build()
    
    application.add_handler(CommandHandler('addmember', add_member))
    application.add_handler(CommandHandler('addemployee', add_employee))
    application.add_handler(CommandHandler('addbook', add_book))
    application.add_handler(CommandHandler('borrowbook', borrow_book))
    application.add_handler(CommandHandler('returnbook', return_book))
    application.add_handler(CommandHandler('deletebook', delete_book))
    
    # Interpret any other command or text message as a start of a private chat.
    # This will record the user as being in a private chat with bot.
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, lost_path))
    
    
    # ...and the error handler
    application.add_error_handler(error_handler)
    
    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=1)
    
    # start_conversation_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start_private_chat)],
    #     states={
    #         ACTIVE: [
    #             CallbackQueryHandler(joined, pattern="^joined$"),
    #             CallbackQueryHandler(show_commands, pattern="^commands$")
    #         ]
    #     },
    #     fallbacks=[
    #         CommandHandler('start', start_private_chat),
    #     ]
    # )
    # application.add_handler(start_conversation_handler)