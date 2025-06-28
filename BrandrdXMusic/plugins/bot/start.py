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

# --- NEW STICKER FILE IDS (Ensure these are valid sticker file IDs) ---
# Replace these with your desired sticker file IDs
WELCOME_STICKER_1 = "CAACAgUAAxkBAAODaF9fCwH1U3853rlI7T5hJQ4JK8cAAk4FAAKd1NlU3Np8RGo3ELIeBA"
WELCOME_STICKER_2 = "CAACAgUAAxkBAAODaF9fCwH1U3853rlI7T5hJQ4JK8cAAk4FAAKd1NlU3Np8RGo3ELIeBA"
STARTING_STICKER_1 = "CAACAgUAAxkBAALBDWhfXWP-s97rb5UBaM5H2qENUsx-AAKhBQAC01ToVJMdqKKVm9x1HgQ"
STARTING_STICKER_2 = "CAACAgUAAxkBAALBDWhfXWP-s97rb5UBaM5H2qENUsx-AAKhBQAC01ToVJMdqKKVm9x1HgQ"

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    # Dynamic reaction based on user's preference or a random choice
    reactions = ["🥰", "💖", "✨", "🚀", "🎶"]
    await message.react(reactions[0]) # You can randomize this if you wish

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            try:
                await message.reply_sticker(WELCOME_STICKER_2)
            except Exception as e:
                print(f"Error sending WELCOME_STICKER_2: {e}")
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
                    text=f"✨ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n👤 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n🔖 <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔍 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠...")
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
                    text=f"🎵 {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n👤 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n🔖 <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        try:
            out = private_panel(_)

            # --- Enhanced Welcome Animation with more flair ---
            welcome_messages = [
                "💫 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ︎ {}. . . ✨",
                "✨ 𝐇𝐞𝐥𝐥𝐨, 𝐒𝐰𝐞𝐞𝐭𝐡𝐞𝐚𝐫𝐭! ꨄ︎ {}. . . 🥳",
                "💖 𝐆𝐥𝐚𝐝 𝐭𝐨 𝐬𝐞𝐞 𝐲𝐨𝐮, {}. . . 🎉",
                "🚀 𝐆𝐞𝐭 𝐫𝐞𝐚𝐝𝐲 𝐭𝐨 𝐣𝐚𝐦, {}. . . 🎶",
                "🌟 𝐄𝐧𝐣𝐨𝐲 𝐭𝐡𝐞 𝐦𝐮𝐬𝐢𝐜, {}. . . 🤩",
                "💞 𝐒𝐢𝐭 𝐛𝐚𝐜𝐤 𝐚𝐧𝐝 𝐫𝐞𝐥𝐚𝐱, {}. . . 🥰",
            ]

            # Send initial welcome message and animate
            lol = await message.reply_text(welcome_messages[0].format(message.from_user.mention))
            for i in range(1, len(welcome_messages)):
                await asyncio.sleep(0.2) # Slower animation for better readability
                await lol.edit_text(welcome_messages[i].format(message.from_user.mention))
            await asyncio.sleep(0.5) # Pause before starting animation
            await lol.delete() # Delete the animated welcome message

            # --- Dynamic Starting Text Animation with stylish touch ---
            starting_messages = [
                "⚡️ ᴘʀᴇᴘᴀʀɪɴɢ...",
                "🎶 ʟᴏᴀᴅɪɴɢ ᴍᴜsɪᴄ ᴇɴɢɪɴᴇ...",
                "🚀 ʙᴏᴏᴛɪɴɢ sʏsᴛᴇᴍs...",
                "✅ ᴀʟᴍᴏsᴛ ᴛʜᴇʀᴇ...",
                "🌟 𝐑𝐞𝐚𝐝𝐲 𝐭𝐨 𝐏𝐥𝐚𝐲! 🎵"
            ]

            lols = await message.reply_text(starting_messages[0])
            for i in range(1, len(starting_messages)):
                await asyncio.sleep(0.2) # Slightly slower for more impact
                await lols.edit_text(starting_messages[i])

            await asyncio.sleep(0.3) # Pause after starting animation

            # --- Changed Sticker for starting animation ---
            m = None
            try:
                m = await message.reply_sticker(STARTING_STICKER_2) # Using the new sticker ID
            except Exception as e:
                print(f"Error sending STARTING_STICKER_2: {e}")

            userss_photo = None
            if message.chat.photo:
                try:
                    userss_photo = await app.download_media(
                        message.chat.photo.big_file_id,
                    )
                except Exception as e:
                    print(f"Error downloading chat photo: {e}")
                    userss_photo = None # Fallback if download fails

            chat_photo = userss_photo if userss_photo else config.START_IMG_URL # Use config.START_IMG_URL for global default

        except AttributeError:
            chat_photo = config.START_IMG_URL # Ensure it falls back to the configured URL
        except Exception as e:
            print(f"An unexpected error occurred during start_pm: {e}")
            chat_photo = config.START_IMG_URL # Fallback in case of any other error

        await lols.delete()
        if m:
            await m.delete()
        await message.reply_photo(
            photo=chat_photo,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"🚀 {message.from_user.mention} ʜᴀs sᴛᴀʀᴛᴇᴅ ʙᴏᴛ.\n\n**👤 ᴜsᴇʀ ɪᴅ :** {sender_id}\n**🔖 ᴜsᴇʀ ɴᴀᴍᴇ:** {sender_name}",
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
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
                except Exception as e:
                    print(f"Error banning user: {e}")
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("🚫 This bot works best in supergroups! Please add me to a supergroup for full functionality. 🚀")
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        "🚨 This chat is blacklisted! Please contact support for more information. "
                        f"Support Chat: {config.SUPPORT_CHAT}",
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(f"Error in new_chat_members handler: {ex}")

# --- New Sticker ID Function ---
@app.on_message(filters.command(["stickerid", "stid"]))
async def get_sticker_id(client, message: Message):
    sticker_file_id = None

    # Check if the message is a reply to a sticker
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_file_id = message.reply_to_message.sticker.file_id
        await message.reply_text(
            f"Sticker ID: \n`{sticker_file_id}`\n\n_You can use this ID in your bot's code!_"
        )
    # Check if the message itself contains a sticker (if the command was used as a caption)
    elif message.sticker:
        sticker_file_id = message.sticker.file_id
        await message.reply_text(
            f"Sticker ID: \n`{sticker_file_id}`\n\n_You can use this ID in your bot's code!_"
        )
    else:
        await message.reply_text(
            "Please reply to a sticker with `/stickerid` or send a sticker with this command as caption to get its ID."
        )

