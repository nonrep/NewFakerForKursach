import psycopg2
import random
import time
from faker import Faker
from config import host, user, password, db_name


def generate(n):
    fake = Faker('ru-RU')
    data = []
    for i in range(0, n):
        days = fake.random_int(min=5, max=14)
        kms = days * fake.random_int(min=450, max=1000)
        start = fake.city_name()
        end = fake.city_name()
        mas=[]
        mas.append( f"Город отправления: {start}")
        for j in range(0, fake.random_int(min=1, max=10)):
            mas.append(f"остановка {j+1}: {fake.city_name()}")
        mas.append(f"Конечный пункт: {end}")
        opis = ', '.join(mas)
        data.append(
            [start,
             end,
             days,
             kms,
             kms*4,
             opis]
             )
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
    after_connection = time.time()
    print(f"Подлкючилось: {after_connection - start_time} секунд")

    with connection.cursor() as cursor:
        data = generate(1_000)
        after_create = time.time()
        print(f"Доп массив создан: {after_create - after_connection} секунд")
        cursor.executemany("""INSERT INTO МАРШРУТЫ(ПУНКТ_НАЗНАЧ, ПУНКТ_ОТПРАВ, ВРЕМЯ, РАССТОЯНИЕ, ОПЛАТА, ОПИСАНИЕ)
        VALUES(%s, %s, %s, %s, %s, %s)""", data)
    after_append = time.time()
    print(f"Данные добавлены: {after_append - after_create}")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')

end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения программы: {execution_time} секунд")
