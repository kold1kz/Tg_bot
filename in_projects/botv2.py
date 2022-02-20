import logging
import asyncio
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from in_projects import keyboards as kb
from config import TOKEN
from sqlighter import SQLighter

from in_projects import utils
#from hltv import Hltv

#logging level set
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

#init bd
db=SQLighter('tb.db')




"""  НЕ ЗАВЕРШЕННЫЕ ВАРИАНТЫ """
#sg=Hltv('lastkey.txt')

'''image = BytesIO()

#Фото надо отправить в виде файла
@dp.message_handler(content_types=['document'])
async def photo_handler(message: types.Message):
    bytes = message.document.thumb.download(destination=image)
    
    #Вывод байт-обьекта
    print(bytes.read())

    #тип данных в переменной - io.BytesIO
    await message.answer(type(image))'''

##


'''@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')'''

""" КОНЕЦ НЕ ЗАВЕРШЕННЫХ ВАРИАНТОВ"""




@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Первый!', reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_2[0])
async def second_test_state_case_met(message: types.Message):
    await message.reply('Второй!', reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4)
async def third_or_fourth_test_state_case_met(message: types.Message):
    await message.reply('Третий или четвертый!', reply=False)

@dp.message_handler(state=TestStates.all())
async def some_test_state_case_met(message: types.Message):
    with dp.current_state(user=message.from_user.id) as state:
        text = MESSAGES['current_state'].format(
            current_state=await state.get_state(),
            states=TestStates.all()
        )
    await message.reply(text, reply=False)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


""" КНОПКИ НАЧАЛО  """

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb)

@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply("Первое - изменяем размер клавиатуры", reply_markup=kb.greet_kb1)

@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply("Второе - прячем клавиатуру после одного нажатия", reply_markup=kb.greet_kb2)

@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок", reply_markup=kb.markup3)

@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("Четвертое - расставляем кнопки в ряд", reply_markup=kb.markup4)

@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок", reply_markup=kb.markup5)

@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply("Шестое - запрашиваем контакт и геолокацию\nЭти две кнопки не зависят друг от друга", reply_markup=kb.markup_request)

@dp.message_handler(commands=['hi7'])
async def process_hi7_command(message: types.Message):
    await message.reply("Седьмое - все методы вместе", reply_markup=kb.markup_big)

@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)

'''@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")'''

""" КНОПКИ КОНЕЦ """

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler(commands=['give_site'])
async def give_my_site(message: types.Message):
    await message.reply("Держи ссылку на мой сайт: '...'")
    await bot.send_message(message.from_user.id, 'pravda ego eshe net v seti!') 

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)



async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        now = 'pidoras' #datetime.utcnow()
        lera='Ты самая красивая и умная девушка из всех кого я знаю! Ты словно ангел с небес, который слепит всех свой красотой и любовью, таких как ты  я никогда не встречал! Люблю!'
        await bot.send_message(263328753, f"{lera}",disable_notification=True)

if __name__ == "__main__":
    #asyncio.get_event_loop().run_until_complete(scheduled(10))
    # Запуск бота
    executor.start_polling(dp)