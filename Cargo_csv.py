import psycopg2
import random
import csv
import time
from faker import Faker
from datetime import datetime
from config import host, user, password, db_name
import datetime

def generator(n, types_id):
    fake = Faker('ru_RU')
    data = [["НОМЕР_ГРУЗА", "ВИД_ГРУЗА", "КОЛИЧЕСТВО", "СТАТУС"]]
    state = 'На складе'
    for i in range(n):
        data.append(
            [i,
             random.choice(types_id),
             fake.random_int(min=1, max=20),
             state])
    return data

data = []
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

        data = generator(5_000_000, types_id)
        print(data)

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')

with open('cargo.csv', 'w', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerows(data)
print('done!')