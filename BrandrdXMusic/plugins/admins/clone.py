import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import AccessTokenExpired, Unauthorized
from pyrogram.types import Message
from pyrogram.types import Message
from BrandrdXMusic import app, LOGGER
from config import API_ID, API_HASH, SUDO_USERS

# --- Pichle code se zaroori functions ---

running_clones = {}
DB_FILE = "cloned_bots.json"

def get_clones_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_clones_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def start_and_manage_clone(user_id, token):
    global running_clones
    if user_id in running_clones:
        await running_clones[user_id].stop()
    try:
        clone_bot = Client(
            name=f"clone_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=token,
            in_memory=True,
        )
        await clone_bot.start()
        bot_info = await clone_bot.get_me()
        running_clones[user_id] = clone_bot
        LOGGER("BrandrdXMusic").info(f"Clone for user {user_id} (@{bot_info.username}) started successfully.")
        return bot_info
    except (AccessTokenExpired, Unauthorized):
        raise AccessTokenExpired("Bot token expired or has been revoked.")
    except Exception as e:
        LOGGER("BrandrdXMusic").error(f"Failed to start clone for user {user_id}: {e}")
        raise e

async def load_all_clones():
    db = get_clones_db()
    if not db:
        LOGGER("BrandrdXMusic").info("No saved bots found to copy.")
        return
    LOGGER("BrandrdXMusic").info(f"Found {len(db)} saved bots. Copying them now...")
    for user_id_str, token in db.items():
        try:
            user_id = int(user_id_str)
            await start_and_manage_clone(user_id, token)
        except Exception as e:
            LOGGER("BrandrdXMusic").error(f"Could not start copied bot for user {user_id_str}: {e}")

# --- Naya /clone Command ka Logic ---

@app.on_message(filters.command("clone") & filters.private)
async def clone_bot_conversational(client: Client, message: Message):
    # Step 1: Check karein ki user Sudo hai ya nahi
    if message.from_user.id not in SUDO_USERS:
        # Agar Sudo nahi hai, to purana message bhejein
        return await message.reply_photo(
            photo=f"https://files.catbox.moe/dsp9mx.jpg",
            caption=f"""**🙂You Are Not Sudo User So You Are Not Allowed To Clone Me.**\n**😌Click Given Below Button And Host Manually Otherwise Contact Owner Or Sudo Users For Clone.**""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ƨσʋяcɛ", url=f"https://telegra.ph/file/843109296a90b8a6c5f68.jpg"
                        )
                    ]
                ]
            ),
        )

    # Step 2: Agar Sudo User hai, to conversational flow shuru karein
    try:
        # Bot token maangein
        ask_msg = await client.ask(
            chat_id=message.chat.id,
            text="🤖 **Please provide the bot token to clone.**\n\nTo cancel this process, send /cancel.",
            timeout=300  # 5 minute ka time
        )

        # Agar user /cancel bhejta hai
        if ask_msg.text == "/cancel":
            return await ask_msg.reply_text("Cloning process has been cancelled.")

        bot_token = ask_msg.text
        user_id = message.from_user.id
        
        processing_msg = await ask_msg.reply_text("🔄 **Processing...** Verifying token and starting the bot.")
        
        # Bot ko start karne ki koshish karein
        bot_info = await start_and_manage_clone(user_id, bot_token)
        
        # Database mein save karein
        db = get_clones_db()
        db[str(user_id)] = bot_token
        save_clones_db(db)
        
        # Success message bhejein
        await processing_msg.edit_text(
            f"✅ **Bot Cloned Successfully!**\n\n"
            f"Your bot **@{bot_info.username}** is now online and running.\n\n"
            "It will restart automatically with the main bot."
        )

    except asyncio.TimeoutError:
        await message.reply_text("⏰ **Timeout!**\nYou didn't provide the token in time. Please start over by sending /clone again.")
    except AccessTokenExpired as e:
        await message.reply_text(f"❌ **Error:** {e}")
    except Exception as e:
        await message.reply_text(f"❌ **An unexpected error occurred:**\n`{e}`")
