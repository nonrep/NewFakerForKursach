import psycopg2
import random
from faker import Faker
from config import host, user, password, db_name
from mimesis import Transport
import string

def generate_truck_name():
    brand = random.choice(['Ford', 'Chevrolet', 'Dodge', 'Toyota'])
    model = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return brand + ' ' + model

def generate(n):
    fake = Faker('ru-RU')
    cars = []
    while len(cars) < 100:
        name = generate_truck_name()
        if name not in cars:
            cars.append(name)
    data = []
    for i in range(0, n):
        data.append(
            [cars[i],
             fake.random_int(17, 29),
             fake.random_int(1, 20)])
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
        data = generate(100)
        cursor.executemany("INSERT INTO МАРКИ(МАРКА, РАСХОД_ТОПЛИВА, ГРУЗОПОДЪЕМНОСТЬ) VALUES(%s, %s, %s)", data)
        print('Данные добавлены')


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
