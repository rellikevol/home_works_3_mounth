from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging, sqlite3, time
from keyboards import inline
from states import SignUpState

load_dotenv('.env')

bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
database = sqlite3.connect('telegram.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created VARCHAR(200)
);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS signup(
    user_id INT,
    name VARCHAR(255),
    tel VARCHAR(13),
    email VARCHAR(255),
    created VARCHAR(200)
);
""")
cursor.connection.commit()
logging.basicConfig(level=logging.INFO)


@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'inline_android':
        await android(call.message)
    elif call.data == 'inline_ios':
        await ios(call.message)
    elif call.data == 'inline_backend':
        await backend(call.message)
    elif call.data == 'inline_frontend':
        await frontend(call.message)
    elif call.data == 'inline_uxui':
        await uxui(call.message)
    elif call.data == 'sign_up':
        await sign_up(call.message)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cursor = database.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.username}',
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{time.ctime()}'
        )""")
        cursor.connection.commit()
    await message.answer(f'Привет, {message.from_user.first_name}! '
                         f'Я могу вам дать информацию о наших направлениях в сфере IT , стоимость курса, месяц обучения',
                         reply_markup=inline)


@dp.message_handler(commands=['android'])
async def android(message: types.Message):
    await message.answer(
        f'Android-разработчик - это специалист, который занимается созданием приложений и программного обеспечения для операционной системы Android. Он использует язык программирования Java, Kotlin или другие языки, поддерживаемые платформой Android\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
        reply_markup=inline)


@dp.message_handler(text=['/cancel'], )
async def video_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Можете посмотерть другие направление.', reply_markup=keyboard1)


@dp.message_handler(commands=['ios'])
async def ios(message: types.Message):
    await message.answer(
        f'iOS-разработчик - это специалист, который занимается разработкой приложений для устройств, работающих под управлением операционной системы iOS, разработанной компанией Apple. iOS-разработчик использует язык программирования Swift или Objective-C и инструменты разработки, предоставляемые Apple, такие как Xcode и т.д.\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
        reply_markup=inline)


@dp.message_handler(commands=['backend'])
async def backend(message: types.Message):
    await message.answer(
        f'Backend-разработчик - это специалист, который занимается созданием и поддержкой серверной части программного обеспечения. Он отвечает за разработку и поддержку логики, обработку данных и взаимодействие с базами данных \nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
        reply_markup=inline)


@dp.message_handler(commands=['frontend'])
async def frontend(message: types.Message):
    await message.answer(
        f'Frontend-разработчик - это специалист, который занимается разработкой пользовательского интерфейса (UI) веб-приложений. Он отвечает за создание визуальной части приложения, с которой взаимодействует пользователь.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
        reply_markup=inline)


@dp.message_handler(commands=['uxui'])
async def uxui(message: types.Message):
    await message.answer(
        f'UX/UI разработчик (User Experience/User Interface) занимается проектированием и разработкой пользовательского интерфейса (UI) и опыта пользователя (UX) для различных цифровых продуктов, таких как мобильные приложения, веб-сайты, программное обеспечение и другие интерактивные системы.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
        reply_markup=inline)


@dp.message_handler(commands=['sign_up'])
async def sign_up(message: types.Message):
    await message.answer("Укажите свои данные")
    await message.answer("Ваше имя:")
    await SignUpState.name.set()


@dp.message_handler(state=SignUpState.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Телефонный номер в формате +996:")
    await SignUpState.tel.set()


@dp.message_handler(state=SignUpState.tel)
async def get_number(message: types.Message, state: FSMContext):
    if len(message.text) == 13 and message.text[1:].isdigit() and message.text[0] == "+":
        await state.update_data(tel=message.text)
        await message.answer("Почта:")
        await SignUpState.email.set()
    else:
        await message.answer("Неправильный формат")


@dp.message_handler(state=SignUpState.email)
async def get_email(message: types.Message, state: FSMContext):
    if '@' in message.text:
        await state.update_data(email=message.text)
        await message.answer("OK")
        user_data = await storage.get_data(user=message.from_user.id)
        await bot.send_message(-947291422, f"Имя: {user_data['name']} телефон: {user_data['tel']} email {user_data['email']}")
        cursor = database.cursor()
        cursor.execute(f"""INSERT INTO signup VALUES(
            {message.from_user.id},
            '{user_data['name']}',
            '{user_data['tel']}',
            '{user_data['email']}',
            '{time.ctime()}'
        );""")
        cursor.connection.commit()
        await message.answer("Ваши данные успешно сохранены")
    else:
        await message.answer("Неправильная почта")


executor.start_polling(dp, skip_updates=True)