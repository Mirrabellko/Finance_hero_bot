#https://mastergroosha.github.io/aiogram-3-guide/messages/
#https://habr.com/ru/articles/732136/
#https://www.youtube.com/watch?v=qRyshRUA0xM&ab_channel=%24sudoteachIT%E2%9A%99%EF%B8%8F
# https://docs.aiogram.dev/en/latest/
# https://www.youtube.com/watch?v=qfNRbyvx5Uo&ab_channel=PythonHubStudio   удаление сообщений
# https://www.youtube.com/watch?v=b_m4Bk1sLwA&ab_channel=PythonHubStudio посмотреть с этого

import asyncio
import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject

from config import TOKEN as tkn
import data_handler as dh
import db_handler as dbh
from handlers.menu_low import menu_low
from handlers.menu_work_db import menu_work_db

# Установить уровень логирования
logging.basicConfig(level=logging.INFO)


# Создание экземпляра бота
# Можно сразу указать здесь parse_mode="HTML"
bot = Bot(token=tkn, parse_mode='HTML')
# Создание экземпляра диспетчера
dp = Dispatcher()
# Импорт роутеров, где хранятся обработчики
dp.include_routers(menu_low, menu_work_db)




# Запуск процесса поллинга новых апдейтов
async def main():
    bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Exit")

# Подумать, надо ли создавать меню после авторизации. Нужна очистка меню, а потом при успешной авторизации отправка меню