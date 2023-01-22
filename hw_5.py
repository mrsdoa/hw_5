import psycopg2
from psycopg2 import OperationalError

conn = psycopg2.connect(user="postgres", password="...", host="10.72.101.48", port="5432")
cur = conn.cursor()
conn.autocommit = True

# -------------------------------------------------------------
# функция создания бд
def create_db(conn, query):
    cur = conn.cursor()
    try:
        cur.execute(query)
        print("Database created successfully")
    except OperationalError as e:
        print(f'The error {e} occured')
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция создания таблицы в бд - ВСЁ ОК
def create_table(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция добавления клиентов в таблицу
def add_client(conn, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    insert_query = """INSERT INTO clients_data (client_id, name, surname, email, phones) VALUES (%s, %s, %s, %s, %s);""", (first_name, last_name, email, phones)
    cur.execute(insert_query)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция добавления номера телефона
def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    insert_phone = """INSERT INTO clients_data phones=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(insert_phone)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция изменения информации о клиенте
def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    cur = conn.cursor()
    changes = """UPDATE clients_data SET client_id=%s, name=%s, surname=%s, email=%s, phones=%s WHERE id=%s;""", (client_id, name, surname, email, phones)
    cur.execute(changes)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция удаления номера телефона
def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    delete_ = """DELETE FROM clients_data phone=%s WHERE client_id=%s;""", (client_id, phone)
    cur.execute(delete_)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция удаления клиента
def delete_client(conn, client_id):
    cur = conn.cursor()
    delete_ = """DELETE FROM clients_data name, surname, email, phones WHERE client_id=%s;""", (client_id)
    cur.execute(delete_)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------

# -------------------------------------------------------------
# функция нахождения инфо о клиенте
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    select_ = """SELECT * FROM clients_data WHERE name=%s, surname=%s, email=%s, phones=%s;""", (first_name, last_name, email, phone)
    cur.execute(select_)
    conn.commit()
    cur.execute("SELECT * FROM client_data")
    record = cur.fetchone()
    print("Резульат", record)
# -------------------------------------------------------------


# -------------------------------------------------------------
# создаём новую бд - ВСЁ ОК
create_db_query = "CREATE DATABASE clients_db"
create_db(conn, create_db_query)

# -------------------------------------------------------------
# создаём таблицу со столбцами
create_table_query = """CREATE TABLE IF NOT EXISTS clients_data(
                            client_id INT PRIMARY KEY,
                            name VARCHAR(40),
                            surname VARCHAR(60),
                            email VARCHAR(60),
                            phones VARCHAR(60));"""
create_table(conn, create_table_query)

# -------------------------------------------------------------
# добавляем клиентов в таблицу
natalia1 = add_client(conn, "Наталья", "Пугачева", "natalia.pugacheva@gmail.com", 89651381516)
daria2 = add_client(conn, "Наталья", "Пугачева", "natalia.pugacheva@gmail.com", 89651381516)
mikhail3 = add_client(conn, "Михаил", "Владимирович", "mishka.vladimir@mail.ru")

# добавляем номер телефона
natalia_2 = add_phone(conn, 1, 89089723345)

# обновляем инфу по клиенту
natalia = change_client(conn, 1, surname='Алексеева')

# -------------------------------------------------------------
# удаляем номер
delete_ph1 = delete_phone(conn, 2, 89651381516)

# -------------------------------------------------------------
# удаляем клиента
delete_cl1 = delete_client(conn, 3)

# -------------------------------------------------------------
# находим клиента
find_cl1 = find_client(conn, first_name='Дарья')

conn.close()
