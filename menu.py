from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btnMain=KeyboardButton('Главное меню')
btnLera=KeyboardButton('Lera')

# --- Main menu ----
btnOutput_allday = KeyboardButton('Вывести погоду на день')
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

# --- Time button---
btnInputTime=KeyboardButton('Ввести время')

# ---- Time menu ---
btnTime_Fi=KeyboardButton("06:00")
btnTime_Se=KeyboardButton("07:00")
btnTime_Th=KeyboardButton("08:00")
btnInput_My_Time=KeyboardButton('Ввести свое время')
timeMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime_Fi, btnTime_Se, btnTime_Th, btnInput_My_Time)

# --- Setting menu ---
btnTimeset=KeyboardButton('Выбрать время рассылки')
btnSub=KeyboardButton('Подписаться на рассылку')
btnUnsub=KeyboardButton('Отписаться от рассылки')
btnCity = KeyboardButton('Выбрать город')
settingMenu=ReplyKeyboardMarkup(resize_keyboard=True).add(btnSub, btnUnsub, btnCity, btnTimeset, btnMain)