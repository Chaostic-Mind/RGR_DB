from views import console_view
from models import crud_model, generator_model, search_model

def handle_users():
    """CRUD для таблиці Users."""
    while True:
        choice = console_view.print_entity_crud_menu("Users (Користувачі)")
        if choice == "1":
            data = crud_model.get_all_users()
            console_view.display_table(["ID", "ПІБ", "Податковий номер", "Email"], data)
        elif choice == "2":
            full_name = input("Введіть ПІБ користувача: ").strip()
            tax_number = input("Введіть податковий номер (10 цифр): ").strip()
            email = input("Введіть email: ").strip()
            crud_model.add_user(full_name, tax_number, email)
        elif choice == "3":
            try:
                user_id = int(input("Введіть ID користувача для оновлення email: "))
                new_email = input("Введіть новий email: ").strip()
                crud_model.update_user_email(user_id, new_email)
            except ValueError:
                print("[Помилка]: Некоректний ID.")
        elif choice == "4":
            try:
                user_id = int(input("Введіть ID користувача для видалення: "))
                crud_model.delete_user(user_id)
            except ValueError:
                print("[Помилка]: Некоректний ID.")
        elif choice == "0":
            break

def handle_document_types():
    """CRUD для таблиці DocumentType."""
    while True:
        choice = console_view.print_entity_crud_menu("DocumentType (Типи документів)")
        if choice == "1":
            data = crud_model.get_all_document_types()
            console_view.display_table(["Type ID", "Назва типу", "Опис"], data)
        elif choice == "2":
            name = input("Введіть назву типу документа: ").strip()
            description = input("Введіть опис: ").strip()
            crud_model.add_document_type(name, description)
        elif choice == "3":
            print("[!] Редагування типів документів не передбачено. Скористайтеся видаленням або додаванням.")
        elif choice == "4":
            try:
                type_id = int(input("Введіть ID типу документа для видалення: "))
                crud_model.delete_document_type(type_id)
            except ValueError:
                print("[Помилка]: Некоректний ID.")
        elif choice == "0":
            break

def handle_documents():
    """CRUD для таблиці Document."""
    while True:
        choice = console_view.print_entity_crud_menu("Document (Документи)")
        if choice == "1":
            data = crud_model.get_all_documents()
            console_view.display_table(["Doc ID", "Номер", "Назва", "Дата створення", "Author ID", "Type ID"], data)
        elif choice == "2":
            doc_number = input("Введіть номер документа: ").strip()
            title = input("Введіть назву документа: ").strip()
            content = input("Введіть зміст документа: ").strip()
            try:
                author_id = int(input("Введіть ID автора (user_id): "))
                type_id = int(input("Введіть ID типу документа (type_id): "))
                crud_model.add_document(doc_number, title, content, author_id, type_id)
            except ValueError:
                print("[Помилка]: ID автора та типу мають бути числами.")
        elif choice == "3":
            print("[!] Редагування документів можна реалізувати за аналогією. Наразі доступні перегляд, додавання та видалення.")
        elif choice == "4":
            try:
                doc_id = int(input("Введіть ID документа для видалення: "))
                crud_model.delete_document(doc_id)
            except ValueError:
                print("[Помилка]: Некоректний ID.")
        elif choice == "0":
            break

def handle_signatures():
    """CRUD для проміжної таблиці DocumentSignature (Підписи)."""
    while True:
        choice = console_view.print_entity_crud_menu("DocumentSignature (Підписи документів)")
        if choice == "1":
            data = crud_model.get_all_signatures()
            console_view.display_table(["User ID", "Doc ID", "Дата підпису", "Хеш підпису", "Статус"], data)
        elif choice == "2":
            try:
                user_id = int(input("Введіть ID користувача (user_id): "))
                doc_id = int(input("Введіть ID документа (doc_id): "))
                signature_hash = input("Введіть хеш підпису: ").strip()
                status = input("Введіть статус (напр., Підписано): ").strip()
                crud_model.add_signature(user_id, doc_id, signature_hash, status)
            except ValueError:
                print("[Помилка]: ID мають бути цілими числами.")
        elif choice == "3":
            print("[!] Редагування підписів не передбачено. Доступні додавання та видалення.")
        elif choice == "4":
            try:
                user_id = int(input("Введіть ID користувача: "))
                doc_id = int(input("Введіть ID документа: "))
                crud_model.delete_signature(user_id, doc_id)
            except ValueError:
                print("[Помилка]: Некоректні ID.")
        elif choice == "0":
            break

def handle_generation():
    """Генерація тестових даних."""
    print("\n--- ГЕНЕРАЦІЯ ТЕСТОВИХ ДАНИХ ---")
    try:
        count = int(input("Введіть кількість записів для генерації: "))
        if count <= 0:
            print("[!] Кількість має бути більше 0.")
            return
        generator_model.generate_test_data(count)
    except ValueError:
        print("[Помилка]: Введіть ціле число.")

def handle_search():
    """Параметризовані пошукові запити."""
    while True:
        choice = console_view.print_search_menu()
        if choice == "1":
            start_date = input("Введіть початкову дату (YYYY-MM-DD): ").strip()
            end_date = input("Введіть кінцеву дату (YYYY-MM-DD): ").strip()
            results = search_model.search_documents_by_date_range(start_date, end_date)
            console_view.display_table(["Doc ID", "Номер", "Назва", "Дата створення", "Автор", "Тип"], results)
        elif choice == "2":
            pattern = input("Введіть шаблон для пошуку в ПІБ (ILIKE): ").strip()
            results = search_model.search_users_by_name_pattern(pattern)
            console_view.display_table(["ID", "ПІБ", "ІПН", "Email"], results)
        elif choice == "3":
            try:
                min_docs = int(input("Мінімальна кількість документів автора (HAVING): "))
                results = search_model.search_document_stats_by_author(min_docs)
                console_view.display_table(["User ID", "ПІБ", "ІПН", "Кількість документів"], results)
            except ValueError:
                print("[Помилка]: Некоректне значення кількості.")
        elif choice == "0":
            break

def run_app():
    """Головний цикл роботи застосунку."""
    while True:
        choice = console_view.print_main_menu()
        if choice == "1":
            handle_users()
        elif choice == "2":
            handle_document_types()
        elif choice == "3":
            handle_documents()
        elif choice == "4":
            handle_signatures()
        elif choice == "5":
            handle_generation()
        elif choice == "6":
            handle_search()
        elif choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        else:
            print("\n[!] Невірний вибір. Спробуйте ще раз.")