from pyrogram import Client, filters

from ahmedyad.config import user


@Client.on_message(filters.private)
async def hello(client, message):
    await message.reply(f"عذرا هذا البوت خاص بحساب المطور {user.me.username} ولم يفيدك في اي شيئ")