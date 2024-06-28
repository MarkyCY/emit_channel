from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup



@Client.on_message(filters.command('info'))
async def info_chat_command(app: Client, message: Message):
    text = f"""
Información:

Chat Title: <code>{message.chat.title}</code>
Chat ID: <code>{message.chat.id}</code>
"""
    if message.reply_to_message:
        text += f"""
Reply Message ID: <code>{message.reply_to_message.id}</code>
"""
    #btns = InlineKeyboardMarkup([
    #    [InlineKeyboardButton('Hacer chat Principal', callback_data=f'principal_{message.chat.id}')]
    #])

    await app.send_message(message.chat.id, text)#, reply_markup=InlineKeyboardMarkup(btns))