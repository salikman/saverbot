import time
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#Dasturchi @Mrgayratov kanla @Kingsofpy
from filters import IsSuperAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, back_to_main_menu
from loader import dp, db, bot
from states.admin_state import SuperAdminState

# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN
@dp.callback_query_handler(IsSuperAdmin(), text="add_admin", state="*")
async def add_admin(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi adminni chat IDsini yuboring...\n"
                                 "🆔 Перейдіть до @userinfobot і натиснути /start, щоб отримати ідентифікаційний номер АДМ",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_ADMIN.set()

@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_ADMIN)
async def add_admin_method(message: types.Message, state: FSMContext):
    admin_id =message.text
    await state.update_data({"admin_id": admin_id})
    await message.answer("👨🏻‍💻 Надішліть нове ім'я АДМ",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_FULLNAME.set()
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_FULLNAME)
async def add_admin_method(message: types.Message,state: FSMContext):
    try:
        full_name = message.text
        await state.update_data({"full_name": full_name})
        malumot = await state.get_data()
        # Dasturchi @Mrgayratov kanla @Kingsofpy
        adminid = malumot.get("admin_id")
        full_name = malumot.get("full_name")

        try:
            db.add_admin(user_id=adminid,
                         full_name=full_name)
        except:
            pass
        await bot.send_message(chat_id=adminid,text="Вітаємо, ви отримали права адміністратора в нашому боті, натисніть /start")
        await message.answer("✅ Нового АДМ успішно додано!", reply_markup=main_menu_for_super_admin)
        await state.finish()
    except Exception as e:
        print(e)
        await message.answer("❌ Виникла помилка!", reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(), text="del_admin", state="*")
async def show_admins(call: types.CallbackQuery):
    print(call.data)
    await call.answer(cache_time=2)
    admins = db.select_all_admins()
    buttons = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[2]}", callback_data=f"admin:{admin[1]}"))
    # Dasturchi @Mrgayratov kanla @Kingsofpy
    buttons.add(InlineKeyboardButton(text="➕ Додати АДМ", callback_data="add_admin"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu"))
    await call.message.edit_text(text="👤 АДМ", reply_markup=buttons)
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.callback_query_handler(IsSuperAdmin(), text_contains="admin:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    admin = db.select_all_admin(user_id=data[1])
    for data in admin:
        text = f"Ваша інформація\n\n"
        text += f"<i>👤 Імя:</i> <b>{data[2]}\n</b>"
        text += f"<i>🆔 ID:</i> <b>{data[1]}</b>"
        buttons = InlineKeyboardMarkup(row_width=1)

        buttons.insert(InlineKeyboardButton(text="❌ Видалено з АДМ", callback_data=f"deladm:{data[1]}"))
        buttons.insert(InlineKeyboardButton(text="⬅️ Назад", callback_data="admins"))

        await call.message.edit_text(text=text, reply_markup=buttons)
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.callback_query_handler(IsSuperAdmin(), text_contains="deladm:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    print(data[1])
    delete_orders = db.delete_admin(admin_id=data[1])
    await bot.send_message(chat_id=data[1],
                           text="Вам надано права АДМ")
    # Dasturchi @Mrgayratov kanla @Kingsofpy
    await call.answer("🗑 АДМ вимкнено !",show_alert=True)
    await call.message.edit_text("✅ АДМ видалено!", reply_markup=main_menu_for_super_admin)
# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN

# MAJBURIY OBUNA SOZLASH UCHUN
@dp.callback_query_handler(text = "add_channel")
async def add_channel(call: types.CallbackQuery):
    await SuperAdminState.SUPER_ADMIN_ADD_CHANNEL.set()
    await call.message.edit_text(text="<i><b>📛 Введіть ім'я користувача або ID каналу: </b></i>")
    await call.message.edit_reply_markup(reply_markup=back_to_main_menu)


@dp.message_handler(state=SuperAdminState.SUPER_ADMIN_ADD_CHANNEL)
async def add_channel(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit() or matn.startswith("@"):
        try:
            if db.check_channel(channel=message.text):
                await message.answer("<i>❌Цей канал додано! Додайте інший канал!</i>", reply_markup=back_to_main_menu)
            else:
                try:
                    deeellll = await bot.send_message(chat_id=message.text, text=".")
                    await bot.delete_message(chat_id=message.text, message_id=deeellll.message_id)
                    try:
                        db.add_channel(channel=message.text)
                    except:
                        pass
                    await message.answer("<i><b>Канал успішно додано ✅</b></i>")
                    await message.answer("<i>Ви в панелі АДМ. 🧑‍💻</i>", reply_markup=main_menu_for_super_admin)
                    await state.finish()
                except:
                    await message.reply("""<i><b>
Я не адмін цього каналу!⚙️
Або канал із вказаним вами логіном не існує! ❌
Повторіть спробу як адміністратор каналу або введіть дійсне ім’я користувача.🔁
                    </b></i>""", reply_markup=back_to_main_menu)
        except Exception as err:
            await message.answer(f"Помилка зникла: {err}")
            await state.finish()
    else:
        await message.answer("Ви ввели помилку.", reply_markup=back_to_main_menu)

@dp.callback_query_handler(text="del_channel")
async def channel_list(call: types.CallbackQuery):
    royxat = db.select_channels()
    text = "🔰 Список каналів:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[1]}\n💠 Username: {o[1]}\n\n"
    await call.message.edit_text(text=text)
    admins = db.select_all_channel()
    buttons = InlineKeyboardMarkup(row_width=2)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[1]}", callback_data=f"delchanel:{admin[1]}"))

    buttons.add(InlineKeyboardButton(text="➕ Додати канал", callback_data="add_channel"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="delchanel:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    print(data[1])
    delete_orders = db.delete_channel(channel=data[1])
    await call.answer("🗑 Канал видалено!",show_alert=True)
    await call.message.edit_text("✅ Канал успішно видалено!", reply_markup=main_menu_for_super_admin)
# MAJBURIY OBUNA SOZLASH UCHUN

# ADMINLARNI KORISH
@dp.callback_query_handler(text="admins")
async def channel_list(call: types.CallbackQuery):
    royxat = db.select_admins()
    text = "🔰 Список АДМ:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[2]}\nID : {o[1]}💠 Імя: {o[2]}\n\n"
    await call.message.edit_text(text=text)

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)
# ADMINLARNI KORISH

# ПЕРЕГЛЯНУТИ СТАТИСТИКУ
@dp.callback_query_handler(text="statistics")
async def stat(call : types.CallbackQuery):
    stat = db.stat()
    for x in stat:
        dta = (x)
        datas = datetime.datetime.now()
        yil_oy_kun = (datetime.datetime.date(datetime.datetime.now()))
        soat_minut_sekund = f"{datas.hour}:{datas.minute}:{datas.second}"
        await call.message.delete()
        await call.message.answer(f"<b>👥 Користуються: {(x)} ПДП\n</b>"
                                  f"<b>⏰ Годин: {soat_minut_sekund}\n</b>"
                                  f"<b>📆 Дата: {yil_oy_kun}</b>",reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("◀️ Назад",callback_data="back_to_main_menu")))
# STATISKA KORISH UCHUN

# ADMINGA SEND FUNC
@dp.callback_query_handler(IsSuperAdmin(), text="send_message_to_admins", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Подати оголошення...\n"
                                 "або натисніть скасувати", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    users =  db.stat_admins()
    for x in users:
        await message.answer(f"📢 Почалася розсилка реклами...\n"
                             f"📊 Кількість АДМ: {x} ta\n"
                             f"🕒 Зачекайте...\n")
        user = db.select_all_admins()
        for i in user:
            user_id= i[1]
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                       message_id=message.message_id, caption=message.caption,
                                       reply_markup=message.reply_markup, parse_mode=types.ParseMode.MARKDOWN)

                time.sleep(0.5)
            except Exception as e:
                print(e)


        await message.answer("✅ Оголошення успішно відправлено!", reply_markup=main_menu_for_super_admin)
        await state.finish()
# ADMINGA SEND FUNC

# Foydalanuvchilar SEND FUNC
@dp.callback_query_handler(IsSuperAdmin(), text="send_advertisement", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Подати оголошення...\n"
                                 "або натисніть скасувати", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    users =  db.stat()
    for x in users:
        await message.answer(f"📢 Почалася розсилка реклами...\n"
                             f"📊 Кількість ПДП: {x} ta\n"
                             f"🕒 Зачекайте...\n")
        user = db.select_all_users()
        for i in user:
            user_id= i[1]
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                       message_id=message.message_id, caption=message.caption,
                                       reply_markup=message.reply_markup, parse_mode=types.ParseMode.MARKDOWN)

                time.sleep(0.5)
            except Exception as e:
                print(e)


        await message.answer("✅ Оголошення успішно відправлено!", reply_markup=main_menu_for_super_admin)
        await state.finish()
# Foydalanuvchilar SEND FUNC


@dp.callback_query_handler(IsSuperAdmin(), text="back_to_main_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="👨‍💻 Меню", reply_markup=main_menu_for_super_admin)
    await state.finish()

