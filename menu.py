from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain=KeyboardButton('Главное меню')
btnLera=KeyboardButton('Lera')

# --- main menu ----
btnOutput = KeyboardButton('Вывести погоду в моем городе')
btnSettings = KeyboardButton('Настройки')
btnHelp =KeyboardButton('Помощь')
mainMenu =ReplyKeyboardMarkup(resize_keyboard=True).add(btnOutput, btnSettings, btnHelp)

# --- City menu ---
btnInputcity=KeyboardButton('Ввести свой город')
btnMsc = KeyboardButton('Москва')
btnSpb=KeyboardButton('Питер')
btnSevas =KeyboardButton('Севастополь')
cityMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnMsc, btnSpb, btnSevas, btnInputcity, btnMain)

# --- setting menu ---
btnTimeset=KeyboardButton('Выбрать время рассылки')
btnSub=KeyboardButton('Подписаться на рассылку')
btnUnsub=KeyboardButton('Отписаться от рассылки')
btnCity = KeyboardButton('Выбрать город')
settingMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnSub, btnUnsub, btnCity, btnTimeset, btnMain)