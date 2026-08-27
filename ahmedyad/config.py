from os import environ

from dotenv import load_dotenv
from pyrogram import Client, enums
from pytgcalls import PyTgCalls
from telebot.async_telebot import AsyncTeleBot

load_dotenv(".env")

SESSION1 = environ["SESSION1"]
SESSION2 = environ["SESSION2"]
api_id = int(environ["api_id"])
api_hash = environ["api_hash"]
log_chat_id = int(environ["chat_id"])
tube_relay_key = environ["tube_relay_key"]
bot_token = environ["bot_token"]

version = '2.3.7'
user = Client(
    'user_account',
    api_id,
    api_hash,
    f'AyyadTeleUserBot {version}',
    'MainUser device', version,
    session_string=SESSION1,
    plugins=dict(root="plugins/user"),
    parse_mode=enums.ParseMode.HTML,
)

userbot = Client(
    'userbot_account',
    api_id,
    api_hash,
    f'AyyadTeleUserBot {version}',
    'BotUser device', version,
    session_string=SESSION2,
    plugins=dict(root="plugins/userbot"),
    parse_mode=enums.ParseMode.HTML,
)

pyrobot = Client(
    'pyrobot',
    api_id,
    api_hash,
    f'AyyadTeleUserBot {version}',
    'BotUser device', version,
    bot_token=bot_token,
    plugins=dict(root="plugins/bot"),
    parse_mode=enums.ParseMode.HTML,
    in_memory=True
)

UBCall = PyTgCalls(userbot)
bot = AsyncTeleBot(bot_token)
