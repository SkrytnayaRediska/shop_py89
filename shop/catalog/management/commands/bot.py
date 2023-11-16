from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from django.conf import settings
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from catalog.models import Category
import json
import requests


class SomeState(StatesGroup):
    waiting_for_text = State()


bot = Bot(token=settings.TELEGRAM_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_categories = KeyboardButton('Categories')
button_cart = KeyboardButton('Show User Cart')
keyboard.add(button_categories)
keyboard.add(button_cart)


@sync_to_async()
def get_categories():
    return list(Category.objects.all())


@dp.message_handler(commands=['help', 'start'])
async def command_helper(message: types.Message):
    await message.answer("Input some message", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Categories')
async def show_categories(msg: types.Message):
    categories = await get_categories()
    msg_to_answer = ''
    for cat in categories:
        msg_to_answer += (f"Category: {cat.name}\n"
                          f"Description: {cat.description}\n"
                          f"-----------------------------------------\n")
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(Text('Show User Cart'))
async def ask_for_credentials(message: types.Message):
    await message.reply("Enter login and password divided by only ',' (Ex.: login,password)")
    await SomeState.waiting_for_text.set()


@dp.message_handler(state=SomeState.waiting_for_text)
async def show_user_cart(message: types.Message, state: FSMContext):
    msg_text = message.text
    login, password = msg_text.split(',')
    data = {
        "email": login,
        "password": password
    }
    response = requests.post('http://127.0.0.1:8000/users/auth/jwt/create',
                             data=json.dumps(data),
                             headers={
                                 "Content-Type": "application/json"
                             })
    if response.status_code == 200:
        token = json.loads(response.content)['access']
        response = requests.get('http://127.0.0.1:8000/catalog/basket/',
                                headers={
                                    "Authorization": f"Bearer {token}"
                                })
        user_cart_data = json.loads(response.content)
        if user_cart_data:
            msg_to_answer = ''
            products = user_cart_data['products']
            for prod in products:
                msg_to_answer += f"Product: {prod['name']}, count: {prod['count']}\n"
            msg_to_answer += f"Result price: {user_cart_data['result_price']}"
            await bot.send_message(message.chat.id, msg_to_answer)
        else:
            await bot.send_message(message.chat.id, 'You cart is empty')
    else:
        await bot.send_message(message.chat.id, "Can't authorize")
    await state.finish()


@dp.message_handler()
async def query_telegram(message: types.Message):
    await bot.send_message(message.chat.id, "Understandable, have a nice day!")


class Command(BaseCommand):
    help = 'Test TG bot'

    def handle(self, *args, **options):
        executor.start_polling(dp)
