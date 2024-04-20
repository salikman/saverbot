from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Команди: ",
            "/start - запустити бота",
            "/help - довідка")
    
    await message.answer("\n".join(text))
