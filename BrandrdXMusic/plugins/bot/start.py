import time
import asyncio
import random
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

# █▀▀ █▀█ █▄░█ █▀▀ █ █▄░█ █▀▀   █▀▀ █░█ ▄▀█ █▀█ █▀▀ █▀▄▀█
# █▄▄ █▄█ █░▀█ █▄▄ █ █░▀█ █▄█   █▄▄ █▀█ █▀█ █▀▄ ██▄ █░▀░█

# ✧✧✧ PREMIUM ASSETS ✧✧✧
# **IMPORTANT**: Verify these sticker file IDs are still valid.
# If stickers are not showing, re-obtain valid file IDs via @StickerIDbot
ULTRA_STICKERS = [
    "CAACAgUAAxkBAAEMMtRlqZcq9QABHlK3QZogv6bQeHwz6gAC1gMAAg6ryVcldUr_lhPexzME",  # Animated music note
    "CAACAgUAAxkBAAEMMtZlqZczVXHfD3LJ1J0Jb3QZJgAB2isAAhYJAAJOi_lVvZv3yP4bQHQeBA",  # DJ animation
    "CAACAgUAAxkBAAEMMthlqZdC6WkAAb7X8hq5XQABmQABP_4AAjQKAAJW7ehVvW4AAUv7VQABHwQ",  # Equalizer
    "CAACAgUAAxkBAAEMMtplqZdQZ0zqJk5XQABmQABP_4AAjQKAAJW7ehVvW4AAUv7VQABHwQ"  # Fireworks
]

NEON_GRADIENTS = [
    "🟣🔵🟢🟡🟠🔴",
    "🔴🟠🟡🟢🔵🟣",
    "✨🌟💫🔥🎶⚡️",
    "⚡️🎶🔥💫🌟✨"
]

# Updated MUSIC_EMOJIS with commonly supported Telegram reactions
# A comprehensive list of supported reactions can be found in Telegram's API documentation or by testing
# These are commonly known to work
MUSIC_EMOJIS = ["👍", "❤️", "😂", "🥳", "🙏", "🤩", "🎉", "🔥", "💯", "🥰", "👏", "😁"]

# ✧✧✧ ANIMATION SEQUENCES ✧✧✧
def generate_loading_bar(progress):
    bar_length = 10
    filled = int(round(bar_length * progress / 100))
    return "█" * filled + "░" * (bar_length - filled)

async def neon_text_animation(message, text):
    anim = await message.reply_text("✨")
    for gradient in NEON_GRADIENTS:
        await anim.edit_text(f"{gradient}\n{text}\n{gradient[::-1]}")
        await asyncio.sleep(0.35) # Increased from 0.15 for slower animation
    return anim

async def music_visualizer(message):
    anim = await message.reply_text("🎵")
    for i in range(1, 6):
        await anim.edit_text("\n".join(["|"*i*2 for _ in range(3)]))
        await asyncio.sleep(0.25) # Increased from 0.1 for slower animation
    return anim

# █▀ █▀▀ █▀█ █▀▀ █▀▀ █▄░█ █▀ █░█ █▀█ ▀█▀
# ▄█ █▄▄ █▀▄ ██▄ ██▄ █░▀█ ▄█ █▀█ █▄█ ░█░

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def ultra_start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # ✧ ULTRA REACTION ANIMATION ✧
    valid_reactions = ["👍", "❤️", "😂", "🥳", "🤩", "🎉", "🔥", "💯", "🥰"] 
    
    if len(valid_reactions) >= 3:
        for emoji in random.sample(valid_reactions, 3):
            try:
                await message.react(emoji)
                await asyncio.sleep(0.4) # Increased from 0.2 for slower reaction
            except Exception as e:
                print(f"Failed to react with {emoji}: {e}")
    else:
        try:
            await message.react("👍")
        except Exception as e:
            print(f"Failed to react with default 👍: {e}")

    # Logger notification for private start
    if config.LOGGER_ID:
        try:
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"""
╔════════════════════╗
       🌟 𝐍𝐄𝐖 𝐔𝐒𝐄𝐑 🌟
╠════════════════════╣
👤 𝐔𝐬𝐞𝐫: {message.from_user.mention}
🆔 𝐈𝐃: <code>{message.from_user.id}</code>
📛 𝐔𝐧: @{message.from_user.username}
⏰ 𝐓𝐢𝐦𝐞: {time.strftime('%X')}
╚════════════════════╝
                """
            )
        except Exception as e:
            print(f"Failed to send start notification to LOGGER_ID: {e}")

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            # ✧ HELP COMMAND ANIMATION ✧
            keyboard = help_pannel(_)
            anim = await neon_text_animation(message, "𝐇𝐄𝐋𝐏 𝐂𝐄𝐍𝐓𝐄𝐑")
            
            try:
                await message.reply_sticker(random.choice(ULTRA_STICKERS))
            except Exception as e:
                print(f"Failed to send sticker for help command: {e}")
            
            for i in range(0, 101, 10):
                await anim.edit_text(f"✨ 𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮 ✨\n{generate_loading_bar(i)} {i}%")
                await asyncio.sleep(0.2) # Increased from 0.1 for slower loading bar
            
            await anim.delete()
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
            
        if name[0:3] == "sud":
            # ✧ SUDO ACCESS ANIMATION ✧
            anim = await message.reply_text("🔐")
            await asyncio.sleep(0.8) # Increased from 0.5
            for i in range(3):
                await anim.edit_text("🔐" + "•"*(i+1))
                await asyncio.sleep(0.5) # Increased from 0.3
            
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"""
╔════════════════════╗
       🔐 𝐒𝐔𝐃𝐎 𝐀𝐂𝐂𝐄𝐒𝐒 🔐
╠════════════════════╣
👤 𝐔𝐬𝐞𝐫: {message.from_user.mention}
🆔 𝐈𝐃: <code>{message.from_user.id}</code>
📛 𝐔𝐧: @{message.from_user.username}
⏰ 𝐓𝐢𝐦𝐞: {time.strftime('%X')}
╚════════════════════╝
                    """,
                )
            return
            
        if name[0:3] == "inf":
            # ✧ TRACK INFO ANIMATION ✧
            anim = await music_visualizer(message)
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
            
            await anim.delete()
            try:
                await message.reply_sticker(random.choice(ULTRA_STICKERS))
            except Exception as e:
                print(f"Failed to send sticker for track info: {e}")
            
            return await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=f"""
╔════════════════════╗
       🎵 𝐓𝐑𝐀𝐂𝐊 𝐈𝐍𝐅𝐎 🎵
╠════════════════════╣
📌 𝐓𝐢𝐭𝐥𝐞: {title}
⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {duration}
👀 𝐕𝐢𝐞𝐰𝐬: {views}
📅 𝐏𝐮𝐛𝐥𝐢𝐬𝐡𝐞𝐝: {published}
🎙️ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: {channel}
╚════════════════════╝
                """,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=_["S_B_8"], url=link),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT)],
                ])
            )
    else:
        try:
            out = private_panel(_)
            
            # ✧ ULTRA WELCOME SEQUENCE ✧
            anim = await neon_text_animation(message, "𝐖𝐄𝐋𝐂𝐎𝐌𝐄")
            
            try:
                await message.reply_sticker(random.choice(ULTRA_STICKERS))
            except Exception as e:
                print(f"Failed to send sticker for welcome sequence: {e}")
            
            welcome_phrases = [
                f"✨ 𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 {message.from_user.mention}",
                f"🌟 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 {app.mention}",
                f"💫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐌𝐮𝐬𝐢𝐜 𝐄𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐞",
                f"🔥 𝐋𝐞𝐭's 𝐑𝐨𝐜𝐤 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭"
            ]
            
            for i, phrase in enumerate(welcome_phrases):
                progress = (i+1)*25
                await anim.edit_text(
                    f"{NEON_GRADIENTS[i%4]}\n"
                    f"{phrase}\n"
                    f"{generate_loading_bar(progress)} {progress}%\n"
                    f"{NEON_GRADIENTS[i%4][::-1]}"
                )
                await asyncio.sleep(0.8) # Increased from 0.5 for slower welcome phrases
            
            # ✧ MUSIC SYSTEM BOOT ANIMATION ✧
            boot_steps = [
                "⚡️ 𝐈𝐧𝐢𝐭𝐢𝐚𝐥𝐢𝐳𝐢𝐧𝐠 𝐒𝐲𝐬𝐭𝐞𝐦...",
                "🎛️ 𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐀𝐮𝐝𝐢𝐨 𝐌𝐨𝐝𝐮𝐥𝐞𝐬...",
                "📡 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐓𝐨 𝐒𝐞𝐫𝐯𝐞𝐫𝐬...",
                "🔊 𝐓𝐞𝐬𝐭𝐢𝐧𝐠 𝐀𝐮𝐝𝐢𝐨 𝐐𝐮𝐚𝐥𝐢𝐭𝐲...",
                f"✅ 𝐑𝐞𝐚𝐝𝐲 𝐓𝐨 𝐑𝐨𝐜𝐤, {message.from_user.mention}!"
            ]
            
            for step in boot_steps:
                await anim.edit_text(
                    f"╔════════════════════╗\n"
                    f"       🎶 {step}\n"
                    f"╚════════════════════╝"
                )
                await asyncio.sleep(1.0) # Increased from 0.7 for slower boot steps
            
            # Get user profile or default image
            userss_photo = None
            if message.chat.photo:
                try:
                    userss_photo = await app.download_media(
                        message.chat.photo.big_file_id,
                    )
                except:
                    userss_photo = None
            
            chat_photo = userss_photo if userss_photo else config.START_IMG_URL

        except Exception as e:
            print(f"Error during private start sequence: {e}")
            chat_photo = config.START_IMG_URL

        await anim.delete()
        
        # ✧ ULTRA FINAL MESSAGE ✧
        await message.reply_photo(
            photo=chat_photo,
            caption=f"""
╔════════════════════════╗
       🎧 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐌𝐔𝐒𝐈𝐂 🎧
╠════════════════════════╣
✨ 𝐇𝐞𝐲 {message.from_user.mention},
🌟 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 {app.mention}

🎶 𝐔𝐥𝐭𝐫𝐚 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐨
🔥 𝟐𝟒/𝟕 𝐕𝐨𝐢𝐜𝐞𝐜𝐡𝐚𝐭 𝐒𝐮𝐩𝐩𝐨𝐫𝐭
💫 𝐒𝐦𝐨𝐨𝐭𝐡 𝐏𝐥𝐚𝐲𝐛𝐚𝐜𝐤

╠════════════════════════╣
       {random.choice(NEON_GRADIENTS)}
╚════════════════════════╝
            """,
            reply_markup=InlineKeyboardMarkup(out),
        )

# █▀▀ █▀█ █▄░█ █▀▀   █▄▀ █▀▀ █▄█ █▄▄ █▀▀ █▀█
# █▄▄ █▄█ █░▀█ █▄▄   █░█ ██▄ ░█░ █▄█ ██▄ █▀▄

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def ultra_start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    
    # ✧ GROUP START ANIMATION ✧
    anim = await message.reply_text("🚀")
    for i in range(5):
        await anim.edit_text("🚀" + "•"*(i+1) + " "*(4-i) + f"{20*(i+1)}%")
        await asyncio.sleep(0.5) # Increased from 0.3
    
    await anim.edit_text("🎸 𝐑𝐞𝐚𝐝𝐲 𝐓𝐨 𝐏𝐥𝐚𝐲!")
    await asyncio.sleep(0.8) # Increased from 0.5
    await anim.delete()
    
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"""
╔════════════════════╗
       🎵 {app.mention} 🎵
╠════════════════════╣
⏳ 𝐔𝐩𝐭𝐢𝐦𝐞: {get_readable_time(uptime)}
🌟 𝐒𝐭𝐚𝐭𝐮𝐬: 𝐎𝐧𝐥𝐢𝐧𝐞
💫 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: {config.MUSIC_BOT_NAME}

╠════════════════════╣
       {random.choice(NEON_GRADIENTS)}
╚════════════════════╝
        """,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def ultra_welcome(client, message: Message):
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
                # ✧ GROUP WELCOME ANIMATION ✧
                anim = await message.reply_text("🎵")
                for i in range(1, 6):
                    await anim.edit_text("\n".join(["🎵" + "•"*i*2 + "🎶" for _ in range(3)]))
                    await asyncio.sleep(0.3) # Increased from 0.2
                
                await anim.delete()
                try:
                    await message.reply_sticker(random.choice(ULTRA_STICKERS))
                except Exception as e:
                    print(f"Failed to send sticker for group welcome: {e}")
                
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=f"""
╔════════════════════╗
       🌟 𝐓𝐇𝐀𝐍𝐊𝐒! 🌟
╠════════════════════╣
💫 𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐚𝐝𝐝𝐢𝐧𝐠 𝐦𝐞 𝐭𝐨:
✨ {message.chat.title}

🎶 𝐈'𝐦 {app.mention}, 𝐚 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐦𝐮𝐬𝐢𝐜 𝐛𝐨𝐭!
🔥 𝐏𝐥𝐚𝐲 𝐡𝐢𝐠𝐡 𝐪𝐮𝐚𝐥𝐢𝐭𝐲 𝐦𝐮𝐬𝐢𝐜 𝟐𝟒/𝟕

╠════════════════════╣
       {random.choice(NEON_GRADIENTS)}
╚════════════════════╝
                    """,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(f"Error in new_chat_members handler: {ex}")