from aiogram import Bot, Dispatcher, types, executor
from random import randint
from decouple import config

KEY = config('KEY', cast=str)
depth = 3
numbers = [str(i) for i in range(1, depth + 1)]

bot = Bot(KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await message.answer(f"Привет, {message.from_user.first_name}! "
                         f"Я загадал число от 1 до {depth}, попробуете отгадать?")


@dp.message_handler()
async def start(message: types.message):
    num = randint(1, depth)
    if message.text in numbers:
        if int(message.text) == num:
            await message.reply("Вы отгадали!")
        else:
            await message.reply(f"Не отгадали, это было число {num}!")
    else:
        await message.reply("Извините, я вас не понял...")


executor.start_polling(dp)
