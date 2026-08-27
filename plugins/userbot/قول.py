import re

from pyrogram import Client, filters
from pyrogram.types import ReplyParameters

from ahmedyad.config import user


@Client.on_message(filters.command("قول", ".") & filters.me)
async def echo(client, message):
    await user.delete_messages(message.chat.id, message.id)
    text = message.text.split('.قول ', 1)[1]
    yad = None
    if re.search(r'^(.*) .في (.*)$', text):
        text2 = text.split(' .في ', 1)[1]
        text = text.split(' .في ', 1)[0]
        if re.search(r'^(.*) .ريب (.*)$', text2):
            chat_id = int(text2.split(' .ريب ', 1)[0])
            yad = int(text2.split(' .ريب ', 1)[1])
        else:
            chat_id = int(text2)
    else:
        chat_id = message.chat.id
        if message.reply_to_message:
            yad = message.reply_to_message.id
    await client.send_message(
        chat_id=chat_id,
        text=text,
        reply_parameters=ReplyParameters(message_id=yad),
    )
