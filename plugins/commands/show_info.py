from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command('info'))
async def info_command(app: Client, message: Message):
    print(message)
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Info', callback_data='info')
        ],
    ])
    await app.send_message(message.chat.id, 'Info', reply_markup=markup)


@Client.on_callback_query(filters.regex('info'))
async def info_callback(app: Client, query: Message):
    print(query)
    await app.send_message(query.message.chat.id, query.from_user.id)


@Client.on_message(filters.command('info_chat'))
async def info_chat_command(app: Client, message: Message):
    chat = await app.get_chat(message.chat.id)
    print(chat)