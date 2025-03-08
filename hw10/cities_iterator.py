from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, List, Dict, Optional, Any

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

class CitiesIterator:
    """
    Класс для итерации по городам
    """
    required_keys = {'name', 'population', 'subject', 'district', 'coords'}
    required_coordinations_keys = {'lat', 'lon'}


    def __init__(self, cities: List[Dict[str, Optional[str|Dict[str, str]|int]]]):
        """
        Инициализация класса

        :param cities: Список городов(словарей, содержащих строки в ключах и словари/строки/инт в значениях)
        :return: None
        """
        self.validate_cities(cities)
        self.cities = cities
        self.min_population = 0
        self.sort_param = None
        self.reverse_sort = False
        self._index = 0
        self._city_objects = None
    
    def validate_cities(self, cities: List[Dict[str, Optional[str|Dict[str, str]|int]]]) -> None:
        """
        Метод для валидации словаря городов

        :param cities: Список городов
        :return: None
        """
        for city in cities:
            missing_keys = self.required_keys - set(city.keys())
            if missing_keys:
                raise ValueError(f"В словаре отсутствуют необходимые поля: {missing_keys}")
            
            if 'coords' in city:
                missing_coords = self.required_coordinations_keys - set(city['coords'].keys())
                if missing_coords:
                    raise ValueError(f"Отсутствуют координаты: {missing_coords}")

    def set_population_filter(self, min_population: int) -> None:
        """
        Метод для установки минимального значения населения

        :param min_population: Минимальное значение населения
        :return: None
        """
        self.min_population = min_population

    

    def sort_by(self, parameter: str, reverse: bool = False) -> None:
        """
        Метод для сортировки городов

        :param parameter: Параметр сортировки
        :param reverse: Параметр обратного сортировки
        :return: None
        """
        self.sort_param = parameter
        self.reverse_sort = reverse
    
