import db_handler as dbh
import data_handler as dh

from aiogram.types import Message, CallbackQuery
from aiogram import types, F, Router
from aiogram.filters.command import Command, CommandObject


menu_low = Router()

# Обработчик команды /start
@menu_low.message(Command('start'))
async def send_welcome(message: types.Message):
    kb = dh.make_register_keyboard()
    await message.answer("<b>Привет. Что желаешь?💸</b>", reply_markup=kb)


# Обработчик новой регистрации
@menu_low.callback_query(F.data == 'new_user')
async def reg_new_user(callback: CallbackQuery):
    await callback.answer('Начинаем регистрацию', show_alert=True)
    await callback.message.edit_text("Придумай свой пароль. \nНеобходимо отправить по следующему образцу \n(Образец: =пароль)")


# Обработчик возврата в главное меню
@menu_low.callback_query(F.data == 'start')
async def start_menu(callback: CallbackQuery):
    await callback.edit_text('Главное меню', show_alert=True)
    await send_welcome(callback.message)


# Обработчик входа в систему
@menu_low.callback_query(F.data == 'old_user')
async def start_menu(callback: CallbackQuery):
    await callback.answer('Вспоминай свой пароль', show_alert=True)
    await callback.message.edit_text("Введи свой пароль по образцу. \n(Образец: =пароль)")
