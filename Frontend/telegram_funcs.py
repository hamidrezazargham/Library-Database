from telegram import Update, ChatMember, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes
)


async def check_membership(user_id: int, chat_ids: list, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user_id is a member of all the chats in chat_ids list"""
    for chat_id in chat_ids:
        member = await context.bot.getChatMember(chat_id, user_id)
        if member is None:
            return False
        if member.status not in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
            return False
    return True

async def send_message(update: Update, response: str, reply_markup: InlineKeyboardMarkup = None, sticker: str = None):
    if sticker is not None:
        await update.effective_message.reply_sticker(sticker)
    return await update.effective_message.reply_markdown_v2(response, reply_to_message_id=update.effective_message.id, disable_web_page_preview=True, reply_markup=reply_markup)

async def send_sticker(update: Update, sticker: str) -> None:
    return await update.effective_message.reply_sticker(sticker)
    
async def send_photo(update: Update, photo: str, caption: str = None, reply_markup: InlineKeyboardMarkup = None):
    return await update.effective_message.reply_photo(photo=photo, caption=caption, reply_to_message_id=update.effective_message.id, reply_markup=reply_markup, parse_mode="MarkdownV2")