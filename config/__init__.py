import os
from dotenv import load_dotenv
import psycopg

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """
    Створює та повертає нове з'єднання з базою даних PostgreSQL 
    засобами драйвера Psycopg 3.
    """
    try:
        connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as error:
        print(f"[Помилка конфігурації БД]: Не вдалося підключитися до бази даних. Деталі: {error}")
        raise