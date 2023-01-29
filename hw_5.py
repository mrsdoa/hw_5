import psycopg2
from psycopg2 import OperationalError

# функция удаления таблицы в бд - ВСЁ ОК
def delete_table(cur, query):
    cur.execute(query)

# функция создания бд - ОК
def create_db(cur, query):
    try:
        cur.execute(query)
        print("Database created successfully")
    except OperationalError as e:
        print(f'The error {e} occured')

# функция создания таблицы в бд - ВСЁ ОК
def create_table(cur, query):
    cur.execute(query)

def add_client(cur, first_name, last_name, email, phones=None):
    table_ins = """INSERT INTO clients_data2(client_id, name, surname, email, phones) VALUES (%s, %s, %s, %s, %s);""", (first_name, last_name, email, phones)
    cur.execute(table_ins)

# функция добавления номера телефона
def add_phone(cur, client_id, phone):
    insert_phone = """INSERT INTO clients_data phones=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(insert_phone)

# функция изменения информации о клиенте
def change_client(cur, client_id, name, surname, email, phones):
    changes = """UPDATE clients_data SET client_id=%s, name=%s, surname=%s, email=%s, phones=%s WHERE id=%s;""", (client_id, name, surname, email, phones)
    cur.execute(changes)

# функция удаления номера телефона
def delete_phone(cur, client_id, phone):
    delete_ = """DELETE FROM clients_data phone=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(delete_)

# функция удаления клиента
def delete_client(cur, client_id):
    delete_cl = """DELETE FROM clients_data name, surname, email, phones WHERE client_id=%s;""", (client_id)
    cur.execute(delete_cl)

# функция нахождения инфо о клиенте
# def find_client(cur, first_name=None, surname=None, email=None, phones=None):
#     select_cl = """SELECT * FROM clients_data WHERE name, surname, email, phones;""", (first_name, surname, email, phones)
#     cur.execute(select_cl)

def find_client(cur,):
    select_cl = """SELECT * FROM clients_data WHERE name=%s, surname=%s, email=%s, phones=%s;""", ()
    cur.execute(select_cl)

with psycopg2.connect(user="postgres", password="...", host="10.72.101.48", port="5432", ) as conn:
    with conn.cursor() as cur:

        if __name__ == "__main__":
            # создаём новую бд - ВСЁ ОК
            create_db_query = "CREATE DATABASE clients_db"
            create_db(cur, create_db_query)

            # функция удаления таблицы
            table_del = """
            DROP TABLE clients_data;"""
            delete_table(cur, table_del)

            # функция создания таблицы
            table1 = """CREATE TABLE IF NOT EXISTS clients_data(
                                        client_id INT PRIMARY KEY,
                                        name VARCHAR(40),
                                        surname VARCHAR(60),
                                        email VARCHAR(60),
                                        phones VARCHAR(60));"""
            create_table(cur, table1)

            # добавляем клиентов в таблицу
            natalia1 = add_client(cur, "Наталья", "Пугачева", "natalia.pugacheva@gmail.com", 89651381516)
            daria2 = add_client(cur, "Наталья", "Пугачева", "natalia.pugacheva@gmail.com", 89651381516)
            mikhail3 = add_client(cur, "Михаил", "Владимирович", "mishka.vladimir@mail.ru")

            # добавляем номер телефона
            natalia_2 = add_phone(cur, 1, 89089723345)

            # обновляем инфу по клиенту
            natalia = change_client(cur, 1, surname='Алексеева')

            # удаляем номер
            delete_ph1 = delete_phone(cur, 2, 89651381516)

            # удаляем клиента
            delete_cl1 = delete_client(cur, 3)

            # находим клиента
            find_cl1 = find_client(cur, name='Дарья')

conn.close()

