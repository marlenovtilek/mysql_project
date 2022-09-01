from email.message import Message
from bot_config import TOKEN 
from aiogram import Bot,Dispatcher,executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state  import StatesGroup, State
from sql.category_manager import Category
from sql.product_manager import Product
import mysql.connector
from sql.config import *
from random import choice
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

storage= MemoryStorage()


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


def get_connection():
    try:
        connect = mysql.connector.connect(
            host=DATABASE_HOST,
            user= DATABASE_USER,
            password=DATABASE_PASSWORD,
            db = DATABASE_NAME,
            autocommit=True,
        )
    except  Exception as e:
        print("Соединение с базой не установлена.")
        exit(0)
    return connect

class ProductState(StatesGroup):
    name = State()


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu = types.KeyboardButton("Категории")
address = types.KeyboardButton("Адрес")
contact = types.KeyboardButton("Контакты")
random = types.KeyboardButton("Рандом")
search =  types.KeyboardButton("Поиск")
markup.row(menu)
markup.row(search,random)
markup.row(address)
markup.row(contact)

@dp.message_handler(commands=['start'])
async def welcome_message(message: types.Message):
        
    await message.answer("Привет.", reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def welcome_message(message: types.Message):
    if message.text == "Категории":
        text = "Выберите категорию:"
        connect = get_connection()
        cursor = connect.cursor()
        category = Category(cursor)
        categories = category.get_all_categories()
        inline_markup = types.InlineKeyboardMarkup()
        for i in categories:
            button = types.InlineKeyboardButton(
                i[1], 
                callback_data=f"category_{i[0]}"
            )
            inline_markup.add(button)

        await message.answer(text, reply_markup=inline_markup)
    elif message.text == "Адрес":
        lon = "74.595894" 
        lat = "42.878893"
        await message.answer_location(lat, lon)
        await message.answer("Мы находимся по адресу:\nРыскулова 79Б г.Бишкек")
    elif message.text == "Контакты":
        text = """
            Наши контакты: 0999134494, 0705009922
            Вебсайт: itrun.kg
        """
        await message.answer(text)
    elif message.text == "Рандом":
        connect = get_connection()
        cursor = connect.cursor()
        product = Product(cursor)
        data_ids = product._get_all_ids()
        ids = [id[0] for id in data_ids]
        print(ids)
        r_id = choice(ids)
        data = product.get_product_by_id(r_id)
        await message.answer(data[1])
    elif message.text == "Поиск": 
        await message.answer("Напишите название продукта: ")
        await ProductState.name.set()
    
# @dp.register_message_handler(welcome_message, state=ProductState.name)
# async def product_search(message: types.Message, state: Message):
#     name = state.get_data()
#     print(name)
#     await message.answer("Поиск....")

        

@dp.callback_query_handler(lambda c: str(c.data).startswith("category_") )
async def get_product_by_category(callback: types.CallbackQuery):
    id = int(callback.data[-1])
    connect = get_connection()
    cursor = connect.cursor()
    product = Product(cursor)
    products_data = product.get_products_by_category(id)
    inline_markup = types.InlineKeyboardMarkup()
    for i in products_data:
        button = types.InlineKeyboardButton(i[1], callback_data=f"product_{i[0]}")
        inline_markup.add(button)
    back = types.InlineKeyboardButton("Назад", callback_data="back_category")
    inline_markup.add(back)

    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text("Выберите категорию", reply_markup=inline_markup)

@dp.callback_query_handler(lambda c: str(c.data).startswith("product_"))
async def get_product(callback: types.CallbackQuery):
    product_id = callback.data.split("_")[-1]
    product_id = int(product_id) 
    connect = get_connection()
    cursor = connect.cursor()
    product = Product(cursor)
    data = product.get_product_by_id(product_id)
    message_text = f"""
        Название:{data[1]}
        Категория: {data[5]}
        Описание:{data[2]}
        Цена: {data[4]}сом
    """
    
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("Назад", callback_data="back_products")
    markup.add(back)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text(message_text, reply_markup=markup)


@dp.callback_query_handler(lambda c: str(c.data).startswith("back_"))
async def get_back(callback):
    data = callback.data.split("_")[1]
    if data == "category":
        await callback.message.edit_text("Возвращаемся в категории...")
    elif data == "products":
        await callback.message.edit_text("Возвращаемся в список продуктов...")



if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)