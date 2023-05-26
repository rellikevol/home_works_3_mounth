from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton


add_task = KeyboardButton("Добавить напоминание")
del_task = KeyboardButton("Удалить напоминание")
basic_menu = ReplyKeyboardMarkup(resize_keyboard=True)
basic_menu.add(add_task, del_task)

add_sec = InlineKeyboardButton("В секундах", callback_data='in_seconds')
add_minute = InlineKeyboardButton("В минутах", callback_data='in_minute')
add_day = InlineKeyboardButton("По дням недели", callback_data='in_days')
cancel = InlineKeyboardButton("Отмена", callback_data='delay_cancel')
task_delay_keyboard = InlineKeyboardMarkup(row_width=2).add(add_sec, add_minute, add_day, cancel)

days_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Понедельник"),
    KeyboardButton("Вторник"),
    KeyboardButton("Среда"),
    KeyboardButton("Четверг"),
    KeyboardButton("Пятница"),
    KeyboardButton("Суббота"),
    KeyboardButton("Воскресенье"),
)

delete_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отмена"))



