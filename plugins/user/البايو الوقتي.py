from pyrogram import Client, filters

from ahmedyad.Redis import db


@Client.on_message(filters.command("تفعيل البايو الوقتي", prefixes=".") & filters.me)
async def en_bio_time(client, message):
    if db.get(f'{client.me.id}:bio'):
        return await message.edit("البايو الوقتي مفعل")
    await message.edit("جاري تفعيل البايو الوقتي")
    bio = await client.get_chat(client.me.id)
    if not bio.bio:
        bio = "by @YYYBD - @YYYBR"
    else:
        bio = bio.bio
    if not db.get(f'{client.me.id}:bio'):
        db.set(f'{client.me.id}:bio', bio)
    await message.edit("تم تفعيل البايو الوقتي")


@Client.on_message(filters.command("تعطيل البايو الوقتي", prefixes=".") & filters.me)
async def de_bio_time(client, message):
    if not db.get(f'{client.me.id}:bio'):
        return await message.edit("البايو الوقتي غير مفعل")
    await message.edit("جاري تعطيل البايو الوقتي")
    bio = db.get(f'{client.me.id}:bio')
    db.delete(f'{client.me.id}:bio')
    await client.update_profile(bio=bio)
    await message.edit("تم تعطيل البايو الوقتي")
