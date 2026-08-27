from os import execle, environ
from sys import executable

from pyrogram import Client, filters


@Client.on_message(filters.command("اعاده تشغيل", ".") & filters.me)
async def restart(client, message):
    await message.edit("جاري اعاده التشغيل")
    args = [executable, "main.py"]
    execle(executable, *args, environ)
