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
from states.send_chanell import SuperAdminStateChannel
from utils.files.spotify import SearchFromSpotify
from utils.files.download_spotify import DownloadMusic
logging.basicConfig(level=logging.INFO)
import re,json
from .tiktok import TikTokDownlaoder
from tiktok_downloader import snaptik
from .shazam import ShazamIO
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


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    user = message.from_user
    try:
        db.add_user(user_id=user.id,name=user.first_name)
    except:
        pass
    user_id = message.from_user.first_name
    await message.answer(f"<b>👋🏻 Привіт {user_id}\n\n </b>Щоб завантажити відео, вставте посилання")

instagram_regex = r'(https?:\/\/(?:www\.)?instagram\.com\/[-a-zA-Z0-9@:%._+~#=]*)'
tiktok_regex = r'(https?:\/\/(?:www\.)?tiktok\.com\/@[-a-zA-Z0-9_]+\/video\/\d+)'
youtube_regex = r'(https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]+)'
    

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    text = message.text
    if re.search(instagram_regex, text):
        msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        app = FastDLAppDownloader()
        vid = app.download_url(text)
        if vid:
            try:
                await msg_del.delete()
                await bot.send_document(message.chat.id, vid, caption="Завантажено через @UltimateSaverBot")
                with open(f"{message.message_id}.mp4", 'wb') as video:
                    rrr = requests.get(vid)
                    video.write(rrr.content)
                input_file = types.InputFile(f"{message.message_id}.mp4")
                shazammusic = await shazamtop(f"{message.message_id}.mp4")
                title = shazammusic['title']
                if title is not None:
                    musics = SearchFromSpotify(track_name=title, limit=5)
                    audio_urls = DownloadMusic(musics)
                inline_kbs = types.InlineKeyboardMarkup()
                os.remove(f"{message.message_id}.mp4")


                    
                
            except Exception as err:
                with open(f"{message.message_id}.mp4", 'wb') as video:
                    rrr = requests.get(vid)
                    video.write(rrr.content)
                input_file = types.InputFile(f"{message.message_id}.mp4")
                await bot.send_document(message.chat.id, document=input_file,caption="Завантажено через @UltimateSaverBot")
                shazammusic = await shazamtop(f"{message.message_id}.mp4")
                title = shazammusic['title']


                os.remove(f"{message.message_id}.mp4")
            
            with open(f"{message.message_id}.mp4", 'wb') as video:
                rrr = requests.get(vid)
                video.write(rrr.content)
            shazammusic = await shazamtop(f"{message.message_id}.mp4")
            title = shazammusic['title']

            os.remove(f"{message.message_id}.mp4")
            

    elif "tiktok.com" in text:
        msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

        res = snaptik(text)
        video = res[0].download(f"{message.message_id}.mp4")
        input_file = types.InputFile(f"{message.message_id}.mp4")
        # await msg_del.delete()

        await bot.send_video(message.chat.id, video=input_file,caption="Завантажено через @UltimateSaverBot")
        os.remove(f"{message.message_id}.mp4")


    elif any(substring in text for substring in ["youtube"]):
        msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

        getUrl = requests.get("https://youtube-dl.wave.video/info?url={}&type=video".format(text))
        getLink = getUrl.json()['formats'][0]['url']
        # getThumbLink = getUrl.json()['thumbnail']

        try: 
            await bot.send_video(chat_id=message.chat.id, video=getLink, caption="Завантажено через @UltimateSaverBot")
        except Exception as err:
            await message.answer("<b> Вибачте, щось пішло не так 😔</b>")



