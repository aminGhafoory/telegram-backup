import asyncio
from telethon import TelegramClient
import configparser
from datetime import datetime
import os

# +------------------user credentials-------------------+
config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["user"]["api_id"]
api_hash = config["user"]["api_hash"]
phone_number = config["user"]["phone_number"]

# +-------------------client setup----------------------+
client = TelegramClient("session_db", api_id, api_hash)
client.start(phone=phone_number)

# +------------backup file path and caption-------------+
date = datetime.now().strftime("%Y/%m/%d")
time = datetime.now().strftime("%H:%M:%S")
file_path = "test.py"
size = os.stat(file_path).st_size / (1024 * 1024)


async def backup(
    file_path: str,
    target_chat: str = "me",
    caption: str = f"\n 📆 **date: **{date}\n⏰ **time: **{time}\n💾 **size: **{size:.2f} Mb \n .",
    error_report: str = "me",
) -> None:
    try:
        await client.send_file(
            target_chat,
            file_path,
            caption=caption,
        )
    except Exception as e:
        print(e)
        await client.send_message(
            error_report, f"❗️**Error in uploading file**: ```{file_path}```"
        )


with client:
    client.loop.run_until_complete(
        backup(target_chat="@links_amin", file_path=file_path)
    )
