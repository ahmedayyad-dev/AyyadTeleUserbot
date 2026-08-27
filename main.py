import platform

# set timezone
if platform.system() == 'Linux':
    import os

    os.system('timedatectl set-timezone Africa/Cairo')
else:
    import pytz

    pytz.timezone('Africa/Cairo')

from asyncio import get_event_loop, create_task

from pytgcalls import idle

from pyrogram.errors import RPCError, FloodWait

from ahmedyad.config import UBCall, user, userbot, bot, pyrobot
from ahmedyad.config import log_chat_id
from time import strftime


async def start_userbot():
    await UBCall.start()
    print("تم تشغيل الحساب المساعد بنجاح")
    await userbot.join_chat("ahmedyad200")
    await userbot.join_chat("YYYBR")
    await userbot.join_chat("Dev3yad")
    try:
        await userbot.send_message(log_chat_id, "تم تشغيل الحساب المساعد بنجاح")
    except (RPCError, FloodWait):
        pass


async def start_user():
    await user.start()
    print("تم تشغيل الحساب الاساسي بنجاح")
    await user.join_chat("ahmedyad200")
    await user.join_chat("YYYBR")
    await user.join_chat("Dev3yad")
    try:
        await user.send_message(log_chat_id, "تم تشغيل الحساب الاساسي بنجاح")
    except (RPCError, FloodWait):
        pass


async def start_bot():
    await pyrobot.start()
    print("تم تشغيل البوت بنجاح")
    try:
        await pyrobot.send_message(log_chat_id, "تم تشغيل البوت بنجاح")
    except (RPCError, FloodWait):
        pass


async def main():
    print("جاري تشغيل السورس")
    create_task(start_userbot())
    create_task(start_user())
    create_task(start_bot())
    await bot.send_photo(
        log_chat_id,
        'https://t.me/fuvrs4w/3351',
        f"تم تشغيل البوت الخاص بك\nالوقت الان {strftime('%Y:%m:%d %I:%M:%S %p')}",

    )
    await idle()
    await userbot.stop()
    await user.stop()


get_event_loop().run_until_complete(main())
