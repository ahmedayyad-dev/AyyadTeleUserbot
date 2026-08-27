from ayyad_apis import TubeRelayAPI
from ayyad_apis.utils import DownloadError, RequestError, ClientError, InvalidInputError
from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait
from pyrogram.types import Message, ReplyParameters
from py_yt import VideosSearch

from ahmedyad.config import tube_relay_key
from ahmedyad.decorators import user_cmd


@user_cmd("تحميل")
async def download(client, m: Message):
    text = m.text.split(None, 1)[1] if len(m.command) > 1 else ""
    video_mode = "فيديو" in text
    text = text.replace("فيديو", "").strip()

    if not text and m.reply_to_message:
        yad = m.reply_to_message.id
    else:
        yad = None

    if not text:
        await m.edit("عطيني اسم اغنية او رابط")
        return

    await m.edit("جاري البحث")
    search = VideosSearch(text, limit=1)
    res = await search.next()
    video_id = res["result"][0]["id"]

    await m.edit("جاري التحميل")
    file_path = f"/tmp/{video_id}.{'mp4' if video_mode else 'm4a'}"
    try:
        async with TubeRelayAPI(api_key=tube_relay_key) as api:
            await api.download(video_id, file_path, type="video" if video_mode else "audio")
    except (DownloadError, InvalidInputError, RequestError, ClientError, OSError) as e:
        return await m.edit(f"خطأ في التحميل : {e}")

    await m.edit("جاري الرفع")
    try:
        if video_mode:
            await m.reply_video(file_path, reply_parameters=ReplyParameters(message_id=yad))
        else:
            await m.reply_audio(file_path, reply_parameters=ReplyParameters(message_id=yad))
        await m.delete()
    except (RPCError, FloodWait) as e:
        await m.edit(f"حدث خطأ\n{e}")
