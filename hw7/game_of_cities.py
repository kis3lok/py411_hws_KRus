import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice
    




@dataclass
class City:
    """
    Датакласс для хранения информации о городе
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False


class JsonFile:
    """
    Класс для работы с JSON файлами
    """
    def __init__(self, path: str = "cities.json"):
        """
        Инициализания класса
        :param path: Путь к файлу
        """
        self.path = path

    def read_data(self):
        """
        Читает данные из файла
        :return: Список словарей с данными
        """
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def write_data(self, *data):
        """
        Записывает данные в файл
        :param data: Список словарей с данными
        :return: None
        """
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    


