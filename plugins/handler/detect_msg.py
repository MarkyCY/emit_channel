from pyrogram import Client, enums
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio
from pyrogram import filters

from dotenv import load_dotenv
from database.mongodb import get_db
from traduction.translate import translate

import asyncio

load_dotenv()

async def get_principal_chats():

    db = await get_db()
    PChannel = db.principal_channels

    ListChn = []

    async for channel in PChannel.find():
        ListChn.append(channel['chat_id'])

    return ListChn


def convert_entities_to_html(text, entities):
    # Mapeo de tipos de entidad a etiquetas HTML
    entity_to_html = {
        "MessageEntityType.BOLD": ("<b>", "</b>"),
        "MessageEntityType.ITALIC": ("<i>", "</i>"),
        "MessageEntityType.UNDERLINE": ("<u>", "</u>"),
        "MessageEntityType.STRIKETHROUGH": ("<s>", "</s>"),
        "MessageEntityType.BLOCKQUOTE": ("<blockquote>", "</blockquote>"),
        "MessageEntityType.CODE": ("<code>", "</code>"),
        "MessageEntityType.SPOILER": ("<spoiler>", "</spoiler>"),
        "MessageEntityType.TEXT_LINK": ("<a href=\"{}\">", "</a>"),
        "MessageEntityType.MENTION": ("<a href=\"tg://resolve?domain={}\">", "</a>")
    }

    # Lista de partes del texto para ensamblar al final
    parts = []
    last_offset = 0

    for entity in sorted(entities, key=lambda e: e.offset):
        start, length = entity.offset, entity.length
        end = start + length

        # Añadir texto sin formato antes de la entidad actual
        if start > last_offset:
            parts.append(text[last_offset:start])

        # Añadir texto con formato si el tipo de entidad es conocido
        entity_text = text[start:end]
        entity_type = str(entity.type)
        
        if entity_type in entity_to_html:
            if entity_type == "MessageEntityType.TEXT_LINK":
                url = entity.url
                parts.append(entity_to_html[entity_type][0].format(url) + entity_text + entity_to_html[entity_type][1])
            elif entity_type == "MessageEntityType.MENTION":
                username = entity_text[1:]  # Remove the "@" symbol
                parts.append(entity_to_html[entity_type][0].format(username) + entity_text + entity_to_html[entity_type][1])
            else:
                parts.append(entity_to_html[entity_type][0] + entity_text + entity_to_html[entity_type][1])

        last_offset = end

    # Añadir cualquier texto restante después de la última entidad
    if last_offset < len(text):
        parts.append(text[last_offset:])

    # Unir todas las partes y retornar el resultado
    return ''.join(parts)


@Client.on_message(filters.channel)
async def on_msg_chnl(app: Client, message: Message):

    chat_id = message.chat.id
    general_chat = await get_principal_chats()

    if chat_id not in general_chat:
        return
    
    msg_id = message.id
    msgs_ids = []

    db = await get_db()
    Channel = db.channels
    Msgs = db.messages_saved

    i = 0
    async for channel in Channel.find({"principal": chat_id}):
        i += 1

        if chat_id == channel['chat_id']:
            continue

        try:
            if message.text:
                if message.entities:
                    text = convert_entities_to_html(message.text, message.entities)
                else:
                    text = message.text
                msg = await app.send_message(channel['chat_id'], await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
            elif message.media:

                media = str(message.media).split('.')[1].lower()
                if message.entities:
                    text = convert_entities_to_html(message.caption, message.entities)
                else:
                    text = message.caption

                if media == 'photo':
                    msg = await app.send_photo(channel['chat_id'], message.photo.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                if media == 'video':
                    msg = await app.send_video(channel['chat_id'], message.video.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                if media == 'document':
                    msg = await app.send_document(channel['chat_id'], message.document.file_id, caption = await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                if media == 'audio':
                    msg = await app.send_audio(channel['chat_id'], message.audio.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            print(e)
            await app.send_message(message.chat.id, 'Error al enviar el mensaje.')
            continue

        ms_id = msg.id
        ms_chat_id = msg.chat.id
        group = [ms_id, ms_chat_id]

        msgs_ids.append(group)

    try:
        await Msgs.insert_one({
            'msg_id': msg_id,
            'chat_id': chat_id,
            'messages_list': msgs_ids
        })
    except Exception as e:
        print(e)
        await app.send_message(message.chat.id, 'Error al insertar el mensaje en la base de datos.')



@Client.on_edited_message(filters.channel)
async def on_edit_msg_chnl(app: Client, message: Message):
    general_chat = await get_principal_chats()
    
    if message.chat.id not in general_chat:
        return
    
    msg_id = message.id

    db = await get_db()
    Channel = db.channels
    Msgs = db.messages_saved

    msg_sel = await Msgs.find_one({'msg_id': msg_id, 'chat_id': message.chat.id})

    if not msg_sel:
        return

    for msg in msg_sel['messages_list']:

        channel = await Channel.find_one({'chat_id': msg[1]})

        if not channel:
            continue

        try:
            if message.text:
                if message.entities:
                    text = convert_entities_to_html(message.text, message.entities)
                else:
                    text = message.text
                await app.edit_message_text(msg[1], msg[0], await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
            elif message.media:

                media = str(message.media).split('.')[1].lower()
                if message.entities:
                    text = convert_entities_to_html(message.caption, message.entities)
                else:
                    text = message.caption

                if media == 'photo':
                    add_media = InputMediaPhoto(message.photo.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'video':
                    add_media = InputMediaVideo(message.video.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'document':
                    add_media = InputMediaDocument(message.document.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                    await app.edit_message_media(msg[1], msg[0], add_media)
                if media == 'audio':
                    add_media = InputMediaAudio(message.audio.file_id, await translate(text, channel['lang']), parse_mode=enums.ParseMode.HTML)
                    await app.edit_message_media(msg[1], msg[0], add_media)
                
        except Exception as e:
            print(e)
