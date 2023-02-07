import psycopg2
from psycopg2 import OperationalError


# функция создания БД
def create_db(cur, query):
    try:
        cur.execute(query)
        print("Database created successfully")
    except OperationalError as e:
        print(f'The error {e} occured')
# функция удаления таблицы в БД
def delete_table(cur, query):
    cur.execute(query)
# функция создания таблицы в БД
def create_table(cur, query):
    cur.execute(query)
def add_client(cur, name, surname, email, phones=None):
    table_ins = """INSERT INTO clients_data(name, surname, email, phones) VALUES (%s, %s, %s, %s)""", {'name': name,
                                                                                                       'surname': surname,
                                                                                                       'email': email,
                                                                                                       'phones': phones}
    cur.execute(table_ins)
    records = cur.fetchone()
    print(records)
# функция добавления номера телефона
def add_phone(cur, client_id, phone):
    insert_phone = """INSERT INTO clients_data phones=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(insert_phone)

# функция изменения информации о клиенте
def change_client(cur, client_id, name=None, surname=None, email=None, phones=None):
    cur.execute("""UPDATE clients_data SET 
    (name=%(name)s OR %(name)s IS NULL) 
    AND (surname=%(surname)s OR %(surname)s IS NULL)
    AND (email=%(email)s OR %(email)s IS NULL)
    AND (phones=%(phones)s OR %(phones)s IS NULL) WHERE client_id=%s;""", {'client_id': client_id, 'name': name, 'surname': surname, 'email': email, 'phones': phones})
    # cur.execute(changes, input_data)

def find_client(cur, name=None, surname=None, email=None, phones=None):
    cur.execute("""SELECT * FROM clients_data
            WHERE (name=%(name)s OR %(name)s IS NULL)
            AND (surname=%(surname)s OR %(surname)s IS NULL)
            AND (email=%(email)s OR %(email)s IS NULL)
            AND (phones=%(phones)s OR %(phones)s IS NULL)""",
                {'name': name, 'surname': surname, 'email': email, 'phones': phones})
    records = cur.fetchall()
    print(records)

# функция удаления номера телефона
def delete_phone(cur, client_id, phone):
    delete_ = """DELETE FROM clients_data phone=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(delete_)

# функция удаления клиента
def delete_client(cur, client_id):
    delete_cl = """DELETE FROM clients_data name, surname, email, phones WHERE client_id=%s;""", (client_id)
    cur.execute(delete_cl)

# функция нахождения инфо о клиенте
def find_client(cur, name=None, surname=None, email=None, phones=None):
    cur.execute("""SELECT * FROM clients_data
            WHERE (name=%(name)s OR %(name)s IS NULL)
            AND (surname=%(surname)s OR %(surname)s IS NULL)
            AND (email=%(email)s OR %(email)s IS NULL)
            AND (phones=%(phones)s OR %(phones)s IS NULL)""",
                {'name': name, 'surname': surname, 'email': email, 'phones': phones})
    records = cur.fetchall()
    print(records)

# ORRRRRRRRRRRRRR
# def find_client(cur, **kwargs):
#
#     filds = ('name', 'surname', 'email', 'phones')
#
#     for key, value in kwargs.items():
#         if key not in filds:
#             return "[ERROR] fields not found"
#
#     tuple_fields_values = tuple(zip(kwargs.keys(), kwargs.values()))
#
#     comprehension_fields_values = [f'{x[0]}={x[1]}' for x in tuple_fields_values]
#
#     fields_values = ' and '.join(comprehension_fields_values)
#
#     cur.execute(f"""SELECT name, surname, email, phones FROM clients_data c
#                     JOIN phones p on p.client_id = c.client_id WHERE {fields_values}""")
#     info = cur.fetchall()
#
#     if info:
#         return f"[INFO]: found successful: {info}"
#     else:
#         return f"[INFO]: client not found"


if __name__ == "__main__":
    with psycopg2.connect(user="postgres", password="z9MxveD1Xwiv", host="10.72.101.48", port="5432", ) as conn:
        with conn.cursor() as cur:
            # создаём новую бд - ВСЁ ОК
            create_db_query = "CREATE DATABASE clients_db"
            create_db(cur, create_db_query)
            # функция удаления таблицы
            table_del = """DROP TABLE clients_data;"""
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
            add_client(cur, 'Наталья', 'Пугачева', 'natalia.pugacheva@gmail.com', '89651381516')
            add_client(cur, "Дарья", "Лукина", "daria.lukina@gmail.com", "89636533814")
            add_client(cur, "Михаил", "Владимирович", "mishka.vladimir@mail.ru")
            # добавляем номер телефона
            natalia_2 = add_phone(cur, 1, 89089723345)
            # обновляем инфу по клиенту
            change_client(cur, 'Алексеева') 
            # удаляем номер
            delete_ph1 = delete_phone(cur, 2, 89651381516)
            # удаляем клиента
            delete_cl1 = delete_client(cur, 3)
            # находим клиента
            find_cl1 = find_client(cur, 'Дарья')
