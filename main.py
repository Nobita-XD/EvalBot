from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import pytgcalls

import os
import re
import sys
import subprocess
import traceback

from time import time
from io import StringIO
from inspect import getfullargspec
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

sudo = [5245342013,5573665287,5325855468]


bot = Client(
    "eval Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)
   

app = Client(os.environ["SESSION_NAME"], int(os.environ["API_ID"]), os.environ["API_HASH"])

LOG = int(os.environ.get("LOG"))
DB = os.environ.get("DB")
mongo_client = MongoClient(DB)
db = mongo_client.abhi

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
    
@bot.on_message(filters.command(["eval"], [".", "/", "!"]) & filters.user(sudo))
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="» Give a command to execute")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "SUCCESS"
    final_output = f"`OUTPUT:`\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳", callback_data=f"runtime {t2-t1} seconds"
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"INPUT:\n{cmd[0:980]}\n\nOUTPUT:\nattached document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} seconds",
                    )
                ]
           ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)




@bot.on_message(filters.command(["hi"], [".", "/", "!"]) & filters.user(sudo))
async def hmm(client, message):
 await message.reply_text("hmm")


bot.run()
 
