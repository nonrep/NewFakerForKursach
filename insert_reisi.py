import psycopg2
import random
from faker import Faker
from datetime import datetime
from config import host, user, password, db_name


def generate(n):
    fake = Faker('ru-RU')
    auto = list(range(1, 150))
    drivers = list(range(1, 100))
    marsh = list(range(1, 101))
    data = []
    for i in range(0, n):
        date = fake.date_between_dates(datetime(2020, 1, 1), datetime(2023,12,31))
        data.append(
            [date,
             random.choice(marsh),
             random.choice(auto),
             random.choice(drivers)])
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
        data = generate(1000)
        cursor.executemany("INSERT INTO РЕЙСЫ(ДАТА_ВЫЕЗДА, МАРШРУТ, АВТО, ВОДИТЕЛЬ) VALUES(%s, %s, %s, %s)", data)
        print('[INFO] Данные добавлены!')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
