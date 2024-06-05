import psycopg2
import random
import csv
import time
from faker import Faker
from datetime import datetime
from config import host, user, password, db_name
import datetime

def rand_date():
    start_date = datetime.date(1990, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    formatted_date = random_date.strftime("%Y-%m-%d")
    return formatted_date
def generate(st, n):
    fake = Faker('ru-RU')
    data = [["НОМЕР_РЕЙСА", "ДАТА_ВЫЕЗДА", "МАРШРУТ", "АВТО", "ВОДИТЕЛЬ", "ПЕРЕВОЗИМОЕ", "СТАТУС"]]
    for i in range(st, n + 1):
        date = rand_date()
        data.append(
            [i,
             date,
             fake.random_int(min=1, max=1000),
             fake.random_int(min=1, max=150),
             fake.random_int(min=1, max=5000),
             i,
             'Запланирован'
             ])
    return data


start = time.time()
data = generate(1, 1_000_000)
after_create = time.time()
print('массив:', after_create - start)
with open('reisi.csv', 'w', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerows(data)
aft_finish = time.time()
print('вставка: ', aft_finish - after_create)
