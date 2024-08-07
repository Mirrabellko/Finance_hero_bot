from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types



# Клавиатура, которая передается при старте
def make_register_keyboard():
    reg_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вход в систему', callback_data='old_user')],
        [InlineKeyboardButton(text='Регистрация', callback_data='new_user')]
        #[InlineKeyboardButton(text='<--', callback_data='start')]
    ])
    return reg_kb


# Клавиатура, которая передается после успешной авторизации/регистрации
def make_work_menu():
    start_work_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Статистика за ...', callback_data='statistic_kb')],
        [InlineKeyboardButton(text='Мои финансовые цели', callback_data='user_fingoal')],
        [InlineKeyboardButton(text='Поставить новую цель', callback_data='add_fingoal')],
        [InlineKeyboardButton(text='Удаление ...', callback_data='delete')],
        [InlineKeyboardButton(text='<--', callback_data='start')]
    ])
    
    return start_work_kb


# Клавиатура, которая дает выбор периода для статистики
def statistic_keyboard():
    statistic_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сегодня', callback_data='today_stat')],
        [InlineKeyboardButton(text='Месяц', callback_data='month_stat')],
        [InlineKeyboardButton(text='<--', callback_data='work_menu')]
    ])
    return statistic_kb


# Клавиатура, которая дает выбор удаления. Доступные опции: проводка, финансовая цель
def detele_keyboard():
    delete_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Операция', callback_data='del_trans')],
        [InlineKeyboardButton(text='Финансовая цель', callback_data='del_fingoal')],
        [InlineKeyboardButton(text='<--', callback_data='work_menu')]
    ])
    return delete_kb


# Клавиатура главного меню
def reply_workmenu():
    #btn = KeyboardButton("Главное меню")
    #reply_kb = ReplyKeyboardMarkup(keyboard=[btn], resize_keyboard=True, one_time_keyboard=True)
    reply_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Главное меню')]
    ], resize_keyboard=True)
    return reply_kb