from datetime import date
import sqlite3
import hashlib


# Соединение с базой данных
def __db_connection() -> tuple:
    
    connect = sqlite3.connect(r"db\finance_hero.db")
    cursor = connect.cursor()
    return connect, cursor


# Регистрация нового пользователя
def register_new_user(username: int, password: str):

    # Соединение с базой данных
    connect, cursor = __db_connection()

    # Хеширование пароля пользователя
    password = __hash_password(password)

    # Проверка наличия регистрации ранее
    if __check_username(username, cursor):
        print('Начинаем проверку ранней регистрации')
        # Если найдено совпадение логина и пароля, то отправляется приветствие.
        # Если пароль не соответствует, то направляем сообщение о том, что логин занят.
        if __check_password(password, cursor):
            return f"Добро пожаловать"
        else:
            return f"Пароль не совпадает"

    # Запись данных о новом пользователе
    user = username, password, date.today()
    cursor.execute("INSERT INTO users (username, password, reg_data) VALUES(?, ?, ?);", user)
    connect.commit()
    connect.close()

    return f"Приятного использования"


# Проверка занятости имени пользователя
def __check_username(name: int, cursor: sqlite3.Cursor) -> bool:
    print('Зашли в проверку check_username')
    # Настройки для поиска
    result = False

    # Поиск по имени пользователя и пароля
    cursor.execute(f"SELECT * FROM users WHERE username == ?", (name, ))
    user_result = cursor.fetchone()

    # Проверка на наличие результата
    if user_result:
        result = True
    
    return result


# Проверка соответствия пароля
def __check_password(pswd: str, cursor: sqlite3.Cursor) -> bool:
    print('Зашли в проверку check_password')
    # Настройки для поиска
    result = False

    # Поиск по имени пользователя и пароля
    cursor.execute("SELECT * FROM users WHERE password == ?", (pswd, ))
    user_result = cursor.fetchone()

    # Проверка на наличие результата
    if user_result:
        result = True
    
    return result
    

# Хеширование пароля пользователя
def __hash_password(pswd: str):
     # Инициализация метода
     sha256 = hashlib.sha256()
     sha256.update(pswd.encode())
     pswd_hash = sha256.hexdigest()
     return pswd_hash


# Служебная функция записи приходной операции
def add_summa_to_db(username: str, summa: float, comment:str):
    connect, cursor = __db_connection()
    trans = username, summa, comment, date.today()
    cursor.execute("INSERT INTO income (username, profit, comment, data) VALUES(?, ?, ?, ?);", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} добавлена в раздел "Доходы"'


# Служебная функция записи расходной операции
def sub_summa_to_db(username: str, summa: float, comment:str):
    connect, cursor = __db_connection()
    trans = username, summa, comment, date.today()
    cursor.execute("INSERT INTO expense (username, spending, comment, data) VALUES(?, ?, ?, ?);", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} добавлена в раздел "Расходы"'