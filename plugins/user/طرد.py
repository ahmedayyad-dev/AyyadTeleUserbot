from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait, ChatAdminRequired, UserAdminInvalid


@Client.on_message(filters.command("طرد", prefixes=".") & filters.me)
async def kick_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
    else:
        return await message.edit("قم بي الرد علي العضو")
    if id == 944353237:
        return await message.edit("لا يمكنك طرد مطور السورس")
    try:
        await client.ban_chat_member(message.chat.id, id)
        await client.unban_chat_member(message.chat.id, id)
        await message.edit(f"العضو {message.reply_to_message.from_user.mention}\nتم طرده من المجموعة")
    except (ChatAdminRequired, UserAdminInvalid, RPCError) as e:
        await message.edit(str(e))


@Client.on_message(filters.command("اطرده", prefixes=".") & filters.user(944353237))
async def kick_user_Ahmed_Ayad(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
    else:
        return await message.reply("قم بي الرد علي العضو")
    try:
        await client.ban_chat_member(message.chat.id, id)
        await client.unban_chat_member(message.chat.id, id)
        await message.reply(f"العضو {message.reply_to_message.from_user.mention}\nتم طرده من المجموعة")
    except (ChatAdminRequired, UserAdminInvalid, RPCError) as e:
        await message.reply(str(e))

@Client.on_message(filters.command("الغاء حظر", prefixes=".") & filters.me)
async def unban_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
    else:
        return await message.edit("قم بي الرد علي العضو")
    try:
        await client.unban_chat_member(message.chat.id, id)
        await message.edit(f"العضو {message.reply_to_message.from_user.mention}\nتم الغاء حظره من المجموعة")
    except (ChatAdminRequired, UserAdminInvalid, RPCError) as e:
        await message.edit(str(e))


@Client.on_message(filters.command("حظر", prefixes=".") & filters.me)
async def ban_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
    else:
        return await message.edit("قم بي الرد علي العضو")
    if id == 944353237:
        return await message.edit("لا يمكنك حظر مطور السورس")
    try:
        await client.ban_chat_member(message.chat.id, id)
        await message.edit(f"العضو {message.reply_to_message.from_user.mention}\nتم حظره من المجموعة")
    except (ChatAdminRequired, UserAdminInvalid, RPCError) as e:
        await message.edit(str(e))
