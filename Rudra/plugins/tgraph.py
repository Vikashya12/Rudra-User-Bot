import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters


from .. import *
from telegraph import Telegraph, upload_file
import requests


telegraph = Telegraph()
filesize = 5242880 #[5MB]


def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    files = {"fileToUpload": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return True, response.text.strip()
    else:
        return False, f"ᴇʀʀᴏʀ: {response.status_code} - {response.text}"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ Tᴇʟᴇɢʀᴀᴘʜ"
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇᴅɪᴀ ғɪʟᴇ ᴜɴᴅᴇʀ 200MB.")

    try:
        text = await message.reply("❍ ʜᴏʟᴅ ᴏɴ ʙᴀʙʏ....♡")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ...")

            success, upload_path = upload_file(local_path)

            if success:
                await text.edit_text(
                    f"🌐 | [👉ʏᴏᴜʀ ʟɪɴᴋ ᴛᴀᴘ ʜᴇʀᴇ👈]({upload_path})",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    " ᴄʀᴇᴀᴛᴇ ʙʏ ˹ᴠɪᴋᴋʏ˼ ᴛᴀᴘ ᴛᴏ sᴇᴇ ",
                                    url=upload_path,
                                )
                            ]
                        ]
                    ),
                )
            else:
                await text.edit_text(
                    f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴜᴘʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ\n{upload_path}"
                )

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ Fɪʟᴇ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ\n\n<i>Rᴇᴀsᴏɴ: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass

__NAME__ = "TGraph"
__MENU__ = """**Telegraph Uploader:**

`.tl` - Reply This Command To
Any Text Or Media To Create
Telegraph Link.

`.tl` [title]” - Set Custom Title
On Your Telegraph Post.
(Working Only On Text Post).

**Ex:-** `/tl 🥀 My Note ✨`
"""
