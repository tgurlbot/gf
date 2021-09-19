# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/GoFile-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from gofile import uploadFile


DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

Bot = Client(
    "GoFile-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}, \n\n`Iam A Simple Gofiles Uploader Bot. Send Me Any File Or Media To Get` __gofile.io__ `Stream Link`\n\n**Made With ❤ BY @BX_Botz**",
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    try:
        message = await update.reply_text(
            text="**UploadinG 📤**",
            quote=True,
            disable_web_page_preview=True
        )
        await update.download()
        response = uploadFile(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        await update.reply_text(
            text=f"Error :- <code>{error}</code>",
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink']}`" + "\n"
    text += f"**Info:** `{response['info']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🔹Open Link🔹", url=response['directLink']),
                InlineKeyboardButton(text="📤 Share Link 📤", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(text="Updates Channel", url="https://telegram.me/BX_Botz")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "close":
        await update.message.delete()

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="🤖 Update Channel", url="https://t.me/BX_Botz"),
        InlineKeyboardButton(text="🎨 Support Group", url="https://t.me/BXSUPPORT")
        ],[
        InlineKeyboardButton(text="🧩 Other Bots", url="https://t.me/BX_Botz/"),
        InlineKeyboardButton(text="Close 🔒", callback_data="close")
    )


Bot.run()
