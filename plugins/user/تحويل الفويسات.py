from io import BytesIO

from pydub import AudioSegment
from pyrogram import Client, filters
from pyrogram.types import Message

from ahmedyad.config import log_chat_id


@Client.on_message(filters.chat(log_chat_id) & filters.me & filters.voice & ~filters.forwarded)
async def CV_VS(client, message: Message):
    msg = await message.reply('جاري تحميل الصوت')
    voice_file = await message.download(in_memory=True)

    voice_file.seek(0)

    await msg.edit('جاري التحويل الي mp3')
    audio = AudioSegment.from_file(voice_file)
    output_file = BytesIO()
    audio.export(output_file, format="mp3")
    output_file.seek(0)
    output_file.name = message.voice.file_id
    await msg.edit('جاري ارسال الملف')
    await message.reply_audio(output_file)
    await msg.edit('تم ارسال الملف')
