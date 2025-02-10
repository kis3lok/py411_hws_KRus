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
    
class CitiesSerializer:
    """
    Класс для сериализации городов
    """
    def __init__(self, city_data: list[dict]):
        """
        Инициализания класса
        :param city_data: Список словарей с данными о городах
        """
        self.citylist = []
        self.serialise(city_data)

    def serialise(self, city_data: list[dict]):
        """
        Сериализация городов
        :param city_data: Список словарей с данными о городах
        :return: None
        """
        for city in city_data:
            self.citylist.append(City(
                name=city["name"],
                population=city["population"],
                subject=city["subject"],
                district=city["district"],
                latitude=float(city['coords']['lat']),
                longitude=float(city['coords']['lon']),
            )) #**kwargs не получилось использовать
    
    def get_all_cities(self):
        """
        Возвращает список всех городов
        :return: Список городов
        """
        return self.citylist
    
class CityGame:
    """
    Класс логики игры
    """
    def __init__(self, cities_serializer: CitiesSerializer):
        """
        Инициализания класса
        :param cities_serializer: экземпляр CitiesSerializer
        """
        self.cities = cities_serializer.get_all_cities()
        self.cities_list = [city.name for city in self.cities]
        self.used_cities = []
        self.ai_variant = ''
        self.bad_letters = self.find_bad_letters()
    
    def find_bad_letters(self) -> set:
        """
        Находит плохие буквы
        :return: Список плохих букв
        """
        all_first_letters = {city.name[0].lower() for city in self.cities}
        all_last_letters = {city.name[-1].lower() for city in self.cities}
    
        bad_letters = set()
        for letter in all_last_letters:
            if letter not in all_first_letters:
                bad_letters.add(letter)
            
        return bad_letters
    
    def start_game(self):
        """
        Начинает игру
        :return: Стартовый город от компьютера
        """
        self.ai_variant = choice(list(self.cities_list))
        self.cities_list.remove(self.ai_variant)
        self.used_cities.append(self.ai_variant)
        return self.ai_variant

    def human_turn(self, city:str):
        """
        Ход игрока
        :param city: Строка с названием города
        :return: True, если город есть в списке, False, если нет
        """
        if city not in self.cities_list:
            return False
        if self.ai_variant and city[0].lower() != self.ai_variant[-1].lower():
            return False
        self.cities_list.remove(city)
        self.used_cities.append(city)
        return True
    
    def ai_turn(self, human_variant: str):
        """
        Ход компьютера
        :param human_variant: Строка с названием города от игрока
        :return: Строка с названием города, начинающимся на ту же букву, на которую заканчивается ^
        """
        last_letter = human_variant[-1].lower()

        for city in self.cities_list:
            if city[0].lower() == last_letter and city[-1].lower() not in self.bad_letters:
                self.ai_variant = city
                self.cities_list.remove(city)
                self.used_cities.append(city)
                return city
        return None

class GameManager:
    """
    Класс для управления игрой
    """
    def __init__(self, json_file: JsonFile, cities_serializer: CitiesSerializer, city_game: CityGame):
        """
        Инициализания класса
        :param json_file: экземпляр JsonFile
        :param cities_serializer: экземпляр CitiesSerializer
        :param city_game: экземпляр CityGame
        """
        self.json_file = json_file
        self.cities_serializer = cities_serializer
        self.city_game = city_game
    
    def call(self):
        """
        Запускает игру
        :return: None
        """
        self.run_game()

    def run_game(self):
        """
        Цикл игры
        :return: None
        """
        print('The game begins!')
        print(f'AI says {self.city_game.start_game()}')
        
        while True:
            human_variant = input('Your turn: ')
            if not self.city_game.human_turn(human_variant):
                print('You lose!')
                break
            ai_variant = self.city_game.ai_turn(human_variant)
            if not ai_variant:
                print('You win!')
                break
            print(f'AI says {ai_variant}')


if __name__ == "__main__":
    json_file = JsonFile("cities.json")
    cities_serializer = CitiesSerializer(json_file.read_data())
    city_game = CityGame(cities_serializer)
    game_manager = GameManager(json_file, cities_serializer, city_game)
    game_manager.call()    



