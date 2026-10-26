def print_main_menu():
    """Головне меню застосунку."""
    print("\n" + "=" * 55)
    print("      СУБД POSTGRESQL - КОНСОЛЬНИЙ КЛІЄНТ (MVC)      ")
    print("=" * 55)
    print("1. Керування користувачами (Users)")
    print("2. Керування типами документів (DocumentType)")
    print("3. Керування документами (Document)")
    print("4. Керування підписами (DocumentSignature)")
    print("5. Генерація тестових даних (generate_series)")
    print("6. Параметризовані пошукові запити")
    print("0. Вихід з програми")
    print("=" * 55)
    return input("Оберіть пункт меню (0-6): ").strip()

def print_entity_crud_menu(entity_name: str):
    """Універсальне меню CRUD для будь-якої таблиці."""
    print(f"\n--- КЕРУВАННЯ: {entity_name} ---")
    print("1. Переглянути всі записи")
    print("2. Додати новий запис")
    print("3. Оновити запис / змінити дані")
    print("4. Видалити запис (з перевіркою RESTRICT)")
    print("0. Назад до головного меню")
    return input("Оберіть операцію (0-4): ").strip()

def print_search_menu():
    """Меню пошукових запитів."""
    print("\n--- ПАРАМЕТРИЗОВАНІ ПОШУКОВІ ЗАПИТИ ---")
    print("1. Пошук документів за діапазоном дат (BETWEEN)")
    print("2. Пошук користувачів за шаблоном імені (ILIKE)")
    print("3. Пошук документів та агрегування (GROUP BY / HAVING)")
    print("0. Назад до головного меню")
    return input("Оберіть пошуковий запит (0-3): ").strip()

def display_table(headers, rows, max_col_width=30):
    """
    Форматоване виведення результатів у вигляді таблиці з автовирівнюванням 
    та обрізанням довгих рядків. Не потребує сторонніх бібліотек.
    """
    if not rows:
        print("\n[!] Дані за вказаним запитом відсутні.")
        return

    # Перетворюємо дані у рядки та обмежуємо максимальну ширину довгих полів
    processed_rows = []
    for row in rows:
        new_row = []
        for val in row:
            val_str = str(val if val is not None else "")
            if len(val_str) > max_col_width:
                val_str = val_str[:max_col_width - 3] + "..."
            new_row.append(val_str)
        processed_rows.append(new_row)

    # Розраховуємо максимальну ширину для кожного стовпця
    col_widths = [len(h) for h in headers]
    for row in processed_rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator_line = "-+-".join("-" * w for w in col_widths)

    print("\n" + header_line)
    print(separator_line)

    for row in processed_rows:
        row_line = " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(row))
        print(row_line)
    
    print("-" * len(separator_line))
    print(f"Усього записів: {len(rows)}")