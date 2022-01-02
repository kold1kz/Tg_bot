from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btnMain=KeyboardButton('Главное меню')
btnLera=KeyboardButton('Lera')

# --- Main menu ----
btnOutput = KeyboardButton('Вывести погоду')
btnSettings = KeyboardButton('Настройки')
btnHelp =KeyboardButton('Помощь')
mainMenu =ReplyKeyboardMarkup(resize_keyboard=True).add(btnOutput, btnSettings, btnHelp)

# --- City menu ---
btnInputcity=KeyboardButton('Ввести свой город')
btnMsc = KeyboardButton('Москва')
btnSpb=KeyboardButton('Питер')
btnSevas =KeyboardButton('Севастополь')
cityMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnMsc, btnSpb, btnSevas, btnInputcity, btnMain)

# --- Time menu---
btnInputTime=KeyboardButton('Ввести время')

# --- Setting menu ---
btnTimeset=KeyboardButton('Выбрать время рассылки')
btnSub=KeyboardButton('Подписаться на рассылку')
btnUnsub=KeyboardButton('Отписаться от рассылки')
btnCity = KeyboardButton('Выбрать город')
settingMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnSub, btnUnsub, btnCity, btnTimeset, btnMain)