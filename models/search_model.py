import time
import psycopg
from config import get_db_connection

def search_documents_by_date_range(start_date: str, end_date: str):
    """
    1. Запит із діапазоном для дат (між start_date та end_date).
    Об'єднує таблиці Document, Users та DocumentType.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT d.doc_id, d.doc_number, d.title, d.created_at, 
                   u.full_name AS author_name, 
                   dt.name AS type_name
            FROM Document d
            JOIN Users u ON d.author_id = u.user_id
            JOIN DocumentType dt ON d.type_id = dt.type_id
            WHERE d.created_at BETWEEN %s AND %s
            ORDER BY d.created_at DESC
            LIMIT 50;
            """
            
            start_time = time.perf_counter()
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            end_time = time.perf_counter()
            
            elapsed_ms = (end_time - start_time) * 1000
            print(f"[Пошук 1] Знайдено {len(results)} записів за {elapsed_ms:.2f} мс.")
            return results
            
    except psycopg.Error as error:
        print(f"[Помилка пошуку за датами]: {error}")
        return []
    finally:
        connection.close()


def search_users_by_name_pattern(pattern: str):
    """
    2. Запит із пошуком за шаблоном (LIKE/ILIKE) для рядків.
    Шукає користувачів за ПІБ у таблиці Users.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql_pattern = f"%{pattern}%"
            query = """
            SELECT user_id, full_name, tax_number, email
            FROM Users
            WHERE full_name ILIKE %s
            ORDER BY user_id;
            """
            
            start_time = time.perf_counter()
            cursor.execute(query, (sql_pattern,))
            results = cursor.fetchall()
            end_time = time.perf_counter()
            
            elapsed_ms = (end_time - start_time) * 1000
            print(f"[Пошук 2] Знайдено {len(results)} користувачів за {elapsed_ms:.2f} мс.")
            return results
            
    except psycopg.Error as error:
        print(f"[Помилка пошуку за шаблоном]: {error}")
        return []
    finally:
        connection.close()


def search_document_stats_by_author(min_docs_count: int):
    """
    3. Запит із групуванням (GROUP BY / HAVING) та агрегуванням.
    Рахує кількість документів, створених кожним автором.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT u.user_id, u.full_name, u.tax_number, COUNT(d.doc_id) AS doc_count
            FROM Users u
            LEFT JOIN Document d ON u.user_id = d.author_id
            GROUP BY u.user_id, u.full_name, u.tax_number
            HAVING COUNT(d.doc_id) >= %s
            ORDER BY doc_count DESC;
            """
            
            start_time = time.perf_counter()
            cursor.execute(query, (min_docs_count,))
            results = cursor.fetchall()
            end_time = time.perf_counter()
            
            elapsed_ms = (end_time - start_time) * 1000
            print(f"[Пошук 3] Знайдено {len(results)} рядків за {elapsed_ms:.2f} мс.")
            return results
            
    except psycopg.Error as error:
        print(f"[Помилка групування та пошуку]: {error}")
        return []
    finally:
        connection.close()