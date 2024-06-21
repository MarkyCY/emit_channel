from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

iso_lang = [
        'ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae',
        'ay', 'az', 'ba', 'bm', 'be', 'bn', 'bh', 'bi', 'bo', 'bs', 'br', 'bg',
        'ca', 'ch', 'ce', 'cv', 'kw', 'co', 'cr', 'cs', 'da', 'de', 'dv', 'dz',
        'el', 'en', 'eo', 'et', 'eu', 'ee', 'fo', 'fa', 'fj', 'fi', 'fr', 'fy',
        'ff', 'gl', 'ka', 'de', 'gd', 'ga', 'gv', 'el', 'gn', 'gu', 'ht', 'ha',
        'he', 'hz', 'hi', 'ho', 'hu', 'is', 'io', 'ig', 'id', 'ia', 'ie', 'iu',
        'ik', 'ga', 'xh', 'zu', 'is', 'it', 'jv', 'ja', 'kl', 'kn', 'kr', 'ks',
        'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'kj', 'ku', 'lo', 'la',
        'lv', 'li', 'ln', 'lt', 'lb', 'lu', 'lg', 'mk', 'mg', 'ms', 'ml', 'mt',
        'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'nd', 'ne', 'ng', 'nb', 'nn', 'no',
        'ii', 'nr', 'oc', 'oj', 'cu', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps',
        'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'sa', 'sc', 'sd', 'se', 'sm', 'sg',
        'sr', 'gd', 'sn', 'si', 'sk', 'sl', 'so', 'st', 'nr', 'es', 'su', 'sw',
        'ss', 'sv', 'ta', 'te', 'tg', 'th', 'ti', 'bo', 'tk', 'tl', 'tn', 'to',
        'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo',
        'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'yo', 'za', 'zu',
    ]


@Client.on_message(filters.command('add_channel'))
async def add_channel_command(app: Client, message: Message):

    chat_id = message.chat.id

    if len(message.command) == 1:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma:\n\nEj. `/add_channel es`')
        return

    lang = message.command[1]
    if lang not in iso_lang:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma válido:\n\nEj. `/add_channel ca`')
        return

    if len(lang) != 2:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma válido:\n\nEj. `/add_channel en`')
        return
    
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Si', callback_data=f'add_channel_{chat_id}_{lang}'),
        ],
    ])

    await app.send_message(message.chat.id, 'Deseas agregar este canal a la lista de canales?', reply_markup=markup)


@Client.on_message(filters.command('change_lang'))
async def change_lang_command(app: Client, message: Message):

    chat_id = message.chat.id

    if len(message.command) == 1:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma para cambiar:\n\nEj. `/change_lang es`')
        return

    lang = message.command[1]

    if lang not in iso_lang:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma válido para cambiar:\n\nEj. `/change_lang ca`')
        return

    if len(lang) != 2:
        await app.send_message(message.chat.id, 'Por favor agregue un idioma válido para cambiar:\n\nEj. `/change_lang en`')
        return
    
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Si', callback_data=f'edit_channel_{chat_id}_{lang}'),
        ],
    ])

    await app.send_message(message.chat.id, f'Deseas cambiar el idioma por `{lang}`?', reply_markup=markup)


@Client.on_message(filters.command('rm_channel'))
async def rm_channel_command(app: Client, message: Message):

    chat_id = message.chat.id

    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Si', callback_data=f'rm_channel_{chat_id}'),
        ],
    ])

    await app.send_message(message.chat.id, f"Deseas eliminar este canal a la lista de canales?", reply_markup=markup)


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