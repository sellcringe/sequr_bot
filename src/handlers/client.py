import asyncio
import os
import urllib.parse

from ..virustotal.scan import scan_file, scan_url



from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from ..service.anime import anime_art

router = Router()

load_dotenv()

@router.message(CommandStart())
async def start_command(message: Message):
    await message.bot.send_message(os.getenv("ADMIN"), text=
    f'user_id: {message.from_user.id}\n'
    f'username: {message.from_user.username}\n'
    f'fullname: {message.from_user.full_name}\n'
    # f'phone number: {message.contact.phone_number}'
                                   )



@router.message(F.document or F.audio or F.video or F.photo)
async def info_about_file(message: Message):

    max_size = 32 * 1024 * 1024
    file_size = message.document.file_size

    if file_size < max_size:
        msg = await message.bot.send_message(message.chat.id, text='Сканирование началось...')

        file = await message.bot.get_file(message.document.file_id)
        file_url = f'https://api.telegram.org/file/bot{os.getenv("TOKEN")}/{file.file_path}'
        scan_task = asyncio.create_task(scan_file(file_url))


        while not scan_task.done():
            await anime_art(message, msg)

        about_file = await scan_task
        await message.answer(str(about_file))
    else:
        await message.answer('Файл больше 32 МБ')



@router.message(F.text.func(lambda text: bool(urllib.parse.urlparse(text).scheme and urllib.parse.urlparse(text).netloc)))
async def info_about_url(message: Message):
    msg = await message.bot.send_message(message.chat.id, text='Сканирование началось...')

    url = message.text
    scan_task = asyncio.create_task(scan_url(url))
    while not scan_task.done():
        await anime_art(message, msg)

    about_url = await scan_task
    await message.answer(str(about_url))



