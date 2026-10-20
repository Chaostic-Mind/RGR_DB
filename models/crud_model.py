import psycopg
from config import get_db_connection

def get_all_users():
    """Отримання списку всіх користувачів згідно з laba1.sql."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, full_name, tax_number, email FROM Users ORDER BY user_id;")
            return cursor.fetchall()
    except psycopg.Error as error:
        print(f"[Помилка читання]: {error}")
        return []
    finally:
        connection.close()

def add_user(full_name: str, tax_number: str, email: str):
    """Додавання нового користувача у відповідності до laba1.sql."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO Users (full_name, tax_number, email)
            VALUES (%s, %s, %s)
            RETURNING user_id;
            """
            cursor.execute(query, (full_name, tax_number, email))
            user_id = cursor.fetchone()[0]
            connection.commit()
            print(f"[Успіх] Користувача успішно додано з ID: {user_id}")
            return user_id
    except psycopg.errors.UniqueViolation:
        connection.rollback()
        print("[Помилка цілісності]: Користувач із таким податковим номером або email вже існує.")
    except psycopg.Error as error:
        connection.rollback()
        print(f"[Помилка бази даних]: {error}")
    finally:
        connection.close()
    return None

def delete_user(user_id: int):
    """Видалення користувача за ID."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Users WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"[Успіх] Користувача з ID {user_id} видалено.")
            else:
                print(f"[Увага] Користувача з ID {user_id} не знайдено.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка зв'язків БД]: Неможливо видалити користувача, оскільки існують пов'язані документи (RESTRICT діє).")
    except psycopg.Error as error:
        connection.rollback()
        print(f"[Помилка видалення]: {error}")
    finally:
        connection.close()

def update_user_email(user_id: int, new_email: str):
    """Оновлення email користувача за його ID."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "UPDATE Users SET email = %s WHERE user_id = %s;"
            cursor.execute(query, (new_email, user_id))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"[Успіх] Email користувача з ID {user_id} оновлено.")
            else:
                print(f"[Увага] Користувача з ID {user_id} не знайдено.")
    except psycopg.Error as error:
        connection.rollback()
        print(f"[Помилка оновлення]: {error}")
    finally:
        connection.close()