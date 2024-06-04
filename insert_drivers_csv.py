import psycopg2
import random
import time
from faker import Faker
from config import host, user, password, db_name
from functions import create_fk_mas
from itertools import combinations



def categories():
    cat = ['C1', 'C', 'CE', 'B']
    return random.choice(cat)


def generate(n, tab_nomer):
    fake = Faker('ru_RU')
    data = []
    for i in range(1, n + 1):
        categor = []
        for j in range(0, fake.random_int(min=1, max=4)):
            categor.append(categories())
        data.append(
            [tab_nomer + i,
             fake.last_name_male(),
             fake.first_name_male(),
             fake.middle_name_male(),
             categor,
             fake.random_int(min=1, max=40)])
    return data


def create_combinations():
    elements = ['C', 'B', 'C1', 'CE']
    result = []

    for r in range(1, 5):
        comb = combinations(elements, r)
        result.extend(comb)

    unique_combinations = []
    for c in result:
        unique = set(c)
        if len(unique) == len(c):
            unique_combinations.append(list(c))

    return unique_combinations

def mas_of_cat(n):
    comb = create_combinations()
    res = []
    for i in range(1, n + 1):
        res.append(random.choice(comb))
    return res


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

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT ТАБ_НОМЕР FROM ВОДИТЕЛИ ORDER BY ТАБ_НОМЕР DESC LIMIT 1")
    #     tab_nomer = cursor.fetchall()
    #     if len(tab_nomer) == 0:
    #         tab_nomer = 10**7
    #     else:
    #         tab_nomer = tab_nomer[0][0]
    #     print(tab_nomer)
    after_create = time.time()
    print(f"Доп массив создан: {after_create - after_connection} секунд")

    # with connection.cursor() as cursor:
    #     data = generate(2_000_000, tab_nomer)
    after_generate = time.time()
    #     print(f"Данные сгенерированы: {after_generate - after_create} секунд")
    #     cursor.executemany("INSERT INTO ВОДИТЕЛИ(ТАБ_НОМЕР, ФАМИЛИЯ, ИМЯ, ОТЧЕСТВО, КАТЕГОРИЯ, СТАЖ) VALUES(%s, %s, %s, %s, %s, %s)", data)
    after_append=time.time()
    print(f"Данные добавлены: {after_append - after_generate}")


    with connection.cursor() as cursor:
        data = mas_of_cat(2_000_000)
        after_generate = time.time()
        print(f"Данные сгенерированы: {after_generate - after_create} секунд")
        for i, cat in enumerate(data):
            sql = f"UPDATE ВОДИТЕЛИ SET КАТЕГОРИЯ =%s WHERE НОМЕР_ВОДИТЕЛЯ = %s"
            cursor.execute(sql, (cat, i+1))


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')


end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения программы: {execution_time} секунд")