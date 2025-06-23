import time
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # Unique reaction for a welcoming touch
    await message.react("✨") 
    
    # Check for deep links
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            # Send the main help message first
            await message.reply_text(_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard)
            await asyncio.sleep(0.5) # Short delay for effect
            # Then follow up with a sticker
            await message.reply_sticker("CAACAgQAAxkBAAEQI3FlTNu5kQAB30Uj4g7uK67j-QABrjsAAsMNAAIz2sBSj0750wQ-tEszBA") # New sticker
            
        elif name[0:3] == "sud": # Sudoers list deep link
            await sudoers_list(client, message, _)
            return
        
        elif name[0:3] == "inf": # Info deep link
            m = await message.reply_text("🔎 𝙁𝙚𝙩𝙘𝙝𝙞𝙣𝙜 𝙮𝙤𝙪𝙧 𝙞𝙣𝙛𝙤...")
            query = name.replace("info_", "").replace("info", "")
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                published = result["publishedTime"]
                url = result["link"]
                if duration is None:
                    duration = "Unknown"
                key_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="• ᴡᴀᴛᴄʜ •", url=url),
                            InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="close"),
                        ]
                    ]
                )
                await m.edit_text(
                    _["start_6"].format(title, duration, views, published, url, result["channel"]["name"], app.mention),
                    reply_markup=key_markup,
                    disable_web_page_preview=True,
                )
    else:
        # Default private start message for a unique and dynamic intro
        out = private_panel(_)
        
        # Send the main welcome photo with stylized caption first
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.first_name, app.mention), 
            reply_markup=InlineKeyboardMarkup(out),
        )
        await asyncio.sleep(0.7) # A short delay for emphasis
        
        # Follow up with a welcoming sticker to make it more engaging
        await message.reply_sticker("CAACAgQAAxkBAAEQI3FlTNu5kQAB30Uj4g7uK67j-QABrjsAAsMNAAIz2sBSj0750wQ-tEszBA") # New sticker
        
    await message.stop_propagation()

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_grp(client, message: Message, _):
    await add_served_chat(message.chat.id)
    # Corrected reaction emoji from "" to "🚀"
    await message.react("🚀") # Energetic reaction for group start
    try:
        if await is_banned_user(message.from_user.id):
            return await message.reply_text(_["gban_warning"].format(app.mention))

        member = await app.get_chat_member(message.chat.id, app.id)
        if member.status == ChatMemberStatus.LEFT:
            return
        if not member.can_manage_video_chats:
            await message.reply_text(_["general_4"])
            return
    except Exception as ex:
        print(ex)

    # Group start message - concise and informative
    out = start_panel(_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_3"].format( # start_3 is designed for group welcomes in en.yml
            message.from_user.first_name,
            app.mention,
            message.chat.title,
            app.mention,
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await message.stop_propagation()