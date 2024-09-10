# Домашнее задание по теме "План написания админ панели".
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

import sqlite3

def initiate_db():
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()
    # создаём таблицу Products, если она ещё не создана при помощи SQL запроса
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    )
    ''')
    # создаём таблицу Users, если она ещё не создана при помощи SQL запроса
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()  # сохраняем состояние
    connection.close()  # закрываем соединение

initiate_db() # Инициируем функцию

# def insert_products(): # Заполняем базу4-мя записями
#     connection = sqlite3.connect('data_products.db')
#     cursor = connection.cursor()
#     for i in range(1, 5):
#         cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
#                        (f"Продукт {i}", f"Описание {i}", i*100))
#
#     connection.commit()  # сохраняем состояние
#     connection.close()  # закрываем соединение
#
# insert_products()

# add_user - Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000
def add_user(username, email, age):
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()
    # check_user = cursor.execute("SELECT * FROM Users WHERE username = username_u")
    #
    # if check_user.fetchone() is None:
    cursor.execute(f'''
    INSERT INTO Users (username, email, age, balance)
    VALUES (?, ?, ?, ?)
    ''', (username, email, age, 1000))

    connection.commit()  # сохраняем состояние
    connection.close()  # закрываем соединение

# is_included(username) - принимает имя пользователя и возвращает True, если такой пользователь есть в
# таблице Users, в противном случае False.
def is_included(username):
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()

    # Проверяем, есть ли пользователь с таким именем в таблице Users
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.close()
    return user is not None # Возвращаем True, если пользователь существует, иначе False

# def delete_records(): # Удаляем записи с id с 5 по 16
#     connection = sqlite3.connect('data_products.db')
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM Products WHERE id BETWEEN 5 AND 16")
#     connection.commit() # сохраняем состояние
#     connection.close() # закрываем соединение
#
# delete_records()

def get_all_products(): # возвращаем все записи из таблицы Products, полученные при помощи SQL запроса.
    connection = sqlite3.connect('data_products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    for product in products:
        id, title, description, price = product  # Распаковываем кортеж
        print(f"ID: {id} | Наименование: {title} | Описание: {description} | Цена: {price}")

    connection.close()  # закрываем соединение
    return products

#get_all_products()



# connection.commit() # сохраняем состояние
# connection.close() # закрываем соединение