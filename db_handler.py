import datetime
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
    if __check_username(username):
        print('Начинаем проверку ранней регистрации')
        # Если найдено совпадение логина и пароля, то отправляется приветствие.
        # Если пароль не соответствует, то направляем сообщение о том, что логин занят.
        if __check_password(password):
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
def __check_username(name: int) -> bool:

    connect, cursor = __db_connection()

    print('Зашли в проверку check_username')
    # Настройки для поиска
    result = False

    # Поиск по имени пользователя и пароля
    cursor.execute(f"SELECT * FROM users WHERE username == ?", (name, ))
    user_result = cursor.fetchone()

    # Проверка на наличие результата
    if user_result:
        result = True

    connect.commit()
    connect.close()
    
    return result


# Проверка соответствия пароля
def __check_password(pswd: str) -> bool:

    connect, cursor = __db_connection()

    print('Зашли в проверку check_password')
    # Настройки для поиска
    result = False

    # Поиск по имени пользователя и пароля
    cursor.execute("SELECT * FROM users WHERE password == ?", (pswd, ))
    user_result = cursor.fetchone()

    # Проверка на наличие результата
    if user_result:
        result = True

    connect.commit()
    connect.close()
    
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
    # Проверка, регистрировался ли пользователь
    connect, cursor = __db_connection()
    if not __check_username(int(username)):
        return "Необходима регистрация"
    
    trans = username, summa, comment.lower(), date.today()
    cursor.execute("INSERT INTO income (username, profit, comment, data) VALUES(?, ?, ?, ?);", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} добавлена в раздел "Доходы"'



# Служебная функция записи расходной операции
def sub_summa_to_db(username: str, summa: float, comment:str):

    # Проверка, регистрировался ли пользователь
    connect, cursor = __db_connection()
    if not __check_username(int(username)):
        return "Необходима регистрация"
    
    trans = username, summa, comment.lower(), date.today()
    cursor.execute("INSERT INTO expense (username, spending, comment, data) VALUES(?, ?, ?, ?);", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} добавлена в раздел "Расходы"'



# Добавление финансовой цели в бд
def add_new_fingoal(username: str, new_fingoal: str):

    # Проверка, регистрировался ли пользователь
    connect, cursor = __db_connection()
    if not __check_username(int(username)):
        return "Необходима регистрация"
    
    summa, fingoal = tuple(new_fingoal.split('\n')[:2])
    trans = username, summa, fingoal, date.today()
    cursor.execute("INSERT INTO fingoals (username, summa, goal_info, data) VALUES(?, ?, ?, ?);", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} добавлена в раздел "Финансовая цель"'



# Выборка для пользователя его финансовых целей
def search_user_fingoals(username: str):

    connect, cursor = __db_connection()

    cursor.execute("SELECT goal_info, summa, progress FROM fingoals WHERE username=?", (username, ))
    user_goals = cursor.fetchall()
    print("Найдены цели", user_goals)
    result = __make_fingoals_str(user_goals)

    connect.commit()
    connect.close()

    return result


# Красивое оформление финцелей из бд:
def __make_fingoals_str(user_fingoals: list[tuple]):
    updown = "__________________________\n"
    title =  "    Сумма        |     Цель\n"
    result = updown + title + updown

    print(result)
    for elem in user_fingoals:
        goal, summa, progress = elem
        if progress == 1:
            progress = '✔️'
        else:
            progress = '💰'
        result = result + "\n" + progress + "      " + str(summa) + "      " + goal  +  "\n"
    
    result += updown

    return result


# Удаление финансовой цели
def del_fingoal(username: str, keyword: str):

    # Проверка, регистрировался ли пользователь
    connect, cursor = __db_connection()
    if not __check_username(int(username)):
        return "Необходима регистрация"
    
    summa, comment = __check_keyword(keyword)

    # Проверка, найдена ли сумма в ключе
    if summa == None:
        return comment
    
    trans = username, summa
    cursor.execute("DELETE FROM fingoals WHERE username=? AND summa=?", trans)
    connect.commit()
    connect.close()
    return f'Сумма {summa} удалена из раздела "Финансовая цель"'

    

# Удаление операции
def del_transaction(username: str, keyword: str):
    # Проверка, регистрировался ли пользователь
    
    if not __check_username(int(username)):
        return "Необходима регистрация"
    
    summa, comment = __check_keyword(keyword)

    # Проверка, найдена ли сумма в ключе
    if summa == None:
        return comment

    # Проверка в бд
    is_income = __search_in_income(username, summa)
    is_expense = __search_in_expense(username, summa)

    # Получение данных с бд
    table, data = __check_trans_type(is_income, is_expense)
    
    # Проверка комментария и удаление при совпадении
    if __comment_intersection(table, data, comment):
        __check_income_or_expense(table, username, summa)
        return f'Сумма {summa} была удалена из раздела "Операции"'
    else:
        return f"Операция не найдена"
    

# Проверка, какой тип операции, возвращает кортеж
def __check_trans_type(is_income: tuple, is_expense: tuple):
    if is_income == None and is_expense == None:
        return (None, [])
    if is_income == None:
        table, data = is_expense
    elif is_expense == None:
        table, data = is_income
    print("Проверка типа операции", table, data)
    return table, data
    


# Определение совпадения комментария
def __comment_intersection(table:str, data: str, comment: str):

    data = data.split(' ')
    comment = comment.split(' ')
    common_elem = []
    print("Определяем совпадение комментариев", comment)
    if len(comment) == 1:
        for elem in data:
            if elem == comment:
                return True
    for i in data:
        for j in comment:
            if i == j:
                common_elem.append(j)
    print("Общий элемент", common_elem)
    if len(common_elem) > 0:
        return True
    else:
        return False
    


# Вызов функции удаления в зависимости от тип операции
def __check_income_or_expense(table: str, username: str, summa: float):

    if table == 'expense':
        __delete_from_bd_expense(username, summa)
        
    if table == 'income':
        __delete_from_bd_income(username, summa)



# Проверка в таблице income
def __search_in_income(username:str, summa: float):
    
    trans = username, summa
    connect, cursor = __db_connection()
    result = None

    cursor.execute("SELECT profit, comment FROM income WHERE username=? AND profit=?", trans)
    income_result = cursor.fetchall()
    print("income_result:", income_result)
    if len(income_result) > 0:
        result = "income", income_result[0][1]

    connect.commit()
    connect.close()
    print("Результат поиска в таблице", result)

    return result


# Проверка в таблице expense
def __search_in_expense(username:str, summa: float):
    
    trans = username, summa
    connect, cursor = __db_connection()
    result = None
    
    cursor.execute("SELECT spending, comment FROM expense WHERE username=? AND spending=?", trans)
    expense_result = cursor.fetchall()
    print("expense_result:", expense_result)

    if len(expense_result) > 0:
        result = "expense", expense_result[0][1]
    
    connect.commit()
    connect.close()
    print("Результат поиска в таблице", result)

    return result
    

# Удаление в таблице income
def __delete_from_bd_income(username:str, summa: float):
    connect, cursor = __db_connection()
    trans = username, summa
    cursor.execute("DELETE FROM income WHERE username=? AND profit=?", trans)
    connect.commit()
    connect.close()


# Удаление в таблице expense
def __delete_from_bd_expense(username:str, summa: float):
    connect, cursor = __db_connection()
    trans = username, summa
    cursor.execute("DELETE FROM expense WHERE username=? AND spending=?", trans)
    connect.commit()
    connect.close()
    


# Проверка ключевого слова, поиск суммы из ключа
def __check_keyword(keyword: str):

    print(keyword, type(keyword))

    keyword = keyword.replace('!', '').lower()

    key_list = keyword.split('\n')

    print(key_list)

    for i in key_list:
        if i.isdigit():
            print(f"Возврат данных сумма {i},коммент {key_list[1]}")
            return float(i), key_list[1]
        else:
            return None, "🔴Сумма не найдена.\nВведите сумму для удаления.\n(Образец: !сумма\nкомментарий)"


# Обработка статистики
def show_statistic(username: str, period:int=1):

    data_tuple = __check_period(period)

    print("Указанный параметр:", data_tuple[0], "--", data_tuple[1])
    # Выборка из бд за нужный период
    expense_list = __search_db_time_expense(data_tuple[0], data_tuple[1], username)
    income_list = __search_db_time_income(data_tuple[0], data_tuple[1], username)

    # Представление данных в строку
    result = __make_trans_str(expense_list, income_list)

    return result

#Проверка периода статистики, возвращает кортеж
def __check_period(period: int):
    
    if period == 1:
        data = date.today(), date.today()

    if period == 30:
        current_data = date.today()
        next_data = __count_period()
        data = current_data, next_data
    
    return data


# Считает финальную дату для статистики за месяц
def __count_period():
    today = date.today()
    
    new_month = today.month
    new_year = today.year
    
    new_month = new_month + 1

    if new_month == 13:
        new_month = new_month - 12
        new_year += 1

    data = today.replace(year=new_year, month=new_month)
    return data


# Выборка из бд операций за указанный период expense
def __search_db_time_expense(data_start: datetime, data_finish: datetime, username: str):
    trans = username, data_start, data_finish
    connect, cursor = __db_connection()
    result = None
    
    cursor.execute("SELECT spending, comment FROM expense WHERE username=? AND data BETWEEN ? AND ?", trans)
    result = cursor.fetchall()
    connect.commit()
    connect.close()

    if len(result) == 0:
        return []
    
    print("Результат поиска в таблице expense", result)

    return result


# Выборка из бд операций за указанный период income
def __search_db_time_income(data_start: datetime, data_finish: datetime, username: str):
    trans = username, data_start, data_finish
    connect, cursor = __db_connection()
    result = None
    
    cursor.execute("SELECT profit, comment FROM income WHERE username=? AND data BETWEEN ? AND ?", trans)
    result = cursor.fetchall()
    connect.commit()
    connect.close()

    if len(result) == 0:
        return []
    
    print("Результат поиска в таблице income", result)

    return result



# Красивое оформление операций из бд:
def __make_trans_str(expense: list[tuple], income: list[tuple]):
    updown = "__________________________\n"
    title =  "    Сумма        |     Цель\n"
    result = updown + title + updown

    print(result)

    for elem in income:
        summa, comment = elem
        result = result + '\n' + '🟢' + str(summa) + '         ' + comment + '\n' + updown

    for elem in expense:
        summa, comment = elem
        result = result + '\n' + '🔴' + str(summa) + '         ' + comment + '\n' + updown

    return result
