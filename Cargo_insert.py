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

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute("SELECT НОМЕР_ВИДА FROM ВИДЫ_ГРУЗОВ")
        types = cursor.fetchall()
        types_id = []
        for type in types:
            types_id.append(type[0])
        print(types_id)

        data = generator(500, types_id)
        print(data)
        cursor.executemany("INSERT INTO ГРУЗ(ВИД_ГРУЗА, КОЛИЧЕСТВО, СТАТУС) VALUES(%s, %s, %s)", data)
        print('Данные добавлены')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
