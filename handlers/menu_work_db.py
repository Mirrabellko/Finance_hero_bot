import db_handler as dbh
import data_handler as dh

from aiogram.types import Message, CallbackQuery
from aiogram import types, F, Router
from aiogram.filters import Command, CommandObject, or_f


menu_work_db = Router()


# Обработчик логина и пароля
@menu_work_db.message(F.text.contains("=") or F.data == 'work_menu')
async def check_login_pass(message: types.Message):
    try:
        user_id = message.from_user.id
        password = message.text.split('=')[1]

        print(f'{user_id} логин для регистрации')
        print(f'{password} пароль для регистрации')

        result = dbh.register_new_user(user_id, password)
        
        if result != "Пароль не совпадает":

            add_info = '\n\nДля добавления операции используйте формат:\n✔️\n + сумма\nкомментарий\n<b>или</b>\n❌\n - сумма\nкомментарий'
            await message.answer(f"{result+add_info}", reply_markup=dh.make_work_menu())
        else:
            await message.answer(f"{result}\nПопробуй еще раз! Образец: =пароль")
    except ValueError:
        await message.answer("Попробуй еще раз! Образец: =пароль")
        


# Обработчик добавления дохода, формат +100.50\nкомментарий
@menu_work_db.message(F.text.contains("+"))
async def insert_to_db_income(message: types.Message):
    user_id = message.from_user.id
    summa, comment = message.text.split('\n')
    summa = float(summa.replace('+', '').replace(',', '.').replace(' ', ''))
    result = dbh.add_summa_to_db(user_id, summa, comment)
    await message.answer(f"{result}", reply_markup=dh.reply_workmenu())



# Обработчик добавления расхода, формат -100.50\nкомментарий
@menu_work_db.message(F.text.contains("-"))
async def insert_to_db_expense(message: types.Message):
    user_id = message.from_user.id
    summa, comment = message.text.split('\n')
    summa = float(summa.replace('-', '').replace(',', '.').replace(' ', ''))
    result = dbh.sub_summa_to_db(user_id, summa, comment)
    await message.answer(f"{result}", reply_markup=dh.reply_workmenu())


# Обработчик основного меню
@menu_work_db.message(F.text == "Главное меню")
async def reg_new_user(message: types.Message):
    await message.answer('Возврат в меню📜', show_alert=True)
    kb = dh.make_work_menu()
    add_info = '\n\nДля добавления операции используйте формат:\n✔️\n + сумма\nкомментарий\n<b>или</b>\n❌\n - сумма\nкомментарий'
    await message.answer(add_info, reply_markup=kb)



# Добавление новой финансовой цели, формат сумма\nкомментарий
@menu_work_db.message(F.text.contains("%"))
async def add_new_fingoal(message: types.Message):
    print('Отработал отлов %')
    user_id = message.from_user.id
    fingoal = message.text.replace("%", "")
    result = dbh.add_new_fingoal(user_id, fingoal)
    await message.answer(f"{result}", reply_markup = dh.make_work_menu())



# Удаление финансовой цели или операции. Формат !сумма\nкомментарий
@menu_work_db.message(F.text.contains("!"))
async def delete_trans_or_fingoal(message: types.Message):
    print('Отработал отлов !')
    user_id = message.from_user.id

    # Проверка, является ли указанная сумма операцией
    result = dbh.del_fingoal(user_id, message.text)
    
    # Проверка, является ли казанная сумма финансовой целью
    result = dbh.del_transaction(user_id, message.text)

    await message.answer(f"{result}", reply_markup = dh.make_work_menu())



# Обработчик отлова без ключевого символа
@menu_work_db.message(F.text)
async def no_key_data_answer(message: types.Message):
    await message.answer("Забыл указать ключевой символ⛔")