import time
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

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

# --- Premium Sticker IDs ---
WELCOME_STICKERS = [
    "CAACAgUAAxkBAAEQI1RlTLnRAy4h9lOS6jgS5FYsQoruOAAC1gMAAg6ryVcldUr_lhPexzME",
    "CAACAgUAAxkBAAKktGhZgVvKBcruKFO1vrlyJyJ92u0BAAIPCQACSErxVkH9JWQPmfaoHgQ",
    "CAACAgUAAxkBAAKkw2hZgbt8t_FQU38s_k_8RZR3gsIiAAINFgAC0QyQVrqrLQzU13foHgQ",
    "CAACAgUAAxkBAAKkyGhZghOqGIGtgP5HkY1Nyk_vfugyAAJ5CgACQgZwVTVo2eQqCh15HgQ"
]

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # Stylish reaction with random choice
    reactions = ["✨", "🔥", "🎶", "💖", "🥳", "⚡️"]
    await message.react(random.choice(reactions))
    
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_sticker(random.choice(WELCOME_STICKERS))
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✨ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔍")
            query = (str(name)).replace("info_", "", 1)
            query = f"[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=){query}"
            from youtubesearchpython.__future__ import VideosSearch
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"🎵 {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        try:
            out = private_panel(_)
            
            # --- Premium Welcome Animation ---
            welcome_animation = await message.reply_text("🔄")
            
            welcome_phrases = [
                f"✨ 𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 {message.from_user.mention}...",
                f"🌟 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 {app.mention}...",
                f"🎶 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐅𝐨𝐫 𝐘𝐨𝐮...",
                f"💫 𝐋𝐞𝐭'𝐬 𝐑𝐨𝐜𝐤 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭 {message.from_user.mention}...",
                f"🔥 𝐑𝐞𝐚𝐝𝐲 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐒𝐨𝐦𝐞 𝐇𝐢𝐭𝐬..."
            ]
            
            for phrase in welcome_phrases:
                await welcome_animation.edit_text(phrase)
                await asyncio.sleep(0.3)
            
            # --- Dynamic Loading Animation ---
            loading_steps = [
                "⚡️ 𝐈𝐧𝐢𝐭𝐢𝐚𝐥𝐢𝐳𝐢𝐧𝐠...",
                "🎵 𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭𝐬...",
                "💿 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐒𝐞𝐫𝐯𝐞𝐫𝐬...",
                "🚀 𝐀𝐥𝐦𝐨𝐬𝐭 𝐓𝐡𝐞𝐫𝐞...",
                f"✅ 𝐑𝐞𝐚𝐝𝐲 𝐓𝐨 𝐑𝐨𝐜𝐤, {message.from_user.mention}!"
            ]
            
            for step in loading_steps:
                await welcome_animation.edit_text(step)
                await asyncio.sleep(0.4)
            
            # Send random welcome sticker
            await message.reply_sticker(random.choice(WELCOME_STICKERS))
            
            # Get user profile or default image
            userss_photo = None
            if message.chat.photo:
                try:
                    userss_photo = await app.download_media(
                        message.chat.photo.big_file_id,
                    )
                except Exception as e:
                    print(f"Error downloading chat photo: {e}")
                    userss_photo = None
            
            chat_photo = userss_photo if userss_photo else config.START_IMG_URL

        except Exception as e:
            print(f"Error in start command: {e}")
            chat_photo = config.START_IMG_URL

        await welcome_animation.delete()
        
        # Final stylish message with gradient effect emojis
        await message.reply_photo(
            photo=chat_photo,
            caption=f"""
✨ **𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 {app.mention}** ✨

💫 𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 {message.from_user.mention}!
🎶 𝐈'𝐦 𝐀 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐌𝐮𝐬𝐢𝐜 𝐁𝐨𝐭 𝐖𝐢𝐭𝐡 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬!

🔥 𝐏𝐥𝐚𝐲 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐮𝐬𝐢𝐜
🌟 𝟐𝟒/𝟕 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐈𝐧 𝐕𝐂
💞 𝐒𝐮𝐩𝐞𝐫 𝐅𝐚𝐬𝐭 𝐀𝐧𝐝 𝐒𝐦𝐨𝐨𝐭𝐡

𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧𝐬 𝐁𝐞𝐥𝐨𝐰 𝐓𝐨 𝐄𝐱𝐩𝐥𝐨𝐫𝐞 𝐌𝐲 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬!
            """,
            reply_markup=InlineKeyboardMarkup(out),
        )
        
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"""
🌟 𝐍𝐞𝐰 𝐔𝐬𝐞𝐫 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐨𝐭 🌟

💫 𝐔𝐬𝐞𝐫: {message.from_user.mention}
🆔 𝐈𝐃: <code>{sender_id}</code>
📛 𝐍𝐚𝐦𝐞: {sender_name}
                """,
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    
    # Group start with stylish design
    m = await message.reply_text("🚀")
    await asyncio.sleep(0.5)
    await m.delete()
    
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"""
🎵 **{app.mention} 𝐈𝐬 𝐀𝐥𝐢𝐯𝐞 𝐀𝐧𝐝 𝐑𝐞𝐚𝐝𝐲!** 🎶

⏳ 𝐔𝐩𝐭𝐢𝐦𝐞: {get_readable_time(uptime)}
💫 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: {config.MUSIC_BOT_NAME}

✨ 𝐔𝐬𝐞 𝐌𝐞 𝐈𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐅𝐨𝐫 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐮𝐬𝐢𝐜!
        """,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"[https://t.me/](https://t.me/){app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                m = await message.reply_text("🎵")
                await asyncio.sleep(0.5)
                await m.delete()
                
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=f"""
🌟 **𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐀𝐝𝐝𝐢𝐧𝐠 𝐌𝐞 𝐈𝐧 {message.chat.title}!** ✨

💫 𝐈'𝐦 {app.mention}, 𝐀 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐌𝐮𝐬𝐢𝐜 𝐁𝐨𝐭!
🎶 𝐏𝐥𝐚𝐲 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐮𝐬𝐢𝐜 𝐈𝐧 𝐕𝐂

🔥 𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐮𝐭𝐭𝐨𝐧𝐬 𝐁𝐞𝐥𝐨𝐰 𝐓𝐨 𝐆𝐞𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝!
                    """,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)