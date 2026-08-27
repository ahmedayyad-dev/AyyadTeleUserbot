from os import execle, environ
from subprocess import run, CalledProcessError
from sys import executable

from pyrogram import Client, filters


@Client.on_message(filters.command("تحديث", ".") & filters.me)
async def update(client, message):
    await message.edit("جاري التحديث")
    try:
        done = run(["git", "pull"], capture_output=True, text=True)
        if done.returncode != 0:
            return await message.edit(f"✗ فشل سحب التحديثات:\n<code>{done.stderr.strip()}</code>")

        synced = run(["uv", "sync"], capture_output=True, text=True)
        if synced.returncode != 0:
            return await message.edit(f"✗ فشل uv sync:\n<code>{synced.stderr.strip()}</code>")
    except (CalledProcessError, OSError) as e:
        return await message.edit(f"✗ خطأ: {e}")

    await message.edit("✓ تم التحديث، جاري اعاده التشغيل")
    args = [executable, "main.py"]
    execle(executable, *args, environ)
