import psycopg2
import random
import json
import csv
from faker import Faker
from config import host, user, password, db_name
import time
from functions import create_fk_mas


# random.choise(mas)
def generate(st, n):
    fake = Faker('ru-RU')
    letters = ["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]
    all_nomers = []
    for let1 in range(0, len(letters)):
        for let2 in range(0, 6):
            for let3 in range(0, 4):
                for nom in range(500, 700):
                    for reg in range(1, 80):
                        all_nomers.append([letters[let1] + letters[let2] + letters[let3], nom, reg])
    data = [["НОМЕР_АВТО", "ГОС_НОМЕР", "МАРКА"]]
    random.shuffle(all_nomers)
    for i in range(st, n + 1):
        seria = all_nomers[i][0]
        nom = all_nomers[i][1]
        reg = all_nomers[i][2]
        mydict = {"СЕРИЯ": seria, "НОМЕР": nom, "РЕГИОН": reg}
        data.append(
            [i,
             json.dumps(mydict, ensure_ascii=False),
             fake.random_int(min=1, max=100)
             ])
    return data

aft_str=time.time()
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        data = generate(1, 2_000_000)
        afr_create=time.time()
        print('массив:', afr_create-aft_str)
        with open('park.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        aft_finish = time.time()
        print('вставка: ', aft_finish-afr_create)
        # cursor.executemany("INSERT INTO АВТОПАРК(ГОС_НОМЕР, МАРКА) VALUES(%s, %s)", data)
        # print('[INFO] Данные добавлены!')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
