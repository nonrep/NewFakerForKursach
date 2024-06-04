import psycopg2
import random
from faker import Faker
from config import host, user, password, db_name


def generate(n):
    fake = Faker('ru-RU')
    auto = list(range(1, 51))
    numbers = list(range(1, 151))
    random.shuffle(numbers)
    data = []
    for i in range(0, n):
        data.append([numbers[i], random.choice(auto)])
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
        data = generate(150)
        cursor.executemany("INSERT INTO АВТОПАРК(ГОС_НОМЕР, МАРКА) VALUES(%s, %s)", data)
        print('[INFO] Данные добавлены!')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
