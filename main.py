import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile
from loguru import logger

from config import bot_token


bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


main_menu_message = '<b>Главное меню</b>'
main_menu_keyboard = InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text="Пицца", callback_data="Pizza")],
                                                   [InlineKeyboardButton(text="Наш номер телефона", callback_data="Phone"),
                                                   InlineKeyboardButton(text="Наш сайт", callback_data="Website")]]).as_markup()
photo = FSInputFile('images/logo.jpg')


def get_pizza_menu() -> str:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM pizza")
    pizzas = cursor.fetchall()
    conn.close()
    pizza_menu = "<b><i>Меню пиццы:</i></b>\n\n"
    for pizza in pizzas:
        pizza_menu += f"<b>- {pizza[0]}</b>\n\n"
    return pizza_menu

def get_pizza_menu_kb() -> InlineKeyboardBuilder:
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM pizza")
    pizzas = cursor.fetchall()
    conn.close()
    pizza_menu_keyboard = InlineKeyboardBuilder()
    for pizza in pizzas:
        pizza_menu_keyboard.add(InlineKeyboardButton(text=pizza[0], callback_data=f"Pizza_{pizza[0]}"))
    pizza_menu_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="Main"))
    return pizza_menu_keyboard.adjust(3).as_markup()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    logger.debug("Стартовое сообщение от пользователя {}".format(message.from_user.id))
    await message.delete()
    await message.answer(
        "<b>Привет!</b>\n\nЯ бот для заказов блюд в пиццерии Бобо Пицца! Для заказа выберите нужное вам блюдо в меню:"    
    )
    await message.answer_photo(caption=main_menu_message, photo=photo, reply_markup=main_menu_keyboard)

@dp.callback_query(F.data == "Pizza")
async def pizza_menu_callback_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(get_pizza_menu(), reply_markup=get_pizza_menu_kb())

@dp.callback_query(F.data.startswith("Pizza_"))
async def go_to_pizza_callback_handler(callback: CallbackQuery) -> None:
    pizza_name = callback.data.split("_")[1]
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pizza WHERE name=?", (pizza_name,))
    pizza = cursor.fetchone()
    conn.close()
    
    order_keyboard = InlineKeyboardBuilder()
    order_keyboard.add(InlineKeyboardButton(text="Заказать", callback_data=f"Order_{pizza_name}"))
    order_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="Pizza"))
    
    await callback.answer()
    await callback.message.answer_photo(caption=f"<b>{pizza[1]}</b>\n\n<i>{pizza[2]}</i>\n\n<b>Цена: {pizza[3]} руб.</b>", photo=FSInputFile(pizza[4]), reply_markup=order_keyboard.as_markup())
    

@dp.callback_query(F.data.startswith("Order_"))
async def order_pizza_callback_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Теперь пришлите свой номер телефона!")

@dp.message(F.text.regexp(r'^\+\d{8,15}$'))
async def user_phone_number_handler(message: Message) -> None:
    phone_number = message.text
    logger.debug(f"Получен номер телефона: {phone_number}")
    await message.answer(f"Спасибо! Ваш номер телефона: {phone_number} принят. Скоро вам позвонит оператор для уточнения заказа.")

@dp.callback_query(F.data.startswith("Phone"))
async def phone_number_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Наш номер телефона: +7 xxx xx xx")

@dp.callback_query(F.data.startswith("Website"))
async def website_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Наш сайт: bobopizza.com")

@dp.callback_query(F.data.startswith("Main"))
async def main_menu_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer_photo(caption=main_menu_message, photo=photo, reply_markup=main_menu_keyboard)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
