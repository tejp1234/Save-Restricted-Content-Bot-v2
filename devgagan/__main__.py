

import asyncio
import importlib
import gc
from pyrogram import idle
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler

# ----------------------------Bot-Start---------------------------- #

loop = asyncio.get_event_loop()

# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(60)  # Check every hour
        gc.collect()

async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
📝 Description: A Pyrogram bot for downloading files from Telegram channels or groups 
                and uploading them back to Telegram.
👨‍💻 Author: Gagan
🌐 GitHub: https://github.com/devgaganin/
📬 Telegram: https://t.me/team_spy_pro
▶️ YouTube: https://youtube.com/@dev_gagan
🗓️ Created: 2025-01-11
🔄 Last Modified: 2025-01-11
🛠️ Version: 2.0.5
📜 License: MIT License
---------------------------------------------------
""")
    
    # Verify LOG_GROUP access
    from config import LOG_GROUP
    from devgagan import app
    try:
        chat = await app.get_chat(LOG_GROUP)
        print(f"✅ LOG_GROUP verified: {chat.title} ({LOG_GROUP})")
    except Exception as e:
        print(f"⚠️ WARNING: Cannot access LOG_GROUP ({LOG_GROUP})")
        print(f"   Error: {e}")
        print(f"   Please add bot to the channel/group with posting rights!")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")
    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #
