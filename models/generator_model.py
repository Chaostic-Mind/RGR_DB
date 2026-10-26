import time
import psycopg
from config import get_db_connection

def generate_test_data(record_count: int = 100):
    """
    Генерує тестові дані (документи) в базі даних засобами SQL-функцій PostgreSQL
    (generate_series, random) безпосередньо в базі даних.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print(f"[*] Початок генерації {record_count} записів для таблиці Document...")
            start_time = time.time()

            query = """
            INSERT INTO Document (doc_number, title, content, created_at, author_id, type_id)
            SELECT 
                'DOC-' || i || '-' || trunc(random() * 1000000)::int AS doc_number,
                'Згенерований документ №' || i AS title,
                'Текст тестового документу номер ' || i AS content,
                NOW() - (random() * INTERVAL '365 days') AS created_at,
                (SELECT user_id FROM Users ORDER BY random() LIMIT 1) AS author_id,
                (SELECT type_id FROM DocumentType ORDER BY random() LIMIT 1) AS type_id
            FROM generate_series(1, %s) AS i;
            """
            
            cursor.execute(query, (record_count,))
            connection.commit()
            
            end_time = time.time()
            elapsed_ms = (end_time - start_time) * 1000
            print(f"[Успіх] Успішно згенеровано {record_count} записів за {elapsed_ms:.2f} мс.")

    except Exception as error:
        connection.rollback()
        print(f"[Помилка генерації даних]: {error}")
    finally:
        connection.close()