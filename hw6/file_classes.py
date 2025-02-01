from abc import *
import json
import csv

class AbstractFile(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
    
    @abstractmethod    
    def read(self):
        """
        Абстрактный метод для чтения данных из файла.
        """
        pass

    @abstractmethod
    def write(self):
        """
        Абстрактный метод для записи данных в файл.
        """
        pass

    @abstractmethod
    def append(self):
        """
        Абстрактный метод для добавления данных в файл.
        """
        pass

class TxtFile(AbstractFile):
    """
    Класс для работы с TXT файлами.
    """
    def read(self):
        """
        Читает содержимое файла и возвращает его в виде строки.
        :return: Содержимое файла в виде строки.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print("File '{self.file_path}' not found")

    def write(self, *data:str):
        """
        Записывает данные в TXT файл.
        :param data: Список строк с данными для записи.
        :return: None
        """
        try:    
            with open(self.file_path, "w", encoding="utf-8") as file:
                for line in data:
                    file.write(line + "\n")
        except Exception as e:
            raise e

    def append(self, *data:str):
        """
        Добавляет данные в TXT файл.
        :param data: Список строк с данными для добавления.
        :return: None
        """
        try:    
            with open(self.file_path, "a", encoding="utf-8") as file:
                for line in data:
                    file.write(line + "\n")
        except Exception as e:
            raise e


class JsonFile(AbstractFile):
    """
    Класс для работы с JSON файлами.
    """
    def read(self):
        """
        Читает содержимое файла и возвращает его в виде списка словарей.
        :return: Содержимое файла в виде списка словарей.
        """
        try:    
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File '{self.file_path}' not found")


    def write(self, *data:dict):
        """
        Записывает данные в JSON файл.
        :param data: Список словарей с данными для записи.
        :return: None
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        
        except Exception as e:
            raise e

    def append(self, *data:dict):
        """
        Добавляет данные в JSON файл.
        :param data: Список словарей с данными для добавления.
        :return: None
        """
        try:
            old_file = self.read()
            old_file.extend(data)
            self.write(*old_file)

        except Exception as e:
            raise e


class CsvFile(AbstractFile):
    """
    Класс для работы с CSV файлами.
    """
    def read(self):
        """
        Читает содержимое файла и возвращает его в виде списка словарей.
        :return: Содержимое файла в виде списка словарей.
        """
        try:    
            with open(self.file_path, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file, delimiter=";")
                return list(reader)
        except FileNotFoundError:
            print("File '{self.file_path}' not found")

    def write(self, *data:dict):
        """
        Записывает данные в CSV файл.
        :param data: Список словарей с данными для записи.
        :return: None
        """
        try:
            with open(self.file_path, "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        except Exception as e:
            raise e

    def append(self, *data:dict):
        """
        Добавляет данные в CSV файл.
        :param data: Список словарей с данными для добавления.
        :return: None"""
        try:
            with open(self.file_path, "a", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writerows(data)
        
        except Exception as e:
            raise e


