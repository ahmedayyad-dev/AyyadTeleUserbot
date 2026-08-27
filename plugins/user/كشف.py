from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait, PeerIdInvalid, UsernameNotOccupied
from pyrogram.types import Message

from ahmedyad.config import user, userbot


@Client.on_message(filters.command("كشف", ".") & filters.me)
async def kashf(client, message: Message):
    if len(message.command) < 2:
        if message.reply_to_message.from_user.id:
            user_id = message.reply_to_message.from_user.id
        else:
            return await message.edit("لم تعطني ايدي الشخص")
    else:
        user_id = message.text.split(None, 1)[1]
    try:
        try:
            info = await user.get_chat(user_id)
        except (RPCError, PeerIdInvalid, UsernameNotOccupied):
            try:
                info = await userbot.get_chat(user_id)
            except (RPCError, PeerIdInvalid, UsernameNotOccupied):
                return await message.edit("لم اجد معلوماته")
        if info.last_name:
            name = f"{info.first_name} {info.last_name}"
        elif info.title:
            name = info.title
        else:
            name = info.first_name
        if info.username:
            username = f"@{info.username}"
        else:
            username = "لا يوجد"
        if info.bio:
            bio = info.bio
        elif info.description:
            bio = info.description
        else:
            bio = "لا يوجد"
        text = f"اليك المعلومات\nرابط الشات : <a href='tg://user?user_id={info.id}'>{name}</a>\nالاسم : {name}\nالايدي : {info.id}\nالمعرف : {username}\nالبايو : {bio}"
    except (RPCError, FloodWait, AttributeError) as e:
        text = f"لم اجد معلوماته\n{e}"
    await message.edit(text)
