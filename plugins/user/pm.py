from pyrogram import Client, filters
from pyrogram.enums import ChatType, MessageOriginType
from pyrogram.errors import RPCError, FloodWait, MessageIdInvalid
from pyrogram.types import ReplyParameters, Message

from ahmedyad.config import userbot
from ahmedyad.config import log_chat_id


@Client.on_message(filters.private & ~filters.user(777000) & ~filters.bot, 1)
async def PM_Private(client, message: Message):
    if message.chat.type != ChatType.BOT:
        try:
            msg = await message.forward(log_chat_id)
            if not msg.forward_origin.type == MessageOriginType.HIDDEN_USER:
                return
        except (RPCError, FloodWait, MessageIdInvalid):
            msg = await message.copy(log_chat_id)
        await userbot.send_message(
            log_chat_id,
            f"تم حفظ هذه الرساله من المحادثه التاليه :\n"
            f"الاسم : {message.from_user.full_name}\n"
            f"الايدي : {message.from_user.id}\n"
            f"المعرف : @{message.from_user.username}\n"
            f"منشن : {message.from_user.mention}\n"
            f"الرساله : tg://openmessage?user_id={message.chat.id}&message_id={message.id}",
            reply_parameters=ReplyParameters(message_id=msg.id),
            disable_notification=True,
        )
