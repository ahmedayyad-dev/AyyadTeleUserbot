from pyrogram import Client, filters

from ahmedyad.Redis import db


@Client.on_message(filters.command("انتحال", ".") & filters.me)
async def copy_user(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
    else:
        return await message.edit("قم بي الرد علي العضو")
    await message.edit("جاري انتحاله")
    if not db.get(f'{client.me.id}:copy_user'):
        me_info = await client.get_chat(client.me.id)
        db.set(f'{client.me.id}:copy_user', '3yad')
        db.set(f'{client.me.id}:copy_user:first_name', me_info.first_name)
        if me_info.bio:
            bio = me_info.bio
            if db.get(f'{client.me.id}:bio'):
                bio = db.get(f'{client.me.id}:bio')
            db.set(f'{client.me.id}:copy_user:bio', bio)
        if me_info.last_name:
            db.set(f'{client.me.id}:copy_user:last_name', me_info.last_name)
    us_info = await client.get_chat(id)
    await client.update_profile(first_name=us_info.first_name)
    if us_info.bio:
        await client.update_profile(bio=us_info.bio)
    else:
        await client.update_profile(bio="")
    if us_info.last_name:
        await client.update_profile(last_name=us_info.last_name)
    else:
        await client.update_profile(last_name="")
    await message.edit("تم الانتحال")


@Client.on_message(filters.command("رجوع", ".") & filters.me)
async def uncopy_user(client, message):
    if not db.get(f'{client.me.id}:copy_user'):
        return await message.edit("لم تقم بانتحال احد")
    await message.edit("جاري الرجوع الي الاعدادات الافتراضيه")
    first_name = db.get(f'{client.me.id}:copy_user:first_name')
    last_name = db.get(f'{client.me.id}:copy_user:last_name')
    bio = db.get(f'{client.me.id}:copy_user:bio')
    db.delete(f'{client.me.id}:copy_user')
    await client.update_profile(first_name=first_name)
    if bio:
        await client.update_profile(bio=bio)
    else:
        await client.update_profile(bio="")
    if last_name:
        await client.update_profile(last_name=last_name)
    else:
        await client.update_profile(last_name="")
    await message.edit("تم الرجوع الي الاعدادات الافتراضيه")
