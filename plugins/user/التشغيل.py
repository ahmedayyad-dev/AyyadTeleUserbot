from ayyad_apis import TubeRelayAPI
from ayyad_apis.utils import DownloadError, RequestError, ClientError, InvalidInputError
from pyrogram import Client, filters
from pyrogram.errors import RPCError, FloodWait
from pyrogram.types import Message
from py_yt import VideosSearch

from ahmedyad.config import UBCall, tube_relay_key
from ahmedyad.decorators import parse_chat_target, user_cmd
from ahmedyad.handlers import skip_current_song, skip_item
from ahmedyad.queues import QUEUE, add_to_queue, clear_queue

from pytgcalls.exceptions import (
    NoActiveGroupCall, CallDeclined, CallBusy,
    NoVideoSourceFound, NoAudioSourceFound, NotInCallError
)


def is_url(text):
    return text.startswith("http://") or text.startswith("https://")


@user_cmd("تشغيل", private=False)
async def play(client, m: Message):
    chat_id, text = parse_chat_target(m.text)
    if chat_id is None:
        chat_id = m.chat.id

    video_mode = "فيديو" in text
    text = text.replace("فيديو", "").strip()

    replied = m.reply_to_message
    if replied:
        if replied.audio or replied.voice:
            await m.edit("جاري التحميل")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                songname = (replied.audio.title or replied.audio.file_name or "Audio")[:35]
            else:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await m.edit(f"تم الاضافة الى القائمة دور {pos}")
            else:
                try:
                    await UBCall.play(chat_id, dl)
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await m.edit("جاري التشغيل")
                except (NoActiveGroupCall, CallDeclined, CallBusy, RPCError, FloodWait) as e:
                    await m.edit(str(e))
        elif replied.video or replied.document:
            await m.edit("جاري التحميل")
            dl = await replied.download()
            link = replied.link
            if replied.video:
                songname = (replied.video.file_name or "Video")[:35]
            elif replied.document:
                songname = (replied.document.file_name or "Video")[:35]
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", 0)
                await m.edit(f"تم الاضافة الى القائمة دور {pos}")
            else:
                try:
                    await UBCall.play(chat_id, dl)
                    add_to_queue(chat_id, songname, dl, link, "Video", 0)
                    await m.edit("جاري التشغيل")
                except (NoVideoSourceFound, NoActiveGroupCall, CallDeclined, RPCError, FloodWait) as e:
                    await m.edit(str(e))
    else:
        if len(m.command) < 2:
            await m.edit("الرد على ملف صوتي/فيديو أو اعطائي رابط أو شيء للبحث")
            return
        query = text.split(None, 1)[1] if len(text.split(None, 1)) > 1 else ""
        if not query:
            await m.edit("الرد على ملف صوتي/فيديو أو اعطائي رابط أو شيء للبحث")
            return

        if is_url(query):
            await m.edit("جاري التحميل")
            try:
                async with TubeRelayAPI(api_key=tube_relay_key) as api:
                    ytlink = api.stream(query, type="video" if video_mode else "audio", quality="best")
            except (InvalidInputError, RequestError, ClientError) as e:
                return await m.edit(f"خطأ في الجلب : {e}")
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Link", ytlink, query, "Video" if video_mode else "Audio", 0)
                await m.edit(f"تم الاضافة الى القائمة دور {pos}")
            else:
                try:
                    await UBCall.play(chat_id, ytlink)
                    add_to_queue(chat_id, "Link", ytlink, query, "Video" if video_mode else "Audio", 0)
                    await m.edit("جاري التشغيل")
                except (NoActiveGroupCall, CallDeclined, CallBusy, RPCError, FloodWait) as e:
                    await m.edit(str(e))
        else:
            await m.edit("جاري البحث")
            search = VideosSearch(query, limit=1)
            res = await search.next()
            data = res["result"][0]
            songname = data["title"][:35]
            await m.edit("جاري التحميل")
            try:
                async with TubeRelayAPI(api_key=tube_relay_key) as api:
                    ytlink = api.stream(data["id"], type="video" if video_mode else "audio", quality="best")
            except (InvalidInputError, RequestError, ClientError) as e:
                return await m.edit(f"خطأ في الجلب : {e}")
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, data["link"], "Video" if video_mode else "Audio", 0)
                await m.edit(f"تم الاضافة الى القائمة دور {pos}")
            else:
                try:
                    await UBCall.play(chat_id, ytlink)
                    add_to_queue(chat_id, songname, ytlink, data["link"], "Video" if video_mode else "Audio", 0)
                    await m.edit("جاري التشغيل")
                except (NoActiveGroupCall, CallDeclined, CallBusy, RPCError, FloodWait) as e:
                    await m.edit(str(e))


@user_cmd("تخطي", private=False)
async def skip(client, m: Message):
    chat_id, text = parse_chat_target(m.text)
    if chat_id is None:
        chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.edit("قائمة التشغيل فارغة")
        elif op == 1:
            await m.edit("قائمة التشغيل فارغة ، مغادرة الدردشة الصوتية")
        else:
            await m.edit(
                f"التشغيل الان : [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = text.split(None, 1)[1]
        OP = "تمت إزالة الأغاني التالية من قائمة الانتظار : "
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split("") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"#{x} - {hm}"
            await m.edit(OP)


@user_cmd(["انهاء", "ايقاف"], private=False)
async def stop(client, m: Message):
    chat_id, _ = parse_chat_target(m.text)
    if chat_id is None:
        chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await UBCall.leave_call(chat_id)
            clear_queue(chat_id)
            await m.edit("تم ايقاف التشغيل بنجاح")
        except (NotInCallError, RPCError, FloodWait) as e:
            await m.edit(str(e))
    else:
        await m.edit("لا اقوم بتشغيل موسيقي")


@user_cmd("توقف", private=False)
async def pause(client, m: Message):
    chat_id, _ = parse_chat_target(m.text)
    if chat_id is None:
        chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await UBCall.pause_stream(chat_id)
            await m.edit("تم إيقاف التشغيل مؤقتا")
        except (NotInCallError, NoActiveGroupCall, RPCError, FloodWait) as e:
            await m.edit(str(e))
    else:
        await m.edit("لا اقوم بتشغيل شيئ")


@user_cmd("استئناف", private=False)
async def resume(client, m: Message):
    chat_id, _ = parse_chat_target(m.text)
    if chat_id is None:
        chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await UBCall.resume_stream(chat_id)
            await m.edit("استئناف التشغيل")
        except (NotInCallError, NoActiveGroupCall, RPCError, FloodWait) as e:
            await m.edit(str(e))
    else:
        await m.edit("لا يوجد موسيقي متوقفة")
