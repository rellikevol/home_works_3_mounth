from parce import get_quote
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv('.env')

bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class StatesForCurrency(StatesGroup):
    currency = State()
    value = State()


keyboard1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('RUB/KGS', callback_data='RUB'),
                                                  InlineKeyboardButton('USD/KGS', callback_data='USD'),
                                                  InlineKeyboardButton('KZT/KGS', callback_data='KZT'))


@dp.message_handler(text=['/start'])
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name} этот поможет тебе поменять валюту! "
                         f"Выбери, что хочешь поменять:", reply_markup=keyboard1)
    await StatesForCurrency.currency.set()


@dp.callback_query_handler(text=['RUB', 'USD', 'KZT'], state=StatesForCurrency.currency)
async def currency(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "Введите, сколько KGS вы хотите поменять:")
    await state.update_data(currency=callback.data)
    await StatesForCurrency.value.set()


@dp.message_handler(state=StatesForCurrency.value)
async def value(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        res = await storage.get_data(user=message.from_user.id)
        price = get_quote(res['currency'])
        if not price['response']:
            await message.reply("Котировки не загрузились, попробуйте ввести сумму ещё раз...")
        else:
            value_kgs = float(message.text)
            price_kgs = float(price['price'].replace(',', '.'))
            await message.answer(f'Цена одного {res["currency"]} {round(price_kgs, 2)} KGS.\n'
                                 f'За {value_kgs} KGS вы получите '
                                 f'{round(value_kgs / price_kgs, 2)} {res["currency"]}.')
            await state.finish()
            await start(message)
    else:
        await message.reply("Это не число, попробуйте ещё раз...")


executor.start_polling(dp, skip_updates=True)
