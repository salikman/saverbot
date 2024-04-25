from time import sleep
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import logging,re
from aiogram import types
from aiogram.types import CallbackQuery
from .insta import instadownloader, InstaDownloader
from data.config import ADMINS
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, main_menu_for_admin
from loader import dp, db, bot
from utils.files.spotify import SearchFromSpotify
from utils.files.download_spotify import DownloadMusic
logging.basicConfig(level=logging.INFO)
import re,json
from tiktok_downloader import snaptik
import os, requests
from .insta import FastDLAppDownloader
from utils.files.shazam import shazamtop




@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start_admin(message: types.Message):
    await message.answer(f"Привіт адмін, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_admin)

@dp.message_handler(IsSuperAdmin(), CommandStart(), state="*")
async def bot_start_super_admin(message: types.Message):
    await message.answer(f"Привіт босс, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_super_admin)

@dp.message_handler(commands=['start'], state="*")
async def bot_start(message: types.Message):
    user = message.from_user
    try:
        db.add_user(user_id=user.id,name=user.first_name,active=True)
    except:
        pass
    user_id = message.from_user.first_name
    await message.answer(f"<b>👋🏻 Привіт {user_id}\n\n </b>Щоб завантажити відео, вставте посилання")

instagram_regex = r'(https?:\/\/(?:www\.)?instagram\.com\/[-a-zA-Z0-9@:%._+~#=]*)'
tiktok_regex = r'(https?:\/\/(?:www\.)?tiktok\.com\/@[-a-zA-Z0-9_]+\/video\/\d+)'
youtube_regex = r'(https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]+)'
    

async def download_instagram_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    download_data = await instadownloader(text)

    if download_data:
        try:
            if download_data['Type'] == 'video':
                await bot.send_video(message.chat.id, download_data['media'], caption="Завантажено через @UltimateSaverBot")
            elif download_data['Type'] == 'image':
                await bot.send_photo(message.chat.id, download_data['media'], caption="Завантажено через @UltimateSaverBot")
            elif download_data['Type'] == 'carousel':
                await bot.send_media_group(message.chat.id, [types.InputMediaPhoto(media) for media in download_data['media']], caption="Завантажено через @UltimateSaverBot")
            elif download_data['Type'] == 'story':
                await bot.send_video(message.chat.id, download_data['media'], caption="Завантажено через @UltimateSaverBot")
        except Exception as err:
            print(err)
            await message.answer("<b>Вибачте, сталася помилка при завантаженні вмісту, спробуйте ще 😔</b>")
    else:
        await message.answer("<b>Не вдалося знайти вміст за цим посиланням 😔</b>")

async def download_tiktok_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    res = snaptik(text)
    video = res[0].download(f"{message.message_id}.mp4")
    input_file = types.InputFile(f"{message.message_id}.mp4")
    await bot.send_video(message.chat.id, video=input_file, caption="Завантажено через @UltimateSaverBot")
    os.remove(f"{message.message_id}.mp4")

async def download_youtube_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    r = requests.get(f"https://youtube-dl.wave.video/info?url={text}&type=video")
    print(r.status_code)
    vid = r.json().get('formats', [{}])[0].get('downloadUrl')

    try:
        await bot.send_video(chat_id=message.chat.id, video=vid, caption="Завантажено через @UltimateSaverBot")
    except Exception as err:
        print(err)
        await message.answer("<b>Вибачте, сталася помилка при завантаженні вмісту, спробуйте ще 😔</b>")

# Handle text messages
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    text = message.text

    if re.search(instagram_regex, text):
        await download_instagram_video(message, text)
    elif "tiktok.com" in text:
        await download_tiktok_video(message, text)
    elif any(substring in text for substring in ["youtube"]):
        await download_youtube_video(message, text)