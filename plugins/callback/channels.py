
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from database.mongodb import get_db

@Client.on_callback_query(filters.regex(r"^add_channel_-?(\d+)_([a-zA-Z]{2})$"))
async def add_channel_callback(app: Client, query: CallbackQuery):

    db = await get_db()
    Channel = db.channels
    Admins = db.admins

    parts = query.data.split('_')
    chat_id = int(parts[2])
    lang = parts[3]

    message = query.message
    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    find_chanel = await Channel.find_one({'chat_id': message.chat.id})

    if find_chanel:
        await app.edit_message_text(message.chat.id, message.id, 'El canal ya se encuentra en la lista de canales.')
        return
    
    try:
        await Channel.insert_one({
            'chat_id': chat_id,
            'lang': lang 
})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al agregar el canal.', show_alert=True)
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {message.sender_chat.id} con idioma `{lang}` agregado a la lista de canales.")
    
    
@Client.on_callback_query(filters.regex(r"^edit_channel_-?(\d+)_([a-zA-Z]{2})$"))
async def edit_channel_lang_callback(app: Client, query: CallbackQuery):

    db = await get_db()
    Channel = db.channels
    Admins = db.admins

    parts = query.data.split('_')
    chat_id = int(parts[2])
    lang = parts[3]

    message = query.message
    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    find_chanel = await Channel.find_one({'chat_id': chat_id})

    if not find_chanel:
        await app.edit_message_text(message.chat.id, message.id, 'El canal no se encuentra en la lista de canales, debes agregarlo con el comando `/add_channel`.')
        return
    
    if find_chanel['lang'] == lang:
        await app.edit_message_text(message.chat.id, message.id, 'El canal ya tiene este idioma.')
        return

    try:
        await Channel.update_one({'chat_id': chat_id}, {'$set': {'lang': lang}})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al cambiar el idioma.', show_alert=True)
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {message.sender_chat.id} cambiado idioma de `{find_chanel['lang']}` a `{lang}` cambiado.")


@Client.on_callback_query(filters.regex(r"^rm_channel_-?(\d+)$"))
async def remove_channel_callback(app: Client, query: CallbackQuery):

    db = await get_db()
    Channel = db.channels
    Admins = db.admins

    parts = query.data.split('_')
    chat_id = int(parts[2])

    message = query.message
    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return
    
    find_chanel = await Channel.find_one({'chat_id': chat_id})

    if not find_chanel:
        await app.edit_message_text(message.chat.id, message.id, 'El canal no se encuentra en la lista de canales.')
        return

    try:
        await Channel.delete_one({'chat_id': message.chat.id})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al eliminar el canal.')
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {chat_id} eliminado de la lista de canales.")
