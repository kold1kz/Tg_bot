from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Эти значения далее будут подставляться в итоговый текст, отсюда 
# такая на первый взгляд странная форма прилагательных
available_time_citys = ["Москва", "Санкт-петербург", "Крым", "Урал"]
#available_time_zone = ["", "среднюю", "большую"]

class OrderCity(StatesGroup):
    waiting_for_time_citys = State()


async def city_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_time_citys:
        keyboard.add(name)
    await message.answer("Выберите ваш город:", reply_markup=keyboard)
    await OrderCity.waiting_for_time_citys.set()

# Обратите внимание: есть второй аргумент
async def city_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_time_citys:
        await message.answer("Пожалуйста, выберите ваш город, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
''' for size in available_food_sizes:
        keyboard.add(size)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await OrderFood.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)'''

def register_handlers_city(dp: Dispatcher):
    dp.register_message_handler(city_start, commands="food", state="*")
    dp.register_message_handler(city_chosen, state=OrderCity.waiting_for_time_citys)