from peewee import *
from datetime import datetime

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

def initialize_db():
    DB.connect()
    DB.create_tables([Master, Service, Appointment, MasterService, AppointmentService])

def create_test_data():
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

def print_data():
    for master in Master.select():
        print(f"{master.id}. {master.last_name} {master.first_name} {master.middle_name or ''}, тел: {master.phone}")
    
    for service in Service.select():
        print(f"{service.id}. {service.title} - {service.price} руб.")
        if service.description:
            print(f"Описание: {service.description}")
    
    for appointment in Appointment.select():
        print(f"{appointment.id}. Клиент: {appointment.client_name}, тел: {appointment.client_phone}")
        print(f"Дата: {appointment.date.strftime('%d.%m.%Y %H:%M')}")
        print(f"Мастер: {appointment.master.last_name} {appointment.master.first_name}")
        print(f"Статус: {appointment.status}")
        
        print("Услуги:")
        services_query = (Service.select().join(AppointmentService).where(AppointmentService.appointment == appointment))
        
        for service in services_query:
            print(f"- {service.title} ({service.price} руб.)")
        print()

def main():
    initialize_db()
        
    if Master.select().count() == 0:
        create_test_data()
        print_data()
    
    DB.close()

if __name__ == "__main__":
    main()