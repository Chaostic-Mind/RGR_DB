import psycopg
from config import get_db_connection

# ==========================================
# 1. КЕРУВАННЯ КОРИСТУВАЧАМИ (Users)
# ==========================================

def get_all_users():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, full_name, tax_number, email FROM Users ORDER BY user_id;")
            return cursor.fetchall()
    except psycopg.Error as e:
        print(f"[Помилка читання користувачів]: {e}")
        return []
    finally:
        connection.close()

def add_user(full_name: str, tax_number: str, email: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (full_name, tax_number, email) VALUES (%s, %s, %s);",
                (full_name, tax_number, email)
            )
            connection.commit()
            print("[Успіх] Користувача успішно додано.")
    except psycopg.errors.UniqueViolation:
        connection.rollback()
        print("[Помилка цілісності]: Користувач із таким податковим номером або email вже існує.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка БД]: {e}")
    finally:
        connection.close()

def update_user_email(user_id: int, new_email: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Users SET email = %s WHERE user_id = %s;",
                (new_email, user_id)
            )
            if cursor.rowcount == 0:
                print(f"[!] Користувача з ID {user_id} не знайдено.")
            else:
                connection.commit()
                print("[Успіх] Email користувача оновлено.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка оновлення]: {e}")
    finally:
        connection.close()

def delete_user(user_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Users WHERE user_id = %s;", (user_id,))
            if cursor.rowcount == 0:
                print(f"[!] Користувача з ID {user_id} не знайдено.")
            else:
                connection.commit()
                print("[Успіх] Користувача видалено.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка обмеження (RESTRICT)]: Неможливо видалити користувача, оскільки на нього існують посилання в інших таблицях (документи або підписи).")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка видалення]: {e}")
    finally:
        connection.close()


# ==========================================
# 2. КЕРУВАННЯ ТИПАМИ ДОКУМЕНТІВ (DocumentType)
# ==========================================

def get_all_document_types():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT type_id, name, description FROM DocumentType ORDER BY type_id;")
            return cursor.fetchall()
    except psycopg.Error as e:
        print(f"[Помилка]: {e}")
        return []
    finally:
        connection.close()

def add_document_type(name: str, description: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO DocumentType (name, description) VALUES (%s, %s);",
                (name, description)
            )
            connection.commit()
            print("[Успіх] Тип документа додано.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка]: {e}")
    finally:
        connection.close()

def delete_document_type(type_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM DocumentType WHERE type_id = %s;", (type_id,))
            if cursor.rowcount == 0:
                print(f"[!] Тип документа з ID {type_id} не знайдено.")
            else:
                connection.commit()
                print("[Успіх] Тип документа видалено.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка обмеження (RESTRICT)]: Неможливо видалити тип документа, оскільки до нього прив'язані існуючі документи.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка]: {e}")
    finally:
        connection.close()


# ==========================================
# 3. КЕРУВАННЯ ДОКУМЕНТАМИ (Document)
# ==========================================

def get_all_documents():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT doc_id, doc_number, title, created_at, author_id, type_id 
                FROM Document ORDER BY doc_id;
            """)
            return cursor.fetchall()
    except psycopg.Error as e:
        print(f"[Помилка]: {e}")
        return []
    finally:
        connection.close()

def add_document(doc_number: str, title: str, content: str, author_id: int, type_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Document (doc_number, title, content, author_id, type_id) 
                VALUES (%s, %s, %s, %s, %s);
                """,
                (doc_number, title, content, author_id, type_id)
            )
            connection.commit()
            print("[Успіх] Документ успішно створено.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка зв'язку]: Вказаний author_id або type_id не існує в базі даних.")
    except psycopg.errors.UniqueViolation:
        connection.rollback()
        print("[Помилка цілісності]: Документ із таким номером вже існує.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка БД]: {e}")
    finally:
        connection.close()

def delete_document(doc_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Document WHERE doc_id = %s;", (doc_id,))
            if cursor.rowcount == 0:
                print(f"[!] Документ з ID {doc_id} не знайдено.")
            else:
                connection.commit()
                print("[Успіх] Документ видалено.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка обмеження (RESTRICT)]: Неможливо видалити документ, оскільки на нього існують посилання (підписи у проміжній таблиці).")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка]: {e}")
    finally:
        connection.close()


# ==========================================
# 4. КЕРУВАННЯ ПІДПИСАМИ (DocumentSignature)
# ==========================================

def get_all_signatures():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, doc_id, signed_at, signature_hash, status 
                FROM DocumentSignature;
            """)
            return cursor.fetchall()
    except psycopg.Error as e:
        print(f"[Помилка]: {e}")
        return []
    finally:
        connection.close()

def add_signature(user_id: int, doc_id: int, signature_hash: str, status: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO DocumentSignature (user_id, doc_id, signature_hash, status) 
                VALUES (%s, %s, %s, %s);
                """,
                (user_id, doc_id, signature_hash, status)
            )
            connection.commit()
            print("[Успіх] Підпис успішно додано.")
    except psycopg.errors.ForeignKeyViolation:
        connection.rollback()
        print("[Помилка зв'язку]: Вказаний користувач (user_id) або документ (doc_id) не існує.")
    except psycopg.errors.UniqueViolation:
        connection.rollback()
        print("[Помилка цілісності]: Цей користувач вже підписав цей документ.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка БД]: {e}")
    finally:
        connection.close()

def delete_signature(user_id: int, doc_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM DocumentSignature WHERE user_id = %s AND doc_id = %s;",
                (user_id, doc_id)
            )
            if cursor.rowcount == 0:
                print(f"[!] Підпис для вказаного користувача та документа не знайдено.")
            else:
                connection.commit()
                print("[Успіх] Підпис видалено.")
    except psycopg.Error as e:
        connection.rollback()
        print(f"[Помилка]: {e}")
    finally:
        connection.close()