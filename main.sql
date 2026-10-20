-- 1. Створення таблиць
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    tax_number VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE DocumentType (
    type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Document (
    doc_id SERIAL PRIMARY KEY,
    doc_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(150) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INT REFERENCES Users(user_id) ON DELETE RESTRICT,
    type_id INT REFERENCES DocumentType(type_id) ON DELETE RESTRICT
);

CREATE TABLE DocumentSignature (
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    doc_id INT REFERENCES Document(doc_id) ON DELETE CASCADE,
    signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    signature_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'Підписано',
    PRIMARY KEY (user_id, doc_id)
);

-- 2. Заповнення даними
INSERT INTO Users (full_name, tax_number, email) VALUES
('Коваленко Олексій Іванович', '1234567890', 'kovalenko@doc.ua'),
('Мельник Тетяна Сергіївна', '0987654321', 'melnyk@doc.ua'),
('Шевченко Дмитро Петрович', '1122334455', 'shevchenko@doc.ua');

INSERT INTO DocumentType (name, description) VALUES
('Наказ', 'Внутрішньоорганізаційний розпорядчий документ'),
('Договір', 'Двостороння або багатостороння угода'),
('Акт прийому-передачі', 'Документ фіксації передачі послуг чи майна');

INSERT INTO Document (doc_number, title, content, author_id, type_id) VALUES
('НК-001', 'Про призначення відповідальних осіб', 'Зміст наказу...', 1, 1),
('ДГ-2026/01', 'Договір на надання IT-послуг', 'Зміст договору...', 1, 2),
('АК-104', 'Акт виконаних робіт за вересень', 'Зміст акта...', 2, 3);

INSERT INTO DocumentSignature (user_id, doc_id, signature_hash, status) VALUES
(1, 1, 'a1b2c3d4e5f6_hash_1', 'Підписано'),
(2, 1, 'f6e5d4c3b2a1_hash_2', 'Підписано'),
(3, 2, '9876543210ab_hash_3', 'Очікує');