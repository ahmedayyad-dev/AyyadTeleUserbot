from googletrans import Translator
from pyrogram import Client, filters


@Client.on_message(filters.command("ترجمه", ".") & filters.me)
async def trans(client, message):
    yadl = message.text.split(None, 1)[1]
    yadI = yadl.split(" .الي ", 1)[0]
    yadl = yadl.split(" .الي ", 1)[1]
    await message.edit(f"جاري ترجمه {yadI} الي اللغه {yadl}")
    try:
        translator = Translator(service_urls=['translate.googleapis.com'])
        result = await translator.translate(yadI, dest=yadl)
        await message.edit(result.text)
    except (ValueError, ConnectionError) as e:
        await message.edit(str(e))
