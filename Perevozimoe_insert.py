import psycopg2
import random
from faker import Faker
from config import host, user, password, db_name
from mimesis import Transport
import string

def generator(n):
    fake = Faker('ru_RU')
    data = [('Ожидает доставки',) for _ in range(n)]
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

        data = generator(1_000_000)
        print(data)
        cursor.executemany("INSERT INTO ПЕРЕВОЗИМОЕ(СТАТУС) VALUES(%s)", data)
        print('Данные добавлены')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
