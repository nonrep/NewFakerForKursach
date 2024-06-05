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
        cursor.execute("SELECT НОМЕР_РЕЙСА FROM РЕЙСЫ WHERE СТАТУС = 'Запланирован' ORDER BY ДАТА_ВЫЕЗДА LIMIT 950000")
        reisi = cursor.fetchall()
        reisi_ids = []
        for reis in reisi:
            reisi_ids.append(reis[0])
        print(reisi_ids)
        #800_000
        # for i in range(800_000):
        #     cursor.execute("UPDATE РЕЙСЫ SET СТАТУС = 'Завершен' WHERE НОМЕР_РЕЙСА = %s", (reisi_ids.pop(0),))
        #50_000
        for i in range(1_000):
            cursor.execute("UPDATE РЕЙСЫ SET СТАТУС = 'Отменен' WHERE НОМЕР_РЕЙСА = %s", (reisi_ids.pop(0),))

        # 100_000
        for i in range(500):
            cursor.execute("UPDATE РЕЙСЫ SET СТАТУС = 'В пути' WHERE НОМЕР_РЕЙСА = %s", (reisi_ids.pop(0),))

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