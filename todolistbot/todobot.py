from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging, asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from keyboards import basic_menu, task_delay_keyboard, days_menu, delete_cancel
from cheks import check_numbers, interval_limit, days_check, time_check, text_limit, text_check
import uuid
from database import create_db, insert, user_tasks, delete, all_tasks
from tasking import schedule_, kill_task, schedule_start

load_dotenv('.env')

bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)

dbname = 'users.db'
create_db(dbname)


class StatesForToDo(StatesGroup):
    type = State()
    interval = State()
    text = State()
    time_for_day = State()


class StatesForDelete(StatesGroup):
    tag = State()


@dp.message_handler(text=['/start'])
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Этот бот поможет Вам создать напиминания.",
                         reply_markup=basic_menu)


@dp.message_handler(text=['Добавить напоминание'])
async def add(message: types.Message):
    await StatesForToDo.type.set()
    await message.answer("Выберите тип напоминания.", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Задать периодичность:", reply_markup=task_delay_keyboard)


@dp.callback_query_handler(text=['delay_cancel'], state=StatesForToDo.type)
async def delay_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback.message.chat.id, "Отмена")
    await start(callback.message)


@dp.callback_query_handler(text=['in_seconds', 'in_days', 'in_minute'], state=StatesForToDo.type)
async def add_type(callback: types.CallbackQuery, state: FSMContext):
    calls = ['in_seconds', 'in_days', 'in_minute']
    if callback.data in calls:
        if callback.data == calls[0]:
            await state.update_data(type='in_seconds')
            await bot.send_message(callback.message.chat.id, "Укажите периодичность напоминания в секундах:")
            await StatesForToDo.interval.set()
        elif callback.data == calls[1]:
            await state.update_data(type='in_days')
            await bot.send_message(callback.message.chat.id, "Выберите день для напоминания:", reply_markup=days_menu)
        elif callback.data == calls[2]:
            await state.update_data(type='in_minute')
            await bot.send_message(callback.message.chat.id, "Укажите периодичность напоминания в минутах:")
        await StatesForToDo.interval.set()
    else:
        await bot.send_message(callback.message.chat.id, "Я вас не понимаю...")


@dp.message_handler(state=StatesForToDo.interval)
async def add_interval(message: types.Message, state: FSMContext):
    res = await storage.get_data(user=message.from_user.id)
    if res['type'] in ['in_seconds', 'in_minute']:
        if check_numbers(message.text):
            await state.update_data(interval=message.text)
            await message.answer(f"Введите текст напоминания (ограничение {text_limit} символов):")
            await StatesForToDo.text.set()
        else:
            await message.reply(f"Введённое значение не число либо превышает лимит в {interval_limit}."
                                f"Попробуйте ещё раз...")
    else:
        if days_check(message.text):
            await state.update_data(interval=message.text)
            await message.answer("Введите время напоминания (например, 14:30):", reply_markup=ReplyKeyboardRemove())
            await StatesForToDo.time_for_day.set()
        else:
            await message.reply(f"Это не похоже на день недели. Попробуйте ещё раз...")


@dp.message_handler(state=StatesForToDo.time_for_day)
async def add_day_time(message: types.Message, state: FSMContext):
    if time_check(message.text):
        await state.update_data(time_for_day=message.text)
        await message.answer(f"Введите текст напоминания (ограничение {text_limit} символов):")
        await StatesForToDo.text.set()
    else:
        await message.reply(f"Я вас не понял. Введите время в формате HH:MM")


@dp.message_handler(state=StatesForToDo.text)
async def add_message(message: types.Message, state: FSMContext):
    if text_check(message.text):
        await state.update_data(text=message.text)
        res = await storage.get_data(user=message.from_user.id)
        tag = str(uuid.uuid4()) + '_' + str(message.from_user.id)
        if res['type'] == 'in_days':
            insert(dbname, message.from_user.id, message.chat.id, res['type'],
                   res['interval'], res['text'], res['time_for_day'], tag)
            schedule_(res['type'], res['interval'], res['text'], message.chat.id, tag, bot, res['time_for_day'])
        else:
            insert(dbname, message.from_user.id, message.chat.id, res['type'],
                   res['interval'], res['text'], 'None', tag)
            schedule_(res['type'], int(res['interval']), res['text'], message.chat.id, tag, bot)
        await message.answer("Уведомление добавлено!")
        await state.finish()
        await start(message)
    else:
        await message.reply(f"Этот текст больше ограничения в {text_limit} символов. Попробуйте ещё раз...")


@dp.message_handler(text=['Удалить напоминание'])
async def add(message: types.Message):
    res = user_tasks(dbname, message.from_user.id)
    if len(res) == 0:
        await message.answer("Пока не одной задачи нет...")
    else:
        await message.answer("Нажмите на удалить, чтобы удалить напоминание:", reply_markup=delete_cancel)
        for x, i in enumerate(res):
            button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Удалить', callback_data=i[6]))
            if i[2] == 'in_seconds':
                await message.answer(f"Напоминание {x + 1}:\n"
                                     f"Период в секундах: {i[3]}\n"
                                     f"Сообщение:\n"
                                     f"{i[4]}", reply_markup=button)
            if i[2] == 'in_minute':
                await message.answer(f"Напоминание {x + 1}:\n"
                                     f"Период в минутах: {i[3]}\n"
                                     f"Сообщение:\n"
                                     f"{i[4]}", reply_markup=button)
            if i[2] == 'in_days':
                await message.answer(f"Напоминание {x + 1}:\n"
                                     f"День: {i[3]}\n"
                                     f"Время: {i[5]}\n"
                                     f"Сообщение:\n"
                                     f"{i[4]}", reply_markup=button)
        await StatesForDelete.tag.set()


@dp.message_handler(text=['Отмена'], state=StatesForDelete.tag)
async def add(message: types.Message, state: FSMContext):
    await message.answer("Отмена...", reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await start(message)


@dp.callback_query_handler(state=StatesForDelete.tag)
async def add_type(callback: types.CallbackQuery, state: FSMContext):
    if kill_task(callback.data):
        delete(dbname, callback.data)
        await bot.send_message(state.chat, "Напоминание удалено!")
    else:
        await bot.send_message(state.chat, "Это напоминание уже было удалено ранее...")


def startup():
    res = all_tasks(dbname)
    if len(res) > 0:
        loop = asyncio.get_event_loop()
        for i in res:
            if i[2] in ['in_seconds', 'in_minute']:
                schedule_start(i[2], i[3], i[4], i[0], i[6], bot, loop)
            if i[2] in ['in_days']:
                schedule_start(i[2], i[3], i[4], i[0], i[6], bot, loop, i[5])


executor.start_polling(dp, skip_updates=True, on_startup=startup())
