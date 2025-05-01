-- Выключение проверки внешних ключей
PRAGMA foreign_keys = OFF;

-- Открытие транзакции
BEGIN TRANSACTION;

-- Создание таблицы мастеров
CREATE TABLE IF NOT EXISTS 'masters' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'first_name' TEXT NOT NULL,
    'last_name' TEXT NOT NULL,
    'middle_name' TEXT,
    'phone' TEXT NOT NULL
);

-- Создание таблицы услуг
CREATE TABLE IF NOT EXISTS 'services' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'title' TEXT UNIQUE NOT NULL,
    'description' TEXT,
    'price' INTEGER NOT NULL
);

-- Создание таблицы записей
CREATE TABLE IF NOT EXISTS 'appointments' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'name' TEXT NOT NULL,
    'phone' TEXT NOT NULL,
    'date' DATETIME DEFAULT CURRENT_TIMESTAMP,
    'master_id' INTEGER NOT NULL,
    'status' TEXT DEFAULT 'ожидает',
    'comment' TEXT,
    FOREIGN KEY ('master_id') REFERENCES 'masters'('id') ON DELETE CASCADE ON UPDATE CASCADE
);

-- Создание таблицы связи мастеров и услуг
CREATE TABLE IF NOT EXISTS 'masters_services' (
    'master_id' INTEGER NOT NULL,
    'service_id' INTEGER NOT NULL,
    PRIMARY KEY ('master_id', 'service_id'),
    FOREIGN KEY ('master_id') REFERENCES 'masters'('id') ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY ('service_id') REFERENCES 'services'('id') ON DELETE CASCADE ON UPDATE CASCADE
);

-- Создание таблицы связи записей и услуг
CREATE TABLE IF NOT EXISTS 'appointments_services' (
    'appointment_id' INTEGER NOT NULL,
    'service_id' INTEGER NOT NULL,
    PRIMARY KEY ('appointment_id', 'service_id'),
    FOREIGN KEY ('appointment_id') REFERENCES 'appointments'('id') ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY ('service_id') REFERENCES 'services'('id') ON DELETE CASCADE ON UPDATE CASCADE
);

-- Добавление мастеров
INSERT INTO 'masters' ('first_name', 'middle_name', 'last_name', 'phone')
VALUES 
    ('Джеймс', 'Алан', 'Хетфилд', '+7(999)-999-99-99'),
    ('Билли', 'Джо', 'Армстронг', '+7(888)-888-88-88');

-- Добавление услуг
INSERT INTO 'services' ('title', 'description', 'price')
VALUES 
    ('Мужская стрижка', 'Мужская стрижка: стиль по запросу или профессиональная. 50/100 грамм виски/коньяка по запросу(бренды см. в салоне)', 1000),
    ('Женская стрижка', 'Мужская стрижка: стиль по запросу или профессиональная', 1500),
    ('Окрашивание', 'Окрашивание волос с предворительным осветлением, если нужно.', 2500),
    ('Укладка', 'Профессиональная укладка волос', 800),
    ('Бритьё лица', 'Профессиональное бритьё усов, бороды и тд.', 700);

-- Добавление связи мастеров и услуг
INSERT INTO 'masters_services' ('master_id', 'service_id')
VALUES 
    (1, 1),
    (1, 5),
    (2, 2),
    (2, 3),
    (2, 4),
    (1, 4);

-- Добавление записей
INSERT INTO 'appointments' ('name', 'phone', 'master_id', 'status')
VALUES 
    ('Клаус Майне', '8(999)-999-09-11', 1, 'подтверждена'),
    ('Энтони Кидис', '8(999)-888-09-11', 2, 'ожидает'),
    ('Эми Ли', '8(999)-777-08-10', 1, 'подтверждена'),
    ('Эксл Роуз', '8(999)-666-07-09', 2, 'отменена');

-- Добавление связи записей и услуг
INSERT INTO 'appointments_services' ('appointment_id', 'service_id')
VALUES 
    (1, 1),
    (2, 2),
    (2, 3),
    (3, 1),
    (3, 5),
    (4, 2),
    (4, 4);


-- Индекс для поиска записей по статусу
-- Это ускорит запросы, фильтрующие записи по статусу (например, "все подтвержденные записи")
-- Часто используется для отображения записей в определенном статусе
CREATE INDEX idx_appointments_status ON appointments(status);

-- Индекс для поиска услуг по цене
-- Ускорит запросы, сортирующие услуги по цене или фильтрующие их по ценовому диапазону
-- Полезно для клиентов, выбирающих услуги по стоимости
CREATE INDEX idx_services_price ON services(price);


-- Составной индекс для поиска мастеров по имени и фамилии
-- Ускорит поиск мастеров, когда клиент ищет конкретного мастера по ФИО
-- Часто используется в интерфейсе поиска и фильтрации
CREATE INDEX idx_masters_name ON masters(last_name, first_name);

-- Составной индекс для поиска записей по дате и мастеру
-- Ускорит запросы, которые ищут все записи к конкретному мастеру на определенную дату
-- Критически важно для планирования расписания и проверки доступности мастеров
CREATE INDEX idx_appointments_date_master ON appointments(date, master_id);

COMMIT;

-- Включение проверки внешних ключей
PRAGMA foreign_keys = ON;

