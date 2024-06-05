import time
import psycopg2
import random
from faker import Faker
from config import host, user, password, db_name
from mimesis import Transport
import string

def generator(n, types_id):
    fake = Faker('ru_RU')
    data = []
    state = 'На складе'
    for i in range(n):
        data.append((random.choice(types_id), fake.random_int(min=1, max=20), state))
    return data

start_time = time.time()
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute("SELECT НОМЕР_ПЕРЕВОЗ FROM ПЕРЕВОЗИМОЕ")
        perevoz = cursor.fetchall()
        perevoz_id = []
        for type in perevoz:
            perevoz_id.append(type[0])


        cursor.execute("SELECT НОМЕР_ГРУЗА FROM ГРУЗ")
        cargo = cursor.fetchall()
        cargo_id = []
        for type in cargo:
            cargo_id.append(type[0])

        after_connection = time.time()
        print(f"Подлкючилось: {after_connection - start_time} секунд")

        fake = Faker('ru_RU')
        data = []
        for i in range(1_000_000):
            k = fake.random_int(min=1, max=5)
            for j in range(k):
                car = cargo_id.pop(0)
                data.append((perevoz_id[i], car))
        after_create = time.time()
        print(f"Доп массив создан: {after_create - after_connection} секунд")
        cursor.executemany("INSERT INTO ГРУЗ_ПЕРЕВОЗИМОЕ(ПЕРЕВОЗИМОЕ, ГРУЗ) VALUES(%s, %s)", data)
        print('Данные добавлены')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')

end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения программы: {execution_time} секунд")