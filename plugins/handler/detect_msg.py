from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio
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
            if message.text:
                msg = await app.send_message(channel['chat_id'], await translate(message.text, channel['lang']))
            elif message.media:
                media = str(message.media).split('.')[1].lower()
                if media == 'photo':
                    msg = await app.send_photo(channel['chat_id'], message.photo.file_id, await translate(message.caption, channel['lang']))
                if media == 'video':
                    msg = await app.send_video(channel['chat_id'], message.video.file_id, await translate(message.caption, channel['lang']))
                if media == 'document':
                    msg = await app.send_document(channel['chat_id'], message.document.file_id, caption = await translate(message.caption, channel['lang']))
                if media == 'audio':
                    msg = await app.send_audio(channel['chat_id'], message.audio.file_id, await translate(message.caption, channel['lang']))
                if media == 'voice':
                    msg = await app.send_voice(channel['chat_id'], message.voice.file_id, await translate(message.caption, channel['lang']))
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
            if message.text:
                await app.edit_message_text(msg[1], msg[0], await translate(message.text, channel['lang']))
            elif message.media:
                media = str(message.media).split('.')[1].lower()
                if media == 'photo':
                    add_media = InputMediaPhoto(message.photo.file_id, await translate(message.caption, channel['lang']))
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'video':
                    add_media = InputMediaVideo(message.video.file_id, await translate(message.caption, channel['lang']))
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'document':
                    add_media = InputMediaDocument(message.document.file_id, await translate(message.caption, channel['lang']))
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'audio':
                    add_media = InputMediaAudio(message.audio.file_id, await translate(message.caption, channel['lang']))
                    await app.edit_message_media(msg[1], msg[0], add_media)
                
        except Exception as e:
            print(e)
