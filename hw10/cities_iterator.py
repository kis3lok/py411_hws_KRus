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
    

    def _prepare_cities(self) -> List[City]:
        """
        Метод для подготовки списка городов, его фильтрации

        :return: Список городов
        """
        city_objects = []
        for city in self.cities:
            city_obj = City(
                name=city["name"],
                population=city["population"],
                subject=city["subject"],
                district=city["district"],
                latitude=float(city['coords']['lat']),
                longitude=float(city['coords']['lon'])
            )
            
            if city_obj.population >= self.min_population:
                city_objects.append(city_obj)
            
        if self.sort_param == 'name':
            city_objects.sort(key=self._sort_by_name, reverse=self.reverse_sort)
        elif self.sort_param == 'population':
            city_objects.sort(key=self._sort_by_population, reverse=self.reverse_sort)
        elif self.sort_param == 'subject':
            city_objects.sort(key=self._sort_by_subject, reverse=self.reverse_sort)
        elif self.sort_param == 'district':
            city_objects.sort(key=self._sort_by_district, reverse=self.reverse_sort)
        
        return city_objects

    def _sort_by_name(self, city: City) -> str:
        """
        Метод для установки сортировки городов по названию

        :param city: экземпляр датакласса City
        :return: название города
        """
        return city.name

    def _sort_by_population(self, city: City) -> int:
        """
        Метод для установки сортировки городов по населению

        :param city: экземпляр датакласса City
        :return: население города
        """
        return city.population

    def _sort_by_subject(self, city: City) -> str:
        """
        Метод для установки сортировки городов по региону

        :param city: экземпляр датакласса City
        :return: регион города
        """
        return city.subject

    def _sort_by_district(self, city: City) -> str:
        """
        Метод для установки сортировки городов по району(дистрикту?)

        :param city: экземпляр датакласса City
        :return: район(дистрикт) города
        """
        return city.district


    def __iter__(self):
        """
        Метод для создания итератора

        :return: экземпляр класса CitiesIterator
        """
        self._city_objects = self._prepare_cities()
        self._index = 0
        return self
    
    def __next__(self) -> City:
        """
        Метод для получения следующего города

        :return: экземпляр датакласса City
        """
        if self._city_objects is None:
            self._city_objects = self._prepare_cities()
            
        if self._index >= len(self._city_objects):
            raise StopIteration
            
        city = self._city_objects[self._index]
        self._index += 1
        return city
    

test_cities = [
    {
        "coords": {
            "lat": "52.65",
            "lon": "90.08333"
        },
        "district": "Сибирский",
        "name": "Абаза",
        "population": 14816,
        "subject": "Хакасия"
    },
    {
        "coords": {
            "lat": "53.71667",
            "lon": "91.41667"
        },
        "district": "Сибирский",
        "name": "Абакан",
        "population": 187239,
        "subject": "Хакасия"
    },
    {
        "coords": {
            "lat": "53.68333",
            "lon": "53.65"
        },
        "district": "Приволжский",
        "name": "Абдулино",
        "population": 18420,
        "subject": "Оренбургская область"
    },
    {
        "coords": {
            "lat": "44.86667",
            "lon": "38.16667"
        },
        "district": "Южный",
        "name": "Абинск",
        "population": 39186,
        "subject": "Краснодарский край"
    },
    {
        "coords": {
            "lat": "55.9",
            "lon": "53.93333"
        },
        "district": "Приволжский",
        "name": "Агидель",
        "population": 13935,
        "subject": "Башкортостан"
    },
]

if __name__ == "__main__":
    
    # Тест итерации
    print('1st test')
    iterator = CitiesIterator(test_cities)
    for city in iterator:
        print(f"{city.name}: {city.population}")
    print()

    # Тест фильтра по минимальному населению (15000)
    print('2nd test')
    iterator = CitiesIterator(test_cities)
    iterator.set_population_filter(15000)
    for city in iterator:
        print(f"{city.name}: {city.population}")
    print()

    # Тест сортировки по названию
    print('3rd test')
    iterator = CitiesIterator(test_cities)
    iterator.sort_by('name')
    for city in iterator:
        print(f"{city.name}")
    print()

    # Тест сортировки по населению в обратном порядке
    print('4th test')
    iterator = CitiesIterator(test_cities)
    iterator.sort_by('population', reverse=True)
    for city in iterator:
        print(f"{city.name}: {city.population}")
    print()

    # Валидация
    print('5th test')
    try:
        invalid_city = [{"name": "Invalid City"}]
        iterator = CitiesIterator(invalid_city)
    except ValueError as e:
        print(e)
