import asyncio

from aiogram.types import Message



cat_art = """
*           *
  /     \\
 |  O _ o|
 |    ^*  |
 |   \ _\ |
  \\_____/
"""
cat_art2 = """
*           *
  /     \\
 |  o _ O |
 |    ^*   |
 |   /_/   |
  \\_____/
"""


async def anime_art(message: Message, msg):
    await asyncio.sleep(1)
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=cat_art)
    await asyncio.sleep(1)
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=cat_art2)

