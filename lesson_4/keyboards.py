from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


inline_buttons1 = [
    InlineKeyboardButton('Android',callback_data='inline_android'),
    InlineKeyboardButton('iOS',callback_data='inline_ios'),
    InlineKeyboardButton('BackEnd',callback_data='inline_backend'),
    InlineKeyboardButton('FrontEnd',callback_data='inline_frontend'),
    InlineKeyboardButton('UXUI',callback_data='inline_uxui'),
    InlineKeyboardButton('Записаться',callback_data='sign_up'),
]
inline = InlineKeyboardMarkup().add(*inline_buttons1)