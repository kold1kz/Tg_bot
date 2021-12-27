import logging
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import menu as nav
from config import TOKEN
from sqlighter import SQLighter
from back import weather

#logging level set
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=TOKEN)

# Диспетчер для бота
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

#init bd
db=SQLighter('tb.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}!\nЭтот бот преднозначен для отправки прогноза погоды на день.\nНастоятельно  прошу использовать специальную клавиатура, дабы бот работал корректно, спасибо! '.format(message.from_user), reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text =='Lera':
        await bot.send_message(message.from_user.id, "Поздравляю, ты нашел пасхалку!\n\nЛера- этой прекрасной девушке повезло получить от меня в голову мячом!)")

    elif message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)

    elif message.text == 'Выбрать город':
        await bot.send_message(message.from_user.id, "Выберите свой город", reply_markup = nav.cityMenu)

    elif message.text=="Вывести погоду в моем городе": 
        await bot.send_message(message.from_user.id, weather.get_weather(db.get_user_city(message.from_user.id)[0][0]),)
    
    elif message.text == 'Москва':
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, False)
            await message.reply("Сори но у тебя нет подписки, если хочешь подписаться, нажми на определенную кнопку в настройках")
        else:
            db.add_city(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Cохранил твой город)")

    elif message.text == 'Питер':
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, False)
            await message.reply("Сори но у тебя нет подписки, если хочешь подписаться, нажми на определенную кнопку в настройках")
        else:
            db.add_city(message.from_user.id, 'Санкт петербург')
            await bot.send_message(message.from_user.id, "Cохранил твой город)")

    elif message.text == 'Севастополь':
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, False)
            await message.reply("Сори но у тебя нет подписки, если хочешь подписаться, нажми на определенную кнопку в настройках")
        else:
            db.add_city(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Cохранил твой город)")

    elif message.text=="Ввести свой город": 
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, False)
            await message.reply("Сори но у тебя нет подписки, если хочешь подписаться, нажми на определенную кнопку в настройках", )
        else:
            if (weather.get_weather(message.text)):
                db.add_city(message.from_user.id, message.text)
                await bot.send_message(message.from_user.id, "Cохранил твой город)")
            else:
                await bot.send_message(message.from_user.id,"Ошибка: город написан не правильно или его нет в базе данных")

    elif message.text=='Настройки':
        await bot.send_message(message.from_user.id, "Меню настройки", reply_markup=nav.settingMenu)
    
    elif message.text=='Подписаться на рассылку':
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id)
        else:
            db.update_subscription(message.from_user.id, True)
        await message.reply("Вы успешно подписались на рассылку!\nТеперь каждый день вы будете полуать прогноз погоды на день!")

    elif message.text=='Отписаться от рассылки':
        if (not db.subscriber_exists(message.from_user.id)):
            db.add_subscriber(message.from_user.id, False)
            await message.reply("Сори но у тебя нет подписки.")
        else:
            db.update_subscription(message.from_user.id, False)
            await message.reply("Жаль что ты уходиш, мне было очень приятно видеть тебя у себя в коде(")
    elif message.text=='Выбрать время рассылки':
        pass

    else:
        await message.reply("Такой команды не существует или кнопка еще не реализована!\nВыберите команду")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates =True)
