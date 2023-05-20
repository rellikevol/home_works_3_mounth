from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import create_db, is_user_exist, append_user, append_number, append_location, \
    check_location_exist, set_title
from cheks import is_number
from datetime import datetime as dt

db_name = "users.db"

load_dotenv('.env')

bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)
button1 = InlineKeyboardButton(text='Отправить номер', callback_data='send_number')
button2 = InlineKeyboardButton(text='Отправить локацию', callback_data='send_location')
button3 = InlineKeyboardButton(text='Заказать еду', callback_data='order_food')
keyboard1 = InlineKeyboardMarkup(row_width=2).add(button1, button2, button3)


class States(StatesGroup):
    number = State()
    location = State()
    title = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    create_db(db_name)
    if not is_user_exist(db_name, message.from_user.id):
        append_user(db_name, message.from_user.first_name, message.from_user.last_name,
                    message.from_user.username, message.from_user.id)
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!', reply_markup=keyboard1)


@dp.callback_query_handler(text=['send_number'])
async def number(callbak: types.CallbackQuery):
    await bot.send_message(callbak.message.chat.id, "Введите ваш телефонный номер (без знака + и пробелов):")
    await States.number.set()


@dp.callback_query_handler(text=['send_location'])
async def location(callbak: types.CallbackQuery):
    await bot.send_message(callbak.message.chat.id, "Отправьте вашу локацию:")
    await States.location.set()


@dp.message_handler(content_types=['location'], state=States.location)
async def send_location(message: types.Message, state: FSMContext):
    append_location(db_name, message.from_user.id, message.location.longitude, message.location.latitude)
    await message.reply("Локация успешно добавлена!")
    await state.finish()
    await start(message)


@dp.message_handler(state=States.location)
async def send_location(message: types.Message, state: FSMContext):
    await message.reply("Это не похоже на локацию, поробуйте ещё раз...")
    await state.finish()
    await start(message)


@dp.message_handler(state=States.number)
async def send_number(message: types.Message, state: FSMContext):
    if is_number(message.text):
        append_number(db_name, message.text, message.from_user.id)
        await message.reply("Номер успешно сохранен!")
    else:
        await message.reply("Это не похоже на телефон, попробуйте ещё раз...")
    await state.finish()
    await start(message)


@dp.callback_query_handler(text=['order_food'])
async def order(callbak: types.CallbackQuery):
    if check_location_exist(db_name, callbak.from_user.id):
        await bot.send_message(callbak.from_user.id, "Напишите, что бы хотели заказать:")
        await States.title.set()
    else:
        await bot.send_message(callbak.from_user.id, "Вначале укажите ваше местоположение.")

@dp.message_handler(state=States.title)
async def send_number(message: types.Message, state: FSMContext):
    set_title(db_name, message.from_user.id, message.text, dt.now())
    await state.finish()
    await message.reply("Заказ оформлен!")
    await start(message)



executor.start_polling(dp, skip_updates=True)
