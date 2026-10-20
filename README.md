# Розрахунково-графічна робота (РГР)
**Дисципліна:** Бази даних та засоби управління  
**Тема:** Створення застосунку бази даних, орієнтованого на взаємодію з СУБД PostgreSQL  

## 1. Мета роботи
Набуття практичних навичок розроблення прикладного застосунку на Python, що взаємодіє з PostgreSQL за допомогою драйвера Psycopg 3, підтримує параметризовані SQL-запити, масову генерацію даних, обробку помилок та має структуру MVC.

## 2. Предметна область та структура БД
Предметна область — електронний документообіг.
- `Users`: інформація про користувачів (user_id, first_name, last_name, email, age, is_active).
- `DocumentType`: види документів (type_id, type_name, description).
- `Document`: збережені документи (document_id, title, creation_date, user_id, type_id).
- `DocumentSignature`: підписи документів (signature_id, document_id, signed_by, signature_date, is_verified).

## 3. Структура проєкту (MVC)
- `config/`: зчитування `.env` та підключення до БД (Psycopg 3).
- `models/`: бізнес-логіка, CRUD-операції, SQL-генератор (100k) та складні пошукові запити.
- `views/`: консольне меню та форматований вивід результатів.
- `controllers/`: зв'язування View та Model, передача параметрів.

## 4. Налаштування та запуск
1. Клонувати репозиторій.
2. Створити та активувати venv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/macOS або venv\Scripts\activate для Windows