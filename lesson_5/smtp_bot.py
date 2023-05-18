from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton
from smtp import is_email, check_len, send_mail

MESSAGE_LIMIT = 250
SUB_LIMIT = 100

load_dotenv('.env')

bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)

class StatesForEmail(StatesGroup):
    email = State()
    subject = State()
    text = State()


keyboard1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Отправить сообщение',
                                                            callback_data='send_email'))
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Этот бот может отправить письмо на email, который вы укажете.',
                         reply_markup=keyboard1)

@dp.message_handler(text=['/cancel'], state=StatesForEmail.all_states)
async def cancel_enter(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Операция отменена...", reply_markup=types.ReplyKeyboardRemove())
    await start(message)
@dp.callback_query_handler(text=['send_email'])
async def start_send(callbak: types.CallbackQuery):
    await bot.send_message(callbak.message.chat.id, "Введите e-mail:", reply_markup=keyboard2)
    await StatesForEmail.email.set()

@dp.message_handler(state=StatesForEmail.email)
async def set_subject(message: types.Message, state: FSMContext):
    if is_email(message.text):
        await state.update_data(email=message.text)
        await message.answer(f"Укажите тему письма, ограничение {SUB_LIMIT} символов.")
        await StatesForEmail.subject.set()
    else:
        await message.reply("Это не похоже на email адрес. Попробуйте ещё раз...")

@dp.message_handler(state=StatesForEmail.subject)
async def set_text(message: types.Message, state: FSMContext):
    if check_len(message.text, SUB_LIMIT):
        await state.update_data(subject=message.text)
        await message.answer(f"Укажите текст письма, ограничение {MESSAGE_LIMIT} символов.")
        await StatesForEmail.text.set()
    else:
        await message.reply(f"Тема письма превышает ограничение в {SUB_LIMIT} символов. "
                            f"Попробуйте ещё раз...")

@dp.message_handler(state=StatesForEmail.text)
async def final(message: types.Message, state: FSMContext):
    if check_len(message.text, MESSAGE_LIMIT):
        await message.answer("Отправляем письмо...")
        await state.update_data(text=message.text)
        res = await storage.get_data(user=message.from_user.id)
        if send_mail(res['text'], res['subject'], res['email']):
            await message.answer("Письмо отправлено!", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Что-то пошло не так... Письмо не отправлено. Попробуете ещё раз?"
                                 , reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        await start(message)
    else:
        await message.reply(f"Текст письма превышает ограничение в {MESSAGE_LIMIT} символов. "
                            f"Попробуйте ещё раз...")


executor.start_polling(dp, skip_updates=True)