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





