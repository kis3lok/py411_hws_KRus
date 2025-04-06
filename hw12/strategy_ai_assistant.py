from mistralai import Mistral
from your_api_key import APIKEY
import base64
from abc import ABC, abstractmethod

api = APIKEY

class RequestStrategy(ABC):
    """
    Абстрактный класс для стратегий запросов.
    """
    @abstractmethod
    def execute(self, text: str, model: str, history: list = None, image_path: str = None) -> dict:
        """
        Абстрактный метод для выполнения запроса.
        :param text: Текст запроса
        :param model: Модель Mistral
        :param history: История запросов
        :param image_path: Путь к изображению (для ImageRequestStrategy)
        :return: Результат запроса
        """
        pass


