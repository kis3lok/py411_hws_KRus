from flask import Flask, request, jsonify
from peewee import *
from datetime import datetime
import json

app = Flask(__name__)

DB = SqliteDatabase('barbershop.db')




class BaseModel(Model):
    class Meta:
        database = DB

class Master(BaseModel):
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    middle_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, unique=True)

class Service(BaseModel):
    title = CharField(max_length=100, unique=True)
    description = TextField(null=True)
    price = DecimalField(max_digits=7, decimal_places=2)

class Appointment(BaseModel):
    client_name = CharField(max_length=100, null=False)
    client_phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    master = ForeignKeyField(Master, backref='appointments')
    status = CharField(max_length=20, default='pending')

class MasterService(BaseModel):
    master = ForeignKeyField(Master)
    service = ForeignKeyField(Service)

class AppointmentService(BaseModel):
    appointment = ForeignKeyField(Appointment)
    service = ForeignKeyField(Service)





def master_to_dict(master):
    """
    Преобразует объект Master в словарь
    """
    return {
        'id': master.id,
        'first_name': master.first_name,
        'last_name': master.last_name,
        'middle_name': master.middle_name,
        'phone': master.phone
    }

def appointment_to_dict(appointment):
    """
    Преобразует объект Appointment в словарь с включением информации о мастере
    """
    return {
        'id': appointment.id,
        'client_name': appointment.client_name,
        'client_phone': appointment.client_phone,
        'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
        'master': {
            'id': appointment.master.id,
            'first_name': appointment.master.first_name,
            'last_name': appointment.master.last_name
        },
        'status': appointment.status
    }

def validate_master_data(data):
    """
    Проверяет корректность данных для создания/обновления мастера
    """
    errors = []
    
    if not data:
        errors.append("Данные не предоставлены")
        return errors
    
    if not data.get('first_name'):
        errors.append("Поле 'first_name' обязательно")
    elif len(data['first_name']) > 50:
        errors.append("Поле 'first_name' не должно превышать 50 символов")
    
    if not data.get('last_name'):
        errors.append("Поле 'last_name' обязательно")
    elif len(data['last_name']) > 50:
        errors.append("Поле 'last_name' не должно превышать 50 символов")
    
    if data.get('middle_name') and len(data['middle_name']) > 50:
        errors.append("Поле 'middle_name' не должно превышать 50 символов")
    
    if not data.get('phone'):
        errors.append("Поле 'phone' обязательно")
    elif len(data['phone']) > 20:
        errors.append("Поле 'phone' не должно превышать 20 символов")
    
    return errors

def validate_appointment_data(data):
    """
    Проверяет корректность данных для создания/обновления записи
    """
    errors = []
    
    if not data:
        errors.append("Данные не предоставлены")
        return errors
    
    if not data.get('client_name'):
        errors.append("Поле 'client_name' обязательно")
    elif len(data['client_name']) > 100:
        errors.append("Поле 'client_name' не должно превышать 100 символов")
    
    if not data.get('client_phone'):
        errors.append("Поле 'client_phone' обязательно")
    elif len(data['client_phone']) > 20:
        errors.append("Поле 'client_phone' не должно превышать 20 символов")
    
    if not data.get('master_id'):
        errors.append("Поле 'master_id' обязательно")
    else:
        try:
            Master.get(Master.id == data['master_id'])
        except Master.DoesNotExist:
            errors.append("Мастер с указанным ID не найден")
    
    if data.get('date'):
        try:
            datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            errors.append("Неверный формат даты. Используйте: YYYY-MM-DD HH:MM:SS")
    
    if data.get('status') and len(data['status']) > 20:
        errors.append("Поле 'status' не должно превышать 20 символов")
    
    return errors

def json_response(data, status_code=200):
    """
    Возвращает JSON ответ с корректной кодировкой
    """
    return json.dumps(data, ensure_ascii=False), status_code, {'Content-Type': 'application/json; charset=utf-8'}




@app.route('/masters', methods=['GET'])
def get_masters():
    """
    Получить список всех мастеров
    """
    try:
        masters = Master.select()
        masters_list = [master_to_dict(master) for master in masters]
        return json_response({'masters': masters_list})
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/masters/<int:master_id>', methods=['GET'])
def get_master(master_id):
    """
    Получить информацию о мастере по ID
    """
    try:
        master = Master.get(Master.id == master_id)
        return json_response({'master': master_to_dict(master)})
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/masters', methods=['POST'])
def create_master():
    """
    Добавить нового мастера
    """
    try:
        data = request.json
        errors = validate_master_data(data)
        
        if errors:
            return json_response({'errors': errors}, 400)
        
        try:
            Master.get(Master.phone == data['phone'])
            return json_response({'error': 'Мастер с таким телефоном уже существует'}, 400)
        except Master.DoesNotExist:
            pass
        
        master = Master.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            phone=data['phone']
        )
        
        return json_response({'master': master_to_dict(master)}, 201)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/masters/<int:master_id>', methods=['PUT'])
def update_master(master_id):
    """
    Обновить информацию о мастере
    """
    try:
        master = Master.get(Master.id == master_id)
        data = request.json
        errors = validate_master_data(data)
        
        if errors:
            return json_response({'errors': errors}, 400)
        
        try:
            existing_master = Master.get(Master.phone == data['phone'])
            if existing_master.id != master_id:
                return json_response({'error': 'Мастер с таким телефоном уже существует'}, 400)
        except Master.DoesNotExist:
            pass
        
        master.first_name = data['first_name']
        master.last_name = data['last_name']
        master.middle_name = data.get('middle_name')
        master.phone = data['phone']
        master.save()
        
        return json_response({'master': master_to_dict(master)})
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/masters/<int:master_id>', methods=['DELETE'])
def delete_master(master_id):
    """
    Удалить мастера
    """
    try:
        master = Master.get(Master.id == master_id)
        
        appointments_count = Appointment.select().where(Appointment.master == master).count()
        if appointments_count > 0:
            return json_response({'error': 'Нельзя удалить мастера, у которого есть записи'}, 400)
        
        master.delete_instance()
        return '', 204
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments', methods=['GET'])
def get_appointments():
    """
    Получить все записи на услуги с опциональной сортировкой
    """
    try:
        query = Appointment.select().join(Master)
        
        sort_by = request.args.get('sort_by', 'date')
        direction = request.args.get('direction', 'asc')
        
        sort_field = None
        if sort_by == 'date':
            sort_field = Appointment.date
        elif sort_by == 'client_name':
            sort_field = Appointment.client_name
        elif sort_by == 'status':
            sort_field = Appointment.status
        elif sort_by == 'master':
            sort_field = Master.last_name
        else:
            sort_field = Appointment.date
        
        if direction.lower() == 'desc':
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())
        
        appointments_list = [appointment_to_dict(appointment) for appointment in query]
        return json_response({'appointments': appointments_list})
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    Получить запись по ID
    """
    try:
        appointment = Appointment.select().join(Master).where(Appointment.id == appointment_id).get()
        return json_response({'appointment': appointment_to_dict(appointment)})
    except Appointment.DoesNotExist:
        return json_response({'error': 'Запись не найдена'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments/master/<int:master_id>', methods=['GET'])
def get_appointments_by_master(master_id):
    """
    Получить все записи для заданного мастера
    """
    try:
        Master.get(Master.id == master_id)
        
        appointments = Appointment.select().join(Master).where(Appointment.master == master_id)
        appointments_list = [appointment_to_dict(appointment) for appointment in appointments]
        return json_response({'appointments': appointments_list})
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments', methods=['POST'])
def create_appointment():
    """
    Создать новую запись
    """
    try:
        data = request.json
        errors = validate_appointment_data(data)
        
        if errors:
            return json_response({'errors': errors}, 400)
        
        master = Master.get(Master.id == data['master_id'])
        
        appointment_data = {
            'client_name': data['client_name'],
            'client_phone': data['client_phone'],
            'master': master,
            'status': data.get('status', 'pending')
        }
        
        if data.get('date'):
            appointment_data['date'] = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        
        appointment = Appointment.create(**appointment_data)
        
        appointment_with_master = Appointment.select().join(Master).where(Appointment.id == appointment.id).get()
        
        return json_response({'appointment': appointment_to_dict(appointment_with_master)}, 201)
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 400)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """
    Обновить запись
    """
    try:
        appointment = Appointment.get(Appointment.id == appointment_id)
        data = request.json
        errors = validate_appointment_data(data)
        
        if errors:
            return json_response({'errors': errors}, 400)
        
        master = Master.get(Master.id == data['master_id'])
        
        appointment.client_name = data['client_name']
        appointment.client_phone = data['client_phone']
        appointment.master = master
        appointment.status = data.get('status', appointment.status)
        
        if data.get('date'):
            appointment.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        
        appointment.save()
        
        appointment_with_master = Appointment.select().join(Master).where(Appointment.id == appointment_id).get()
        
        return json_response({'appointment': appointment_to_dict(appointment_with_master)})
    except Appointment.DoesNotExist:
        return json_response({'error': 'Запись не найдена'}, 404)
    except Master.DoesNotExist:
        return json_response({'error': 'Мастер не найден'}, 400)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """
    Удалить запись
    """
    try:
        appointment = Appointment.get(Appointment.id == appointment_id)
        appointment.delete_instance()
        return '', 204
    except Appointment.DoesNotExist:
        return json_response({'error': 'Запись не найдена'}, 404)
    except Exception as e:
        return json_response({'error': f'Внутренняя ошибка сервера: {str(e)}'}, 500)

@app.errorhandler(404)
def not_found(error):
    return json_response({'error': 'Ресурс не найден'}, 404)

@app.errorhandler(400)
def bad_request(error):
    return json_response({'error': 'Некорректный запрос'}, 400)

@app.errorhandler(500)
def internal_error(error):
    return json_response({'error': 'Внутренняя ошибка сервера'}, 500)





def create_test_data():
    """
    Создает тестовые данные
    """
    if Master.select().count() > 0:
        return
    
    masters = [
        {'first_name': 'Джеймс', 'last_name': 'Хетфилд', 'middle_name': 'Алан', 'phone': '+7(999)-999-99-99'},
        {'first_name': 'Билли', 'last_name': 'Армстронг', 'middle_name': 'Джо', 'phone': '+7(888)-888-88-88'},
        {'first_name': 'Эксл', 'last_name': 'Роуз', 'middle_name': None, 'phone': '+7(777)777-777-777'}
    ]
    Master.insert_many(masters).execute()
    
    services = [
        {'title': 'Мужская стрижка', 'description': 'Мужская стрижка: стиль по запросу или профессиональная. 50/100 грамм виски/коньяка по запросу(бренды см. в салоне)', 'price': 1000},
        {'title': 'Бритьё лица', 'description': 'Профессиональное бритьё усов, бороды и тд.', 'price': 700},
        {'title': 'Окрашивание', 'description': 'Окрашивание волос с предворительным осветлением, если нужно.', 'price': 2500},
        {'title': 'Укладка', 'description': 'Профессиональная укладка волос', 'price': 800}
    ]
    Service.insert_many(services).execute()
    
    master_services = []
    for master in Master.select():
        for service in Service.select():
            master_services.append({'master': master, 'service': service})
    MasterService.insert_many(master_services).execute()
    
    appointments = [
        {
            'client_name': 'Курт Кобейн',
            'client_phone': '+7(900)111-11-11',
            'master': Master.get(Master.first_name == 'Джеймс'),
            'date': datetime(2001, 9, 11, 8, 46),
            'status': 'confirmed'
        },
        {
            'client_name': 'Тилль Линдеманн',
            'client_phone': '+7(900)222-22-23',
            'master': Master.get(Master.first_name == 'Билли'),
            'date': datetime(2007, 7, 7, 7, 7),
            'status': 'pending'
        },
        {
            'client_name': 'Дэвид Боуи',
            'client_phone': '+7(900)333-33-33',
            'master': Master.get(Master.first_name == 'Эксл'),
            'date': datetime(2025, 5, 5, 21, 8),
            'status': 'confirmed'
        }
    ]
    
    for appointment_data in appointments:
        appointment = Appointment.create(**appointment_data)
        
        services = list(Service.select().limit(4))
        if appointment.master.first_name == 'Джеймс':
            AppointmentService.create(appointment=appointment, service=services[0])
            AppointmentService.create(appointment=appointment, service=services[1])
        elif appointment.master.first_name == 'Билли':
            AppointmentService.create(appointment=appointment, service=services[1])
            AppointmentService.create(appointment=appointment, service=services[2])
        else:
            AppointmentService.create(appointment=appointment, service=services[2])
            AppointmentService.create(appointment=appointment, service=services[3])




if __name__ == '__main__':
    DB.connect()
    DB.create_tables([Master, Service, Appointment, MasterService, AppointmentService], safe=True)
    create_test_data()
    DB.close()
    app.run(debug=True)