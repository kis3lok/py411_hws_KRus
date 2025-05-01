
import sqlite3
from typing import List, Tuple, Optional

DB_PATH = 'hw16/bbshop.db'
SQL_SCHEMA_PATH = 'hw16/barbershop.sql'

def read_sql_file(filepath: str) -> str:
    """
    Читает текст SQL-скрипта из файла и возвращает его содержимое.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def execute_script(conn, script: str) -> None:
    """
    Принимает соединение и текст скрипта, создаёт курсор, выполняет скрипт через метод executescript, сохраняет изменения.
    """
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()

def find_appointment_by_phone(conn, phone: str) -> List[Tuple]:
    """
    Принимает соединение и номер телефона, выполняет параметризованный SELECT-запрос 
    на точное совпадение номера телефона, возвращает список найденных записей.
    """
    cursor = conn.cursor()
    query = """
    SELECT 
        a.id, 
        a.name AS client_name, 
        a.phone, 
        a.date, 
        m.first_name || ' ' || m.last_name AS master_name,
        GROUP_CONCAT(s.title, ', ') AS services,
        a.status
    FROM 
        appointments a
    JOIN 
        masters m ON a.master_id = m.id
    JOIN 
        appointments_services aps ON a.id = aps.appointment_id
    JOIN 
        services s ON aps.service_id = s.id
    WHERE 
        a.phone = ?
    GROUP BY 
        a.id
    """
    cursor.execute(query, (phone,))
    return cursor.fetchall()

def find_appointment_by_comment(conn, comment_part: str) -> List[Tuple]:
    """
    Принимает соединение и часть комментария, ищет записи, где комментарий содержит 
    переданную строку, используя оператор LIKE, возвращает список найденных записей.
    """
    cursor = conn.cursor()
    query = """
    SELECT 
        a.id, 
        a.name AS client_name, 
        a.phone, 
        a.date, 
        m.first_name || ' ' || m.last_name AS master_name,
        GROUP_CONCAT(s.title, ', ') AS services,
        a.status,
        a.comment
    FROM 
        appointments a
    JOIN 
        masters m ON a.master_id = m.id
    JOIN 
        appointments_services aps ON a.id = aps.appointment_id
    JOIN 
        services s ON aps.service_id = s.id
    WHERE 
        a.comment LIKE ?
    GROUP BY 
        a.id
    """
    cursor.execute(query, (f'%{comment_part}%',))
    return cursor.fetchall()

def create_appointment(conn, client_name: str, client_phone: str, master_name: str, 
    services_list: List[str], comment: Optional[str] = None) -> int:
    """
    Создаёт новую запись в таблице клиентов, принимает имя клиента, телефон, 
    имя мастера и список услуг. Ищет мастера и услуги по именам, вставляет запись в базу, 
    связывает её с услугами. Возвращает ID созданной записи.
    """
    cursor = conn.cursor()
    
    master_name_parts = master_name.split()
    if len(master_name_parts) == 2:
        first_name, last_name = master_name_parts
        cursor.execute(
            "SELECT id FROM masters WHERE first_name = ? AND last_name = ?", 
            (first_name, last_name)
        )
    else:
        cursor.execute(
            "SELECT id FROM masters WHERE first_name || ' ' || last_name LIKE ?", 
            (f'%{master_name}%',)
        )
    
    master_result = cursor.fetchone()
    if not master_result:
        raise ValueError(f"Мастер с именем '{master_name}' не найден")
    
    master_id = master_result[0]
    
    if comment:
        cursor.execute(
            "INSERT INTO appointments (name, phone, master_id, comment) VALUES (?, ?, ?, ?)",
            (client_name, client_phone, master_id, comment)
        )
    else:
        cursor.execute(
            "INSERT INTO appointments (name, phone, master_id) VALUES (?, ?, ?)",
            (client_name, client_phone, master_id)
        )
    
    appointment_id = cursor.lastrowid
    
    for service_name in services_list:
        cursor.execute("SELECT id FROM services WHERE title = ?", (service_name,))
        service_result = cursor.fetchone()
        
        if not service_result:
            raise ValueError(f"Услуга с названием '{service_name}' не найдена")
        
        service_id = service_result[0]
        
        cursor.execute(
            "SELECT 1 FROM masters_services WHERE master_id = ? AND service_id = ?",
            (master_id, service_id)
        )
        
        if not cursor.fetchone():
            cursor.execute("SELECT title FROM services WHERE id = ?", (service_id,))
            service_title = cursor.fetchone()[0]
            raise ValueError(f"Мастер '{master_name}' не предоставляет услугу '{service_title}'")
        
        cursor.execute(
            "INSERT INTO appointments_services (appointment_id, service_id) VALUES (?, ?)",
            (appointment_id, service_id)
        )
    
    conn.commit()
    return appointment_id

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    
    # Тест создания записи
    try:
        appointment_id = create_appointment(
            conn,
            "Иван Иванов",
            "+79001234567",
            "Джеймс Хетфилд", 
            ["Мужская стрижка", "Бритьё лица"],
            "тестовый комментарий"
        )
        print(f"Создана запись с ID: {appointment_id}")
    except ValueError as e:
        print(f"Ошибка при создании записи: {e}")
    
    # Тест поиска по телефону
    appointments = find_appointment_by_phone(conn, "+79001234567")
    if appointments:
        print(f"Найдено {len(appointments)} записей:")
        for app in appointments:
            print(f"ID: {app[0]}, Клиент: {app[1]}, Телефон: {app[2]}, Дата: {app[3]}, Мастер: {app[4]}, Услуги: {app[5]}, Статус: {app[6]}")
    else:
        print("Записи не найдены")
    
    # Тест поиска по комментарию
    appointments = find_appointment_by_comment(conn, "тестовый")
    if appointments:
        print(f"Найдено {len(appointments)} записей:")
        for app in appointments:
            print(f"ID: {app[0]}, Клиент: {app[1]}, Телефон: {app[2]}, Дата: {app[3]}, Мастер: {app[4]}, Услуги: {app[5]}, Статус: {app[6]}, Комментарий: {app[7]}")
    else:
        print("Записи не найдены")