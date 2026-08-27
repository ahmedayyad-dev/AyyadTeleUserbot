from re import match

from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait
from pyrogram.types import ReplyParameters


async def FSendSticker(client, message, ahmed):
    reply_id = message.reply_to_message.id if message.reply_to_message else None
    try:
        await client.send_sticker(
            message.chat.id, ahmed,
            reply_parameters=ReplyParameters(message_id=reply_id)
        )
        await message.delete()
    except (RPCError, FloodWait) as e:
        await message.edit(f"✗ خطأ: {str(e)}")


@Client.on_message(filters.command("طرطر", ".") & filters.me)
async def AyadP1(client, message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == 944353237:
            return await message.edit("لا يمكنك الطرطره علي مطور السورس")
    await FSendSticker(client, message, 'https://t.me/fuvrs4w/3352')


@Client.on_message(filters.command("ممم", ".") & filters.me)
async def AyadP2(client, message):
    await FSendSticker(client, message, 'https://t.me/fuvrs4w/3359')


@Client.on_message(filters.command("ههه", ".") & filters.me)
async def AyadP3(client, message):
    await FSendSticker(client, message, 'https://t.me/fuvrs4w/3360')


@Client.on_message(filters.command(["اشطه", "اشطا"], ".") & filters.me)
async def AyadP4(client, message):
    await FSendSticker(client, message, 'https://t.me/fuvrs4w/3361')


@Client.on_message(filters.regex(r"^\.(\d+) جنيه$") & filters.me)
async def AyadP2(client, message):
    m = match(r"^\.(\d+) جنيه$", message.text)
    if not m:
        return
    sticker_map = {5: 3353, 10: 3354, 20: 3355, 50: 3356, 100: 3357, 200: 3358}

    if t in sticker_map:
        await FSendSticker(client, message, f"https://t.me/fuvrs4w/{sticker_map[int(m.group(1))]}")
    else:
        await message.edit(f"الرقم {t} مش موجود")
