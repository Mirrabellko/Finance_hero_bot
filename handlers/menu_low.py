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
    await callback.message.edit_text("Придумай свой пароль. \nНеобходимо отправить по следующему образцу:\n(Образец: =пароль)")


# Обработчик возврата в главное меню
@menu_low.callback_query(F.data == 'start')
async def start_menu(callback: CallbackQuery):
    await callback.message.edit_text('Главное меню', show_alert=True)
    await send_welcome(callback.message)


# Обработчик входа в систему
@menu_low.callback_query(F.data == 'old_user')
async def password_menu(callback: CallbackQuery):
    await callback.answer('Вспоминай свой пароль', show_alert=True)
    await callback.message.edit_text("Введи свой пароль по образцу:\n(Образец: =пароль)")


# Обработчик выбора постановки новой цели
@menu_low.callback_query(F.data == 'add_fingoal')
async def fingoal_menu(callback: CallbackQuery):
    await callback.message.edit_text('Введи свою финансовую цель по следующему образцу:\n(Образец:\n%сумма\nкомментарий)')
    


# Предоставить информацию ою уже созданных финансовых целях
@menu_low.callback_query(F.data == 'user_fingoal')
async def add_new_fingoal(callback: CallbackQuery):
    pass


# Отправка клавиатуры статистики
@menu_low.callback_query(F.data == 'statistic_kb')
async def add_new_fingoal(callback: CallbackQuery):
    pass


# Отправка клавиатуры меню удаления
@menu_low.callback_query(F.data == 'delete')
async def add_new_fingoal(callback: CallbackQuery):
    await callback.message.edit_text("Что хочешь удалить?☠️\nВведи сумму и комментарий к ней.\n(Образец: !сумма\nкомментарий)")



# Отправка статистики за выбранный период
@menu_low.callback_query(F.text.contains("_stat"))
async def add_new_fingoal(callback: CallbackQuery):
    pass


