from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from database.mongodb import get_db


@Client.on_callback_query(filters.regex(r"^rm_msg_-?(\d+)_(\d+)$"))
async def remove_msgs(app: Client, query: CallbackQuery):

    db = await get_db()
    Admins = db.admins
    Channel = db.channels
    Msgs = db.messages_saved

    parts = query.data.split('_')
    chat_id = int(parts[2])
    msg_id = int(parts[3])

    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return
    
    msg_sel = await Msgs.find_one({'msg_id': msg_id})

    if not msg_sel:
        await app.answer_callback_query(query.id, 'No existe el mensaje en la base de datos.', show_alert=True)
        return

    for msg in msg_sel['messages_list']:

        channel = await Channel.find_one({'chat_id': msg[1]})

        if not channel:
            continue
        
        try:
            await app.delete_messages(msg[1], msg[0])
        except Exception as e:
            print(e)

    try:
        await app.delete_messages(chat_id, msg_id)
    except Exception as e:
        print(e)
        return
    
    await app.answer_callback_query(query.id, 'Los mensajes han sido eliminados.', show_alert=True)