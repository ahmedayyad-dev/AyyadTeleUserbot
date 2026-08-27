from pyrogram import Client, filters
from pyrogram.enums import ChatType

from ahmedyad.config import log_chat_id


@Client.on_message(filters.command("ملكياتي", prefixes=".") & filters.me)
async def get_owned_groups(client, message):
    await message.edit("جاري جمع الملكيات")
    is_creator_list = "قائمه الملكيات\n"
    n = 0
    msg = await client.send_message(log_chat_id, "جاري جمع الملكيات")
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if dialog.chat.id < 0 and dialog.chat.is_creator:
            n += 1
            await message.edit(f"تم جمع {n} ملكيات\n" + "تم ارسالهم الي مجموعه السجل")
            await msg.edit(f"تم جمع {n} ملكيات\n" + is_creator_list)
            is_creator_list += f"{'-' * 35} {n}-\n"
            is_creator_list += f"الاسم :{chat.title}\n"
            is_creator_list += f"الايدي :{chat.id}\n"
            is_creator_list += f"النوع : {'قناه' if chat.type == ChatType.CHANNEL else 'جروب'}\n"
            is_creator_list += f"يوزر : {chat.username}\n"
            invite_link = (await client.get_chat(chat.id)).invite_link
            is_creator_list += f"اللينك : {invite_link}\n"

    await message.edit(is_creator_list)
