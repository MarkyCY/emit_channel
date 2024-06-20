from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters

from dotenv import load_dotenv
from database.mongodb import get_db
from traduction.translate import translate

load_dotenv()

import os

general_chat = int(os.getenv('CHANNEL_OFFICIAL'))


@Client.on_message(filters.channel & filters.chat(general_chat))
async def on_msg_chnl(app: Client, message: Message):

    msg_id = message.id
    msgs_ids = []

    db = await get_db()
    Channel = db.channels
    Msgs = db.messages_saved

    i = 0
    async for channel in Channel.find({}):
        i += 1

        if message.chat.id == channel['chat_id']:
            continue

        try:
            msg = await app.send_message(channel['chat_id'], await translate(message.text, channel['lang']))
        except Exception as e:
            print(e)
            app.send_message(message.chat.id, 'Error al enviar el mensaje.')
            continue

        ms_id = msg.id
        ms_chat_id = msg.chat.id
        group = [ms_id, ms_chat_id]

        msgs_ids.append(group)

    try:
        await Msgs.insert_one({
            'msg_id': msg_id,
            'messages_list': msgs_ids
        })
    except Exception as e:
        print(e)
        await app.send_message(message.chat.id, 'Error al insertar el mensaje en la base de datos.')



@Client.on_edited_message(filters.channel & filters.chat(general_chat))
async def on_edit_msg_chnl(app: Client, message: Message):

    msg_id = message.id

    db = await get_db()
    Channel = db.channels
    Msgs = db.messages_saved

    msg_sel = await Msgs.find_one({'msg_id': msg_id})

    if not msg_sel:
        return

    for msg in msg_sel['messages_list']:

        channel = await Channel.find_one({'chat_id': msg[1]})

        if not channel:
            continue

        try:
            await app.edit_message_text(msg[1], msg[0], await translate(message.text, channel['lang']))
        except Exception as e:
            print(e)
