from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('rm_msg'))
async def rm_msg_command(app: Client, message: Message):

    chat_id = message.chat.id

    if message.reply_to_message is None:
        await app.send_message(message.chat.id, "Por favor responde a un mensaje para eliminarlo")
        return

    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Si', callback_data=f'rm_msg_{chat_id}_{message.reply_to_message.id}'),
        ],
    ])

    await app.send_message(message.chat.id, f"Deseas eliminar este mensaje de todas partes?", reply_markup=markup)