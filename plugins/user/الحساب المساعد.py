import re

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, RPCError, FloodWait, ChatAdminRequired

from ahmedyad.config import userbot


@Client.on_message(filters.command("انضم", ".") & filters.me & ~filters.private)
async def ub_join(client, message):
    if re.search(r'^(.*) .الي (.*)$', message.text):
        invite = message.text.split(' .الي ', 1)[1]
    else:
        if message.chat.username:
            invite = message.chat.username
        else:
            try:
                invite = await client.export_chat_invite_link(message.chat.id)
            except (RPCError, FloodWait, ChatAdminRequired) as e:
                await message.edit(f"لم استطيع دعوة الحساب المساعد انتظر جاري اضافته\n\n{e}")
                try:
                    gub = await userbot.get_me()
                    gme = await client.get_me()
                    await userbot.add_contact(gme.username, gme.first_name)
                    await client.add_contact(gub.username, gub.first_name)
                    await client.add_chat_members(message.chat.id, gub.id)
                    return await message.edit("تم اضافة الحساب المساعد بنجاح")
                except (RPCError, FloodWait) as e:
                    return await message.edit(str(e))
    try:
        await userbot.join_chat(invite)
        await message.edit("تم دخول الحساب المساعد بنجاح")
    except UserAlreadyParticipant:
        await message.edit("الحساب المساعد بالفعل في الدردشة الخاصة بك")
    except (RPCError, FloodWait) as e:
        await message.edit(f"خطأ : {e}")


@Client.on_message(filters.command("غادر", ".") & filters.me)
async def ub_leave(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = message.text.split(None, 1)[1]
    await userbot.leave_chat(chat_id)
    await message.edit("قام الحساب المساعد بالخروج من المحادثة")
