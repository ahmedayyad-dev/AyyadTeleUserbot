import io

from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait
from pyrogram.raw import functions, types
from pyrogram.types import Message


@Client.on_message(filters.command("تيست", prefixes=".") & filters.user([944353237, 'me']))
async def TestBotForMe(client, message):
    await message.reply("انا اعمل الان")


@Client.on_message(filters.command("ايدي", ".") & filters.me)
async def get_me_info(client: Client, message: Message):
    lines = []
    lines.append("┌─────────────────────────────┐")
    lines.append("│         معلومات الرسالة      │")
    lines.append("├─────────────────────────────┤")
    lines.append(f"│ ايديك       : <code>{message.from_user.id}</code>")
    lines.append(f"│ ايدي الرسالة: <code>{message.id}</code>")
    lines.append(f"│ ايدي الشات  : <code>{message.chat.id}</code>")

    media = message.audio or message.video or message.voice or message.document or message.photo or message.sticker
    if media:
        file_id = message.photo.file_id if message.photo else media.file_id
        lines.append(f"│ ايدي الميديا: <code>{file_id}</code>")

    lines.append("└─────────────────────────────┘")

    if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
        lines.append("┌─────────────────────────────┐")
        lines.append("│       معلومات الرد          │")
        lines.append("├─────────────────────────────┤")
        lines.append(f"│ ايدي المردود عليه: <code>{user_id}</code>")
        lines.append(f"│ ايدي رسالة الرد  : <code>{reply.id}</code>")
        reply_media = reply.audio or reply.video or reply.voice or reply.document or reply.photo or reply.sticker
        if reply_media:
            r_file_id = reply.photo.file_id if reply.photo else reply_media.file_id
            lines.append(f"│ ايدي ميديا الرد  : <code>{r_file_id}</code>")
        lines.append("└─────────────────────────────┘")

    if message.forward_from or message.forward_from_chat:
        f_id = message.forward_from.id if message.forward_from else message.forward_from_chat.id
        lines.append("┌─────────────────────────────┐")
        lines.append("│       معلومات الريبوست      │")
        lines.append("├─────────────────────────────┤")
        lines.append(f"│ ايدي المصدر: <code>{f_id}</code>")
        lines.append("└─────────────────────────────┘")

    await message.edit("\n".join(lines), parse_mode="html")


@Client.on_message(filters.command("ابديت", ".") & filters.me)
async def get_raw_update_file(client: Client, message: Message):
    target_msg_id = message.reply_to_message_id if message.reply_to_message_id else message.id
    try:
        peer = await client.resolve_peer(message.chat.id)
        if isinstance(peer, (types.InputPeerChannel, types.InputPeerChannelFromMessage)):
            raw_result = await client.invoke(
                functions.channels.GetMessages(
                    channel=peer,
                    id=[types.InputMessageID(id=target_msg_id)]
                )
            )
        else:
            raw_result = await client.invoke(
                functions.messages.GetMessages(
                    id=[types.InputMessageID(id=target_msg_id)]
                )
            )
        raw_text = str(raw_result)
        with io.BytesIO(raw_text.encode('utf-8')) as out_file:
            out_file.name = "raw_update.txt"
            await message.reply_document(out_file)
    except (RPCError, FloodWait) as e:
        await message.reply_text(f"**حدث خطأ أثناء جلب الـ Raw Update:**\n`{e}`")
