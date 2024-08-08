
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

from traduction.translate import translate
from database.mongodb import get_db
from bson import ObjectId



@Client.on_callback_query(filters.regex(r"^resend_[a-f\d]{24}$"))
async def re_send_msg(app: Client, query: CallbackQuery):

    db = await get_db()
    Msgs = db.messages_saved
    LostMsgs = db.lost_messages
    Channel = db.channels
    Admins = db.admins

    parts = query.data.split('_')
    lostmsg_id = ObjectId(parts[1])

    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    try:
        lostmsg = await LostMsgs.find_one({"_id": lostmsg_id})
        channel = await Channel.find_one({"chat_id": lostmsg['chat_id']})

        media = lostmsg['media']
        file_id = lostmsg['file_id']

        text_tr = await translate(lostmsg['text'], channel['lang'])

        if media is not None:
            if media == 'photo':
                msg = await app.send_photo(lostmsg['chat_id'], file_id, text_tr, parse_mode=enums.ParseMode.HTML)
            if media == 'video':
                msg = await app.send_video(lostmsg['chat_id'], file_id, text_tr, parse_mode=enums.ParseMode.HTML)
            if media == 'document':
                msg = await app.send_document(lostmsg['chat_id'], file_id, text_tr, parse_mode=enums.ParseMode.HTML)
            if media == 'audio':
                msg = await app.send_audio(lostmsg['chat_id'], file_id, text_tr, parse_mode=enums.ParseMode.HTML)
        else:
            msg = await app.send_message(lostmsg['chat_id'], text_tr, parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await app.answer_callback_query(query.id, 'Error al reenviar el mensaje.')
        return print(e)
    
    await Msgs.update_one({"msg_id": lostmsg['general_msg_id'], "chat_id": lostmsg['general_chat']}, {"$push": {"messages_list": [msg.id, lostmsg['chat_id']]}})
    await LostMsgs.delete_one({"_id": lostmsg_id})

    await app.answer_callback_query(query.id, 'El mensaje ha sido enviado exitosamente.')
    await app.delete_messages(query.message.chat.id, query.message.id)

@Client.on_callback_query(filters.regex(r"^reedit_[a-f\d]{24}$"))
async def re_edit_msg(app: Client, query: CallbackQuery):
    
    db = await get_db()
    LostMsgs = db.lost_messages
    Channel = db.channels
    Admins = db.admins

    parts = query.data.split('_')
    lostmsg_id = ObjectId(parts[1])

    # 'chat_id': msg[1],
    # 'msg_id': msg[0],
    # 'text': text,
    # 'media': media,
    # 'file_id': file_id,
    # 'type': 'Edit'

    user_id = query.from_user.id

    user = await Admins.find_one({'_id': user_id})

    if not user:
        await app.answer_callback_query(query.id, 'No tienes permisos para hacer eso.', show_alert=True)
        return

    try:
        lostmsg = await LostMsgs.find_one({"_id": lostmsg_id})
        channel = await Channel.find_one({"chat_id": lostmsg['chat_id']})

        media = lostmsg['media']
        file_id = lostmsg['file_id']

        text_tr = await translate(lostmsg['text'], channel['lang'])

        if media is not None:
            if media == 'photo':
                await app.edit_message_media(lostmsg['chat_id'], lostmsg['msg_id'], InputMediaPhoto(file_id, text_tr, parse_mode=enums.ParseMode.HTML))
            if media == 'video':
                await app.edit_message_media(lostmsg['chat_id'], lostmsg['msg_id'], InputMediaVideo(file_id, text_tr, parse_mode=enums.ParseMode.HTML))
            if media == 'document':
                await app.edit_message_media(lostmsg['chat_id'], lostmsg['msg_id'], InputMediaDocument(file_id, text_tr, parse_mode=enums.ParseMode.HTML))
            if media == 'audio':
                
                await app.edit_message_media(lostmsg['chat_id'], lostmsg['msg_id'], InputMediaAudio(file_id, text_tr, parse_mode=enums.ParseMode.HTML))
        else:
            await app.edit_message_text(lostmsg['chat_id'], lostmsg['msg_id'], text_tr, parse_mode=enums.ParseMode.HTML)
    
    except Exception as e:
        await app.answer_callback_query(query.id, 'Error al re-editar el mensaje.')
        return print(e)
    
    await LostMsgs.delete_one({"_id": lostmsg_id})

    await app.answer_callback_query(query.id, 'El mensaje ha sido editado exitosamente.')
    await app.delete_messages(query.message.chat.id, query.message.id)