import psycopg2
import random
from faker import Faker
from config import host, user, password, db_name


def generate(n):
    fake = Faker('ru-RU')
    letters = ["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]
    # data = [["СЕРИЯ", "НОМЕР", "РЕГИОН"]]
    data = []
    for i in range(1, n + 1):
        data.append(
            (''.join(random.choices(letters, k=3)),
             fake.random_int(min=100, max=999),
             fake.random_int(min=1, max=89)))
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
        data = generate(50)
        cursor.executemany("INSERT INTO ГОС_НОМЕРА(СЕРИЯ, НОМЕР, РЕГИОН) VALUES(%s, %s, %s)", data)
        print('Данные добавлены')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
