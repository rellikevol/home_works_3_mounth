from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import articles, messages

load_dotenv('.env')
bot = Bot(os.environ.get('KEY'))
dp = Dispatcher(bot)

keyboard2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Назад', callback_data='start'))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    prev = messages()
    keyboard1 = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i in articles():
        buttons.append(InlineKeyboardButton(text=i[0], callback_data=i[0]))
    keyboard1.add(*buttons)
    await bot.send_photo(message.chat.id, prev[0][2], caption=prev[0][1], reply_markup=keyboard1)


@dp.callback_query_handler()
async def ansewr_line(callbak: types.CallbackQuery):
    for i in articles():
        if callbak.data == i[0]:
            await bot.send_photo(callbak.message.chat.id, i[3], caption=i[2], reply_markup=keyboard2)
            await callbak.answer()
    if callbak.data == 'start':
        await start(callbak.message)
        await callbak.answer()


executor.start_polling(dp)
