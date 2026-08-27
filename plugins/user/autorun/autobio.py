import asyncio
from time import strftime

from pyrogram.errors import FloodWait

from ahmedyad.Redis import db
from ahmedyad.config import user


async def autobio():
    while not await asyncio.sleep(60):
        if bool(db.get(f'{user.me.id}:bio') and not db.get(f'{user.me.id}:copy_user')):
            time = strftime("%I:%M %p")
            bio = db.get(f'{user.me.id}:bio')
            try:
                await user.update_profile(bio=f'{time} | {bio}')
            except FloodWait as e:
                await asyncio.sleep(e.value + 10)


asyncio.create_task(autobio())
