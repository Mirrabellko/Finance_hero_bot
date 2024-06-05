import db_handler as dbh
import data_handler as dh

from aiogram.types import Message, CallbackQuery
from aiogram import types, F, Router
from aiogram.filters.command import Command, CommandObject


menu_low = Router()

# Обработчик команды /start
@menu_low.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("<b>Привет. Какой у тебя пароль?💸</b>\n\nПри первичном запуске система его запомнит.\nНеобходимо отправить по следующему образцу:\n(Образец: =пароль)")


# Обработчик основного меню
@menu_low.callback_query(F.data == 'work_menu')
async def reg_new_user(callback: CallbackQuery):
    await callback.answer('Приятного использования💝', show_alert=True)
    kb = dh.make_work_menu()
    add_info = '\n\nДля добавления операции используйте формат:\n✔️\n + сумма\nкомментарий\n<b>или</b>\n❌\n - сумма\nкомментарий'
    await callback.message.edit_text(add_info, reply_markup=kb)



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
async def view_fingoals(callback: CallbackQuery):
    user_id = callback.from_user.id
    result = dbh.search_user_fingoals(user_id)
    await callback.message.reply(result, reply_markup=dh.reply_workmenu())


# Отправка клавиатуры статистики
@menu_low.callback_query(F.data == 'statistic_kb')
async def show_userstat_kb(callback: CallbackQuery):
    await callback.message.edit_text("Выбери, за какой период❓", reply_markup= dh.statistic_keyboard())


# Отправка клавиатуры меню удаления
@menu_low.callback_query(F.data == 'delete')
async def add_new_fingoal(callback: CallbackQuery):
    await callback.message.edit_text("Что хочешь удалить?☠️\nВведи сумму и комментарий к ней.\n(Образец: !сумма\nкомментарий)")



# Отправка статистики за текущий день
@menu_low.callback_query(F.data == "today_stat")
async def show_userstat_day(callback: CallbackQuery):
    print("Отлов статистики сегодня")
    user_id = callback.from_user.id
    result = dbh.show_statistic(user_id)
    await callback.message.reply(result, reply_markup=dh.reply_workmenu())



# Отправка статистики за месяц
@menu_low.callback_query(F.data == "month_stat")
async def show_userstat_month(callback: CallbackQuery):
    print("Отлов статистики месяц")
    user_id = callback.from_user.id
    period = 30
    result = dbh.show_statistic(user_id, period)
    await callback.message.reply(result, reply_markup=dh.reply_workmenu())

