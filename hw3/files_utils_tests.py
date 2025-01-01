import json
import csv
import yaml

from files_utils import write_json, read_json, append_json, write_csv, read_csv, append_csv, write_txt, read_txt, append_txt, write_yaml, read_yaml
# 0000000000000000000000000
file_path = "placeholder.json"
data = [
    "Монин Владимир Александрович",
    "Артемьев Алексей Львович",
    "Багаутдинов Ринат Дмитриевич",
    "Балагуров Артем Алексеевич",
    "Бибиков Кирилл Сергеевич",
    "Крылов Илья Сергеевич",
    "Кряжев Руслан Анатольевич",
    "Кузнецов Иван Станиславович",
    "Лапицкая Наталья Владимировна",
    "Мазуренко Кристина Владимировна",
    "Морозов Илья Валерьевич",
    "Мустяцэ Иван Иванович",
    "Никулина Екатерина Александровна"
]
write_json(data, file_path)
print(read_json(file_path))
append_json(file_path, ["Новый стуfdfdfдент4", "Новый студент5"],  indent=2)

# 0000000000000000000000000

file_path = "placeholder.csv"
students_dict = [
    ["lastname", "firstname", "middlename"],
    ["Монин", "Владимир", "Александрович"],
    ["Артемьев", "Алексей", "Львович"],
    ["Багаутдинов", "Ринат", "Дмитриевич"],
    ["Балагуров", "Артем", "Алексеевич"],
    ["Бибиков", "Кирилл", "Сергеевич"],
    ["Крылов", "Илья", "Сергеевич"],
    ["Кряжев", "Руслан", "Анатольевич"],
    ["Кузнецов", "Иван", "Станиславович"],
    ["Лапицкая", "Наталья", "Владимировна"],
    ["Мазуренко", "Кристина", "Владимировна"],
    ["Морозов", "Илья", "Валерьевич"],
    ["Мустяцэ", "Иван", "Иванович"],
    ["Никулина", "Екатерина", "Александровна"],
]

write_csv(students_dict, file_path)
print(read_csv(file_path))
append_csv(file_path, [["Фамилия", "Имя"]])

# 0000000000000000000000000

file_path = "placeholder.txt"
write_txt(file_path, "Hewwo world", "Hello world", "Hi world")
print(read_txt(file_path))
append_txt(file_path, "Hewwo world", "Hello world", "Hi world")

# 0000000000000000000000000

file_path = "placeholder.yaml"
config = {
    'app_name': 'Мое приложение',
    'version': '1.0',
    'admin': 'Василий Уткин',
    'settings': {
        'theme': 'dark',
        'language': 'ru',
        'notifications': True
    },
    'users': [
        'admin',
        'moderator',
        'guest'
    ]
}

write_yaml(config, file_path)
print(read_yaml(file_path))