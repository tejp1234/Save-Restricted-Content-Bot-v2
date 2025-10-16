# ---------------------------------------------------
# File Name: login.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import filters, Client
from devgagan import app
import random
import os
import asyncio
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe, chk_user
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)

def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # Editted ... 

async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    session_file_exists = os.path.exists(session_file)
    memory_file_exists = os.path.exists(memory_file)

    if session_file_exists:
        os.remove(session_file)
    
    if memory_file_exists:
        os.remove(memory_file)

    # Delete session from the database
    if session_file_exists or memory_file_exists:
        await db.remove_session(user_id)
        return True  # Files were deleted
    return False  # No files found

@app.on_message(filters.command("logout"))
async def clear_db(client, message):
    user_id = message.chat.id
    files_deleted = await delete_session_files(user_id)
    try:
        await db.remove_session(user_id)
    except Exception:
        pass

    if files_deleted:
        await message.reply("✅ Your session data and files have been cleared from memory and disk.")
    else:
        await message.reply("✅ Logged out with flag -m")
        
    
@app.on_message(filters.command("login"))
async def generate_session(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    number = await _.ask(
        user_id,
        "📱 Please enter your phone number with country code (e.g., +919876543210):",
        filters=filters.text,
    )
    phone_number = number.text.strip()

    await message.reply("📲 Sending OTP...")

    try:
        client = Client(f"session_{user_id}", api_id, api_hash)

        # ✅ Properly start the client
        await client.start()

        # ✅ Send OTP
        code = await client.send_code(phone_number)

    except ApiIdInvalid:
        await message.reply("❌ Invalid API ID or HASH.")
        return
    except PhoneNumberInvalid:
        await message.reply("❌ Invalid phone number. Please try again.")
        return
    except Exception as e:
        await message.reply(f"⚠️ Error sending OTP: {e}")
        return

    try:
        otp_msg = await _.ask(
            user_id,
            "📨 Enter the OTP you received on Telegram:\n\nExample: `1 2 3 4 5`",
            filters=filters.text,
            timeout=600,
        )
    except TimeoutError:
        await message.reply("⏰ Timeout! Please try again.")
        await client.disconnect()
        return

    phone_code = otp_msg.text.replace(" ", "")

    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await message.reply("❌ Invalid OTP.")
        await client.disconnect()
        return
    except PhoneCodeExpired:
        await message.reply("❌ OTP expired.")
        await client.disconnect()
        return
    except SessionPasswordNeeded:
        try:
            pw_msg = await _.ask(
                user_id,
                "🔐 Your account has two-step verification.\nPlease enter your password:",
                filters=filters.text,
                timeout=300,
            )
            password = pw_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await message.reply("❌ Invalid password.")
            await client.disconnect()
            return
        except TimeoutError:
            await message.reply("⏰ Timeout! Please restart login.")
            await client.disconnect()
            return

    # ✅ Export and save session
    string_session = await client.export_session_string()
    await db.set_session(user_id, string_session)

    await message.reply("✅ Login successful! Your session is now active.")
    await client.disconnect()
