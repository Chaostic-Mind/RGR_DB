from views import console_view
from models import crud_model, generator_model, search_model

def handle_crud():
    """Логіка обробки меню CRUD для користувачів."""
    while True:
        choice = console_view.print_crud_menu()
        if choice == "1":
            users = crud_model.get_all_users()
            headers = ["ID", "ПІБ", "ІПН (Tax Number)", "Email"]
            console_view.display_table(headers, users)
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

def handle_generation():
    """Логіка обробки генерації даних."""
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
    """Логіка обробки пошукових запитів згідно з laba1.sql."""
    while True:
        choice = console_view.print_search_menu()
        if choice == "1":
            start_date = input("Введіть початкову дату (YYYY-MM-DD): ").strip()
            end_date = input("Введіть кінцеву дату (YYYY-MM-DD): ").strip()
            results = search_model.search_documents_by_date_range(start_date, end_date)
            headers = ["Doc ID", "Номер", "Назва", "Дата створення", "Автор ID", "Тип ID"]
            console_view.display_table(headers, results)
        elif choice == "2":
            pattern = input("Введіть шаблон для пошуку в ПІБ (ILIKE): ").strip()
            results = search_model.search_users_by_name_pattern(pattern)
            headers = ["ID", "ПІБ", "ІПН", "Email"]
            console_view.display_table(headers, results)
        elif choice == "3":
            try:
                min_docs = int(input("Мінімальна кількість документів автора (HAVING): "))
                results = search_model.search_document_stats_by_author(min_docs)
                headers = ["User ID", "ПІБ", "ІПН", "Кількість документів"]
                console_view.display_table(headers, results)
            except ValueError:
                print("[Помилка]: Некоректне значення кількості.")
        elif choice == "0":
            break

def run_app():
    """Головний цикл роботи застосунку."""
    while True:
        choice = console_view.print_main_menu()
        if choice == "1":
            handle_crud()
        elif choice == "2":
            handle_generation()
        elif choice == "3":
            handle_search()
        elif choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        else:
            print("\n[!] Невірний вибір. Спробуйте ще раз.")