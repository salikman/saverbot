from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_for_super_admin = InlineKeyboardMarkup(row_width=2)

main_menu_for_super_admin.add(InlineKeyboardButton(text="➕ Додати канал", callback_data="add_channel"),
                              InlineKeyboardButton(text="➖ Видалити канал", callback_data="del_channel"),
                              InlineKeyboardButton(text="➕ Додати АДМ", callback_data="add_admin"),
                              InlineKeyboardButton(text="➖ Видалити АДМ", callback_data="del_admin"),
                              InlineKeyboardButton(text="👤 Адміністратори", callback_data="admins"),
                              InlineKeyboardButton(text="📝 Оголошення для АДМ",callback_data="send_message_to_admins"),
                              InlineKeyboardButton(text="📝 Оголошення для ПДП", callback_data="send_advertisement"),
                              InlineKeyboardButton(text="📊 Статистика", callback_data="statistics"),
                              )

main_menu_for_admin = InlineKeyboardMarkup(row_width=2)

main_menu_for_admin.add(InlineKeyboardButton(text="📊 Статистика", callback_data="stat"),
                              )

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main_menu")
        ]
    ]
)
