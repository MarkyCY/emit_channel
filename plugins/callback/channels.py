
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.mongodb import get_db
from bson import ObjectId

#region add channel
@Client.on_callback_query(filters.regex(r"^add_channel_-?(\d+)_([a-zA-Z]{2})$"))
async def add_channel_callback(app: Client, query: CallbackQuery):

    db = await get_db()
    Channel = db.channels
    Admins = db.admins
    PChannel = db.principal_channels

    parts = query.data.split('_')
    chat_id = int(parts[2])
    lang = parts[3]

    pchn = await PChannel.find_one({'chat_id': chat_id})

    if pchn:
        await app.edit_message_text(query.message.chat.id, query.message.id, 'Los canales alfa no pueden estar anexados.')
        return

    message = query.message
    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    find_chanel = await Channel.find_one({'chat_id': message.chat.id})

    if find_chanel:
        await app.answer_callback_query(query.id, 'El canal ya se encuentra en la lista de canales.')
        return
    
    try:
        data = await Channel.insert_one({
            'chat_id': chat_id,
            'lang': lang 
        })
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al agregar el canal.', show_alert=True)
        return
    
    markup = []

    async for channel in PChannel.find():
        markup.append([InlineKeyboardButton(channel['name'], callback_data=f'ins_chn_{channel["chat_id"]}_{data.inserted_id}')])

    markup = InlineKeyboardMarkup(markup)

    await app.edit_message_text(message.chat.id, message.id, f"Selecciona a que `Canal Alfa` pertenece este canal.", reply_markup=markup)

#region insert channel principal
@Client.on_callback_query(filters.regex(r"^ins_chn_-?(\d+)_[a-f\d]{24}$"))
async def ins_chn_callback(app: Client, query: CallbackQuery):

    chat_id = query.message.chat.id

    db = await get_db()
    Channel = db.channels
    Admins = db.admins
    PChannel = db.principal_channels

    parts = query.data.split('_')
    pchat_id = int(parts[2])
    ins_id = ObjectId(parts[3])

    
    message = query.message
    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return
    
    pchn = await PChannel.find_one({'chat_id': chat_id})
    if pchn:
        await app.answer_callback_query(query.id, 'Los canales alfa no pueden estar inscritos en otros canales alfa.')
        return
    
    find_principal_chn = await PChannel.find_one({'chat_id': pchat_id})

    if not find_principal_chn:
        await Channel.delete_one({'_id': ins_id})
        await app.edit_message_text(message.chat.id, message.id, f"El canal alfa no existe.")
        return

    try:
        update = await Channel.update_one({'_id': ins_id}, {'$set': {'principal': pchat_id}})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, f'Error al agregar el canal: {e}', show_alert=True)
        return
    
    if update.modified_count == 0:
        await app.answer_callback_query(query.id, 'Error al agregar el canal.', show_alert=True)
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {message.sender_chat.id} agregado al Canal Alfa.")

#region edit channel lang
@Client.on_callback_query(filters.regex(r"^edit_channel_-?(\d+)_([a-zA-Z]{2})$"))
async def edit_channel_lang_callback(app: Client, query: CallbackQuery):

    db = await get_db()
    Channel = db.channels
    Admins = db.admins
    PChannel = db.principal_channels

    parts = query.data.split('_')
    chat_id = int(parts[2])
    lang = parts[3]

    message = query.message
    user_id = query.from_user.id

    pchn = await PChannel.find_one({'chat_id': chat_id})

    if pchn:
        await app.answer_callback_query(query.id, 'Los canales alfas no necesitan idioma.', show_alert=True)
        return

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    find_chanel = await Channel.find_one({'chat_id': chat_id})

    if not find_chanel:
        await app.answer_callback_query(query.id, 'El canal no se encuentra en la lista de canales, debes agregarlo con el comando `/add_channel`.')
        return
    
    if find_chanel['lang'] == lang:
        await app.answer_callback_query(query.id, 'El canal ya tiene este idioma.')
        return

    try:
        update = await Channel.update_one({'chat_id': chat_id}, {'$set': {'lang': lang}})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al cambiar el idioma.', show_alert=True)
        return

    if update.modified_count == 0:
        await app.answer_callback_query(query.id, 'Error al cambiar el idioma.', show_alert=True)
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {message.sender_chat.id} cambiado idioma de `{find_chanel['lang']}` a `{lang}` cambiado.")

#region remove channel
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
        await app.answer_callback_query(query.id, 'El canal no se encuentra en la lista de canales.')
        return

    try:
        await Channel.delete_one({'chat_id': message.chat.id})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'Error al eliminar el canal.')
        return

    await app.edit_message_text(message.chat.id, message.id, f"Canal {chat_id} eliminado de la lista de canales.")


#region Set Principal Channel
@Client.on_callback_query(filters.regex(r"^set_principal_-?(\d+)$"))
async def set_principal_callback(app: Client, query: CallbackQuery):

    message = query.message
    user_id = query.from_user.id

    parts = query.data.split('_')
    chat_id = int(parts[2])

    db = await get_db()
    Channel = db.channels
    PChannel = db.principal_channels
    Admins = db.admins
    
    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    find_chanel = await Channel.find_one({'chat_id': chat_id})
    if find_chanel:
        await app.answer_callback_query(query.id, 'No se puede agregar como alfa un canal anexado a un canal alfa.')
        return

    find_chanel = await PChannel.find_one({'chat_id': chat_id})
    if find_chanel:
        await app.answer_callback_query(query.id, 'Este canal ya esta inscrito como alfa.')
        return
    
    try:
        await PChannel.insert_one({'chat_id': chat_id, 'name': message.chat.title})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'No se pudo agregar el canal como alfa.')
        return
    
    await app.edit_message_text(message.chat.id, message.id, 'Canal agregado como alfa.')
    
#region Unset Principal Channel
@Client.on_callback_query(filters.regex(r"^unset_principal_-?(\d+)$"))
async def unset_principal_callback(app: Client, query: CallbackQuery):

    chat_id = query.message.chat.id
    message = query.message
    user_id = query.from_user.id

    db = await get_db()
    PChannel = db.principal_channels
    Admins = db.admins
    
    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.')
        return

    find_chanel = await PChannel.find_one({'chat_id': chat_id})
    if not find_chanel:
        await app.answer_callback_query(query.id, 'Este canal no se encuentra como alfa.')
        return
    
    try:
        await PChannel.delete_one({'chat_id': chat_id})
    except Exception as e:
        print(e)
        await app.answer_callback_query(query.id, 'No se pudo remover el canal como alfa.')
        return
    
    await app.edit_message_text(message.chat.id, message.id, 'Canal removido como alfa.')