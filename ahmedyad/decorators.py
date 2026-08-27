import re

from pyrogram import Client, filters


def parse_chat_target(text):
    match = re.search(r'^(.*) .في -(.*)$', text)
    if match:
        return int(text.split(' .في ', 1)[1]), text.split(' .في ', 1)[0]
    return None, text


def user_cmd(command, private=True):
    f = filters.command(command, ".") & filters.me
    if not private:
        f &= ~filters.private
    return Client.on_message(f)
