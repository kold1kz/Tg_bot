from asyncio.windows_events import NULL
import datetime
import logging
import asyncio

from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import menu as nav
from config import TOKEN
from sqlighter import SQLighter
from back import weather, TestStates
from datetime import datetime


#logging level set
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
#init bd
db=SQLighter('tb.db')



@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    if (weather.get_weather(message.text))!="☠ Пожалуйста проверь написанние своего города ☠":
        db.add_city(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, "Cохранил твой город))", reply_markup=nav.mainMenu)
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
    else:
        await bot.send_message(message.from_user.id,"Ошибка: город написан не правильно или его нет в базе данных")

@dp.message_handler(state=TestStates.TEST_STATE_2)
async def first_test_state_case_met(message: types.Message):
    try:
        if (len(message.text)==5 and int(message.text[:2])>-1 and int(message.text[:2]) < 25 and int(message.text[3:]) >-1 and int(message.text[3:]) <61): 
            db.set_time(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Теперь в это время тебе будет приходить прогноз погоды на день))", reply_markup=nav.mainMenu)
            db.update_subscription(message.from_user.id, True)
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
            
            if (db.get_user_city(message.from_user.id)[0][0]==0):
                await bot.send_message(message.from_user.id, "Выберите свой город", reply_markup = nav.cityMenu)
    
        else:
            await bot.send_message(message.from_user.id, "Некорректно введено время, пожалуйста, введите правильное время")
            state = dp.current_state(user=message.from_user.id)
            argument=2
            await state.set_state(TestStates.all()[int(argument)])

    except:
        await bot.send_message(message.from_user.id,"Ошибка в объявении времени")
    



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}!\nЭтот бот преднозначен для отправки прогноза погоды на день.\nНастоятельно  прошу использовать специальную клавиатура, дабы бот работал корректно, спасибо! '.format(message.from_user), reply_markup=nav.timeMenu)
    await bot.send_message(message.from_user.id, "Выберите время рассылки в формате HH:MM")
    if (not db.subscriber_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.add_name(message.from_user.first_name, message.from_user.id)

@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    if (db.get_user_city(message.from_user.id)==False):
        await bot.send_message(message.from_user.id, 'Выбери город в котором ты проживаешь', reply_markup=nav.cityMenu)
    await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text =='Lera':
        await bot.send_message(message.from_user.id, "Поздравляю, ты нашел пасхалку!\n\nЛера- этой прекрасной девушке повезло получить от меня в голову мячом!)")


    elif message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)
        

    elif message.text == 'Выбрать город':
        await bot.send_message(message.from_user.id, "Выберите свой город", reply_markup = nav.cityMenu)

    elif message.text=="Вывести погоду": 
        if (db.subscriber_exists(message.from_user.id)):
            await bot.send_message(message.from_user.id, weather.get_weather(db.get_user_city(message.from_user.id)[0][0]),)
        else:
            await bot.send_message(message.from_user.id, "Вы не установлии свой город, это можно сделать в меню 'Настройки'")    

    elif message.text=="Ввести свой город": 
        await message.reply("Введите свой город!", reply_markup=nav.ReplyKeyboardRemove())
        state = dp.current_state(user=message.from_user.id)
        argument=1
        await state.set_state(TestStates.all()[int(argument)])   
    
    elif message.text == 'Москва':
        db.add_city(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, "Cохранил твой город)", reply_markup = nav.mainMenu)

    elif message.text == 'Питер':
        db.add_city(message.from_user.id, 'Санкт петербург')
        await bot.send_message(message.from_user.id, "Cохранил твой город)", reply_markup = nav.mainMenu)

    elif message.text == 'Севастополь':
        db.add_city(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, "Cохранил твой город)", reply_markup = nav.mainMenu)

    elif message.text=='Настройки':
        await bot.send_message(message.from_user.id, "Меню настройки", reply_markup=nav.settingMenu)
    

    elif message.text == '06:00':
        db.set_time(message.from_user.id, message.text)
        if (db.get_user_city(message.from_user.id)[0][0]==0):
            await bot.send_message(message.from_user.id, 'Выбери город в котором ты проживаешь', reply_markup=nav.cityMenu)
        else:
            await bot.send_message(message.from_user.id, "Cохранил твое время)", reply_markup = nav.mainMenu)

    elif message.text == '07:00':
        db.set_time(message.from_user.id, message.text)
        if (db.get_user_city(message.from_user.id)[0][0]==0):
            await bot.send_message(message.from_user.id, 'Выбери город в котором ты проживаешь', reply_markup=nav.cityMenu)
        else:
            await bot.send_message(message.from_user.id, "Cохранил твое время)", reply_markup = nav.mainMenu)

    elif message.text == '08:00':
        db.set_time(message.from_user.id, message.text)
        if (db.get_user_city(message.from_user.id)[0][0]==0):
            await bot.send_message(message.from_user.id, 'Выбери город в котором ты проживаешь', reply_markup=nav.cityMenu)
        else:
            await bot.send_message(message.from_user.id, "Cохранил твое время)", reply_markup = nav.mainMenu)

    elif message.text == 'Ввести свое время':
        await message.reply("Введите время в форамте: HH:MM", reply_markup=nav.ReplyKeyboardRemove())
        db.update_subscription(message.from_user.id, True)
        state = dp.current_state(user=message.from_user.id)
        argument=2
        await state.set_state(TestStates.all()[int(argument)])
        

    elif message.text=='Подписаться на рассылку':
        if (not db.get_suba(message.from_user.id)):
            db.add_subscriber(message.from_user.id)
        else:
            db.update_subscription(message.from_user.id, True)
        await message.reply("Вы успешно подписались на рассылку!\nТеперь каждый день вы будете полуать прогноз погоды на день!", reply_markup=nav.mainMenu)

    elif message.text=='Отписаться от рассылки':
        if (db.get_suba(message.from_user.id)):
            db.update_subscription(message.from_user.id, False)
            await message.reply("Жаль что ты уходиш, мне было очень приятно видеть тебя у себя в коде(", reply_markup=nav.mainMenu)
        else:
            await message.reply("Сори но у тебя нет подписки.")

    elif message.text=='Выбрать время рассылки':
        await message.reply("Введите время в форамте: HH:MM", reply_markup=nav.ReplyKeyboardRemove())
        db.update_subscription(message.from_user.id, True)
        state = dp.current_state(user=message.from_user.id)
        argument=2
        await state.set_state(TestStates.all()[int(argument)])

    else:
        await message.reply("Такой команды не существует или кнопка еще не реализована!\nВыберите команду")


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        time=str(datetime.now())[11:16]
        for user in db.get_subscriptions():
            if user[5]==time:
                await bot.send_message(user[1], weather.get_weather(user[4]), disable_notification=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(60))
    # Запуск бота
    executor.start_polling(dp, skip_updates =True, on_shutdown=shutdown)
    db.close() 