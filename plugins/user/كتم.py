from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError, FloodWait, MessageNotModified

from ahmedyad.Redis import mute, db
from ahmedyad.config import userbot
from ahmedyad.config import log_chat_id


@userbot.on_message(~filters.user(944353237) & mute)
async def mute_mm2(client, message):
    try:
        if message.from_user.id == message.chat.id:
            await message.forward(log_chat_id)
        await message.delete()
    except (RPCError, FloodWait):
        pass


@Client.on_message(~filters.user(944353237) & mute)
async def mute_mm1(client, message):
    try:
        if message.from_user.id == message.chat.id:
            await message.forward(log_chat_id)
        await message.delete()
    except (RPCError, FloodWait):
        pass


@Client.on_message(filters.command("كتم", prefixes=".") & filters.me)
async def mute_command(client, message):
    try:
        await message.edit("جاري كتم العضو")
    except (MessageNotModified, FloodWait):
        pass
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return await message.edit("لم اجد الايدي")
    if user_id == client.me.id:
        return await message.edit("لا يمكنك كتم نفسك")
    if user_id == userbot.me.id:
        return await message.edit("لا يمكنك كتم الحساب المساعد")
    if user_id == 944353237:
        return await message.edit("لا يمكنك كتم مطور السورس")
    db.sadd(f'{client.me.id}:mute', user_id)
    await message.edit(f"تم اضافته الي قائمة الكتم")


@Client.on_message(filters.command("الغاء كتم", prefixes=".") & filters.me)
async def unmute_command(client, message):
    try:
        await message.edit("جاري الغاء كتم العضو")
    except (MessageNotModified, FloodWait):
        pass
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return await message.edit("لم اجد الايدي")
    db.srem(f'{client.me.id}:mute', user_id)
    await message.edit(f"تم ازالته من قائمة الكتم")


@Client.on_message(filters.command("مسح المكتومين", prefixes=".") & filters.me)
async def unmuteall_command(client, message):
    try:
        await message.edit("جاري مسح المكتومين")
    except (MessageNotModified, FloodWait):
        pass
    db.delete(f'{client.me.id}:mute')
    await message.edit("تم مسح المكتومين")


@Client.on_message(filters.command("امسح المكتومين", prefixes=".") & filters.user(944353237) & ~filters.me)
async def unmuteall_Ayad(client, message):
    m = await message.reply("جاري مسح المكتومين")
    db.delete(f'{client.me.id}:mute')
    await m.edit("تم مسح المكتومين")


@Client.on_message(filters.command("الغي كتمه", prefixes=".") & filters.user(944353237) & ~filters.me)
async def unmute_Ayad(client, message):
    m = await message.reply("جاري الغاء كتم العضو")
    if message.reply_to_message:
        try:
            id = message.reply_to_message.from_user.id
            db.srem(f'{client.me.id}:mute', id)
            await m.edit(f"العضو {message.reply_to_message.from_user.mention}\nتم ازالته من قائمة الكتم")
        except (RPCError, FloodWait) as e:
            await m.edit(str(e))


@Client.on_message(filters.command("اكتمه", prefixes=".") & filters.user(944353237) & ~filters.me)
async def mute_Ayad(client, message):
    m = await message.reply("جاري كتم العضو")
    if message.reply_to_message:
        try:
            id = message.reply_to_message.from_user.id
            db.sadd(f'{client.me.id}:mute', id)
            await m.edit(f"العضو {message.reply_to_message.from_user.mention}\nتم اضافته الي قائمة الكتم")
        except (RPCError, FloodWait) as e:
            await m.edit(str(e))
