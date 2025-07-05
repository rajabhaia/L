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

# ✧✧✧ PREMIUM ASSETS ✧✧✧
ULTRA_STICKERS = [
    "CAACAgUAAxkBAAEQI1RlTLnRAy4h9lOS6jgS5FYsQoruOAAC1gMAAg6ryVcldUr_lhPexzME",
    "CAACAgUAAxkBAAKkw2hZgbt8t_FQU38s_k_8RZR3gsIiAAINFgAC0QyQVrqrLQzU13foHgQ",
    "CAACAgUAAxkBAAKkyGhZghOqGIGtgP5HkY1Nyk_vfugyAAJ5CgACQgZwVTVo2eQqCh15HgQ",
    "CAACAgEAAxkBAAEkK2VmH4wuG-7D1p-3X2t3j_7W78-pAACBAADmQ8jR-xR7wABGj7dMwQ",
    "CAACAgUAAxkBAAEQI1BlTLmx7PtOO3aPNshEU2gCy7iAFgACNQUAApqMuVeA6eJ50VbvmDME"
]

NEON_GRADIENTS = [
    "✨🌟💫🔥🎶⚡️",
    "⚡️🎶🔥💫🌟✨"
]

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
        await asyncio.sleep(0.35)
    return anim

async def music_visualizer(message):
    anim = await message.reply_text("🎵")
    for i in range(1, 6):
        await anim.edit_text("\n".join(["|"*i*2 for _ in range(3)]))
        await asyncio.sleep(0.45)
    return anim

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def ultra_start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    try:
        await message.reply_sticker(random.choice(ULTRA_STICKERS))
    except Exception as e:
        print(f"Failed to send welcome sticker: {e}")
    
    valid_reactions = ["👍", "❤️", "🔥", "🎉", "👏"]
    
    if len(valid_reactions) >= 3:
        for emoji in random.sample(valid_reactions, 3):
            try:
                await message.react(emoji)
                await asyncio.sleep(0.10)
            except Exception as e:
                print(f"Failed to react with {emoji}: {e}")

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
            keyboard = help_pannel(_)
            anim = await neon_text_animation(message, "𝐇𝐄𝐋𝐏 𝐂𝐄𝐍𝐓𝐄𝐑")
            
            try:
                await message.reply_sticker(random.choice(ULTRA_STICKERS))
            except Exception as e:
                print(f"Failed to send sticker for help command: {e}")
            
            for i in range(0, 101, 10):
                await anim.edit_text(f"✨ 𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮 ✨\n{generate_loading_bar(i)} {i}%")
                await asyncio.sleep(0.5)
            
            await anim.delete()
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
            
        if name[0:3] == "sud":
            anim = await message.reply_text("🔐")
            await asyncio.sleep(0.8)
            for i in range(3):
                await anim.edit_text("🔐" + "•"*(i+1))
                await asyncio.sleep(0.5)
            
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
            
            lol = await message.reply_text("💖 Hii cutiepie {}! 💖".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.edit_text("✨ Welcome to my cozy little corner, sweetie! ✨".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.edit_text("🌸 Let's make some magic with music! 🌸".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.edit_text("💅 Ready to slay with some tunes? 💅".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.edit_text("💋 Kisses and good vibes only! 💋".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.edit_text("🎀 So happy you're here, hun! 🎀".format(message.from_user.mention))
            await asyncio.sleep(0.2)
            await lol.delete()
            
            lols = await message.reply_text("**💖 L**")
            await asyncio.sleep(0.1)
            await lols.edit_text("💖 Lo")        
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loa**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Load**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loadi**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loadin**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loading**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loading.**")
            await asyncio.sleep(0.1) 
            await lols.edit_text("**💖 Loading....**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loading.**")
            await asyncio.sleep(0.1)
            await lols.edit_text("**💖 Loading....**")
            await asyncio.sleep(0.5)
            
            await lols.delete()
            
            m = await message.reply_sticker("CAACAgUAAxkBAAEQI1BlTLmx7PtOO3aPNshEU2gCy7iAFgACNQUAApqMuVeA6eJ50VbvmDME")
            await asyncio.sleep(0.5)
            
            userss_photo = None
            if message.chat.photo:
                try:
                    userss_photo = await app.download_media(
                        message.chat.photo.big_file_id,
                    )
                except Exception as e:
                    print(f"Error downloading user photo: {e}")
                    userss_photo = None
            
            chat_photo = userss_photo if userss_photo else config.START_IMG_URL

        except Exception as e:
            print(f"Error during private start sequence: {e}")
            chat_photo = config.START_IMG_URL

        try:
            await message.reply_sticker(random.choice(ULTRA_STICKERS))
        except Exception as e:
            print(f"Failed to send goodbye sticker: {e}")
        
        await message.reply_photo(
            photo=chat_photo,
            caption=f"""
╔════════════════════════╗
       🎧 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐌𝐔𝐒𝐈𝐂 🎧
╠════════════════════════╣
✨ Hiii, {message.from_user.mention}!
💖 Welcome to your ultimate music experience with {app.mention}!

🎶 Get ready for super high-quality audio
🌸 I'm here 24/7 to make sure your party never stops!
💫 Enjoy the smoothest music playback ever!

╠════════════════════════╣
       {random.choice(NEON_GRADIENTS)}
╚════════════════════════╝
            """,
            reply_markup=InlineKeyboardMarkup(out),
        )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def ultra_start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    
    try:
        await message.reply_sticker(random.choice(ULTRA_STICKERS))
    except Exception as e:
        print(f"Failed to send group welcome sticker: {e}")
    
    anim = await message.reply_text("🚀")
    for i in range(5):
        await anim.edit_text("🚀" + "•"*(i+1) + " "*(4-i) + f"{20*(i+1)}%")
        await asyncio.sleep(0.5)
    
    await anim.edit_text("🎸 𝐑𝐞𝐚𝐝𝐲 𝐓𝐨 𝐏𝐥𝐚𝐲!")
    await asyncio.sleep(0.8)
    await anim.delete()
    
    try:
        await message.reply_sticker(random.choice(ULTRA_STICKERS))
    except Exception as e:
        print(f"Failed to send group goodbye sticker: {e}")
    
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=f"""
╔════════════════════╗
       🎵 {app.mention} 🎵
╠════════════════════╣
⏳ Uptime: {get_readable_time(uptime)}
🌟 Status: Online and fabulous!
💫 Powered By: {config.MUSIC_BOT_NAME} - Your ultimate music companion!

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
                except Exception as e:
                    print(f"Error banning member: {e}")
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
                try:
                    await message.reply_sticker(random.choice(ULTRA_STICKERS))
                except Exception as e:
                    print(f"Failed to send group welcome sticker: {e}")
                
                anim = await message.reply_text("🎵")
                for i in range(1, 6):
                    await anim.edit_text("\n".join(["💖" + "🎶"*i*2 + "✨" for _ in range(3)])) # Changed emojis
                    await asyncio.sleep(0.3)
                
                await anim.delete()
                
                try:
                    await message.reply_sticker(random.choice(ULTRA_STICKERS))
                except Exception as e:
                    print(f"Failed to send group goodbye sticker: {e}")
                
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=f"""
╔════════════════════╗
       🌟 𝐓𝐇𝐀𝐍𝐊𝐒, 𝐇𝐔𝐍! 🌟
╠════════════════════╣
💫 Thanks for adding me to your awesome group, sweetie:
✨ {message.chat.title}

🎶 I'm {app.mention}, your fabulous premium music bot!
💖 I'm here to play high-quality music 24/7, let's party!

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