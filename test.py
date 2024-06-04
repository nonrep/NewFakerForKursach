import psycopg2
import random
import time
from faker import Faker
from datetime import datetime
from config import host, user, password, db_name


def create_fk_mas(mas):
    result = []
    for elem in mas:
        result.append(elem[0])
    return result


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
        cursor.execute("SELECT НОМЕР_ГОС_НОМЕРА FROM ГОС_НОМЕРА")
        data = cursor.fetchall()
    data = create_fk_mas(data)
    print(data)
except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')


# for i in range(0, len(data)):
#     string = data[i][0] + data[i][1] + data[i][2]
#     for j in range(i + 1, len(data) - 1):
#         if string == data[j][0] + data[j][1] + data[j][2]:
#             print(i, j, string)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time} секунд")