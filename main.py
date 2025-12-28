import asyncio
import os
import yt_dlp

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# ================== CONFIG ==================
API_ID = 123456         # <-- your api_id
API_HASH = "API_HASH_HERE"
SESSION_NAME = "user"    # session file name
# ============================================

app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)

pytgcalls = PyTgCalls(app)

def download(song):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{song}"])
    return "song.webm"

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("Use: /play songname")
        return

    song = " ".join(message.command[1:])
    await message.reply("🎶 Downloading...")

    file = download(song)

    await pytgcalls.join_group_call(
        message.chat.id,
        AudioPiped(file),
    )

    await message.reply(f"▶️ Playing: **{song}**")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply("⏹️ Stopped")

async def main():
    await app.start()
    await pytgcalls.start()
    print("🎧 User VC Music Running...")
    await asyncio.Event().wait()

asyncio.run(main())
