import asyncio
import os

from patchright.async_api import async_playwright
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("اسكرين", ".") & filters.me)
async def screenshot(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("لم احصل على رابط الموقع")
        return

    url = message.text.split(None, 1)[1]

    out_file = f"screenshot_{message.id}.png"

    try:
        await message.edit("جاري تشغيل المتصفح...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                executable_path="/usr/bin/brave-browser",
                headless=True,
                proxy={
                    "server": "socks5://127.0.0.1:9050",
                    "username": "",
                    "password": "",
                    "bypass": ""
                },
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process'
                ],
            )

            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
            )

            page = await context.new_page()

            await message.edit("جاري تحميل الصفحة...")
            await page.goto(url, wait_until="networkidle", timeout=60000)

            await asyncio.sleep(2)

            await message.edit("جاري التقاط الصورة...")
            await page.screenshot(path=out_file, full_page=True)

            await browser.close()

            await message.edit("جاري الارسال...")
            await message.reply_photo(
                out_file,
                caption=f"رابط الموقع: {url}",
                reply_to_message_id=message.id
            )
            await message.delete()

    except (ValueError, OSError) as e:
        await message.edit(f"حدث خطأ:\n`{str(e)}`")
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)
