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



