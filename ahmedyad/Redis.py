from pyrogram.filters import create
from pyrogram.types import Message
from redis import Redis

db = Redis(decode_responses=True)


async def mute_user(_, client, m: Message):
    if m.from_user and db.sismember(f'{client.me.id}:mute', m.from_user.id):
        return True


mute = create(mute_user)
