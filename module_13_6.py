import asyncio
import logging
import aiogram

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery

from pip import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

buttons = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                         KeyboardButton(text='Информация')]],resize_keyboard=True)
in_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas'),
                                                   InlineKeyboardButton(text='Рассчитать норму калорий',
                                                                        callback_data='calories')]],resize_keyboard=True)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=buttons)
    print('Привет! Я бот помогающий твоему здоровью.')



async def start():
    await dp.start_polling(bot)

class UserState(StatesGroup):
    #(возраст, рост, вес)
    age = State()
    growth = State()
    weight = State()

@dp.message(F.text == 'Рассчитать')
async def main_menu(message:Message):
    await message.answer('Выберите опцию:',reply_markup=in_button)

@dp.callback_query(F.data == 'formulas')
async def get_formulas(callback:CallbackQuery):
    await callback.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")


@dp.callback_query(F.data == 'calories')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    norma = int(data['weight'])*10 + int(data['growth'])* 6.25 - int(data['age'])*5-161
    await message.answer(f'Ваша норма калорий в сутки: {norma}')
    await state.clear()

@dp.message()
async def cmd_not_start(message: Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('exit')

#  module_13_6.py