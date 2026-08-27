import os

from pyrogram import Client, filters

from ahmedyad.config import log_chat_id


@Client.on_message(filters.command("حفظ الرساله", ".") & filters.me)
async def save_message(client, message):
    await message.edit('جاري حفظ الرساله')
    chat = message.command[1]
    msg = int(message.command[2])
    try:
        get = await client.get_messages(chat, msg)
    except (RPCError, FloodWait, ValueError):
        return await message.edit('لم اجد الرساله')
    if get.media:
        a = await get.download()
        await client.send_document(log_chat_id, a)
        os.remove(a)
    else:
        await get.copy(log_chat_id)
    await message.edit('تم حفظ الرساله في مجموعه السجل')
