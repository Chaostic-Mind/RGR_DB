def print_main_menu():
    """Головне меню застосунку."""
    print("\n" + "=" * 50)
    print("      СУБД POSTGRESQL - КОНСОЛЬНИЙ КЛІЄНТ (MVC)      ")
    print("=" * 50)
    print("1. Операції з користувачами (CRUD Users)")
    print("2. Генерація тестових даних (generate_series)")
    print("3. Виконання параметризованих пошукових запитів")
    print("0. Вихід з програми")
    print("=" * 50)
    return input("Оберіть пункт меню (0-3): ").strip()

def print_crud_menu():
    """Меню CRUD-операцій."""
    print("\n--- ОПЕРАЦІЇ З КОРИСТУВАЧАМИ (Users) ---")
    print("1. Переглянути всіх користувачів")
    print("2. Додати нового користувача")
    print("3. Змінити email користувача")
    print("4. Видалити користувача (перевірка RESTRICT / CASCADE)")
    print("0. Назад до головного меню")
    return input("Оберіть операцію (0-4): ").strip()

def print_search_menu():
    """Меню пошукових запитів."""
    print("\n--- ПАРАМЕТРИЗОВАНІ ПОШУКОВІ ЗАПИТИ ---")
    print("1. Пошук документов за діапазоном дат (BETWEEN)")
    print("2. Пошук користувачів за шаблоном імені (ILIKE %pattern%)")
    print("3. Пошук документів та агрегування (GROUP BY / HAVING)")
    print("0. Назад до головного меню")
    return input("Оберіть пошуковий запит (0-3): ").strip()

def display_table(headers, rows):
    """Форматоване виведення результатів вибірки у вигляді таблиці."""
    if not rows:
        print("\n[!] Дані за вказаним запитом відсутні.")
        return

    print("\n" + "-" * 70)
    header_line = " | ".join(f"{h:<15}" for h in headers)
    print(header_line)
    print("-" * 70)
    for row in rows:
        row_line = " | ".join(f"{str(item):<15}" for item in row)
        print(row_line)
    print("-" * 70)
    print(f"Усього записів: {len(rows)}")