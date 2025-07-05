import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import AccessTokenExpired, Unauthorized

from BrandrdXMusic import app
from config import API_ID, API_HASH, SUDO_USERS

# Ek dictionary jo chal rahe copy clients ko store karegi
running_copys = {}
DB_FILE = "copyd_bots.json"

# --- Database Functions ---

def get_copys_db():
    """copyd_bots.json se data load karta hai."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_copys_db(data):
    """Data ko copyd_bots.json mein save karta hai."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- copy Management ---

async def start_and_manage_copy(user_id, token):
    """Ek naye copy bot client ko start aur manage karta hai."""
    global running_copys
    
    # Agar is user ka copy pehle se chal raha hai, to use rokein
    if user_id in running_copys:
        await running_copys[user_id].stop()
    
    try:
        # copy bot ke liye naya Pyrogram client banayein
        # Session name unique hona zaroori hai
        copy_bot = Client(
            name=f"copy_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=token,
            in_memory=True, # Session file banane ki zaroorat nahi
        )
        
        await copy_bot.start()
        bot_info = await copy_bot.get_me()
        
        # Chal rahe copys ki dictionary mein add karein
        running_copys[user_id] = copy_bot
        
        print(f"[INFO] - copy for user {user_id} (@{bot_info.username}) started successfully.")
        return bot_info
        
    except (AccessTokenExpired, Unauthorized):
        raise AccessTokenExpired("Bot token expired or has been revoked.")
    except Exception as e:
        print(f"[ERROR] - Failed to start copy for user {user_id}: {e}")
        raise e


@app.on_message(filters.command("copy") & filters.user(SUDO_USERS) & filters.private)
async def copy_bot_command(client, message):
    """
    /copy command ko handle karta hai.
    Usage: /copy BOT_TOKEN
    """
    await message.reply_text("🔄 **Processing your request...** Please wait.")

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n`/copy BOT_TOKEN`\n\n"
            "Please provide a bot token to copy."
        )

    bot_token = message.command[1]
    user_id = message.from_user.id

    try:
        # copy ko start karne ki koshish karein
        bot_info = await start_and_manage_copy(user_id, bot_token)
        
        # Agar successful, to database mein save karein
        db = get_copys_db()
        db[str(user_id)] = bot_token
        save_copys_db(db)
        
        await message.reply_text(
            f"✅ **Bot copyd Successfully!**\n\n"
            f"Your bot **@{bot_info.username}** is now online and running.\n\n"
            "It will restart automatically with the main bot."
        )
    except AccessTokenExpired as e:
        await message.reply_text(f"❌ **Error:** {e}")
    except Exception as e:
        await message.reply_text(f"❌ **An unexpected error occurred:**\n`{e}`")


# --- Startup Function ---

async def load_all_copys():
    """Bot ke start hone par sabhi saved copys ko load aur start karta hai."""
    db = get_copys_db()
    if not db:
        print("[INFO] - No saved copys found in database.")
        return

    print(f"[INFO] - Found {len(db)} saved copys. Starting them now...")
    for user_id_str, token in db.items():
        try:
            user_id = int(user_id_str)
            await start_and_manage_copy(user_id, token)
        except Exception as e:
            print(f"[ERROR] - Could not start copy for user {user_id_str}: {e}")