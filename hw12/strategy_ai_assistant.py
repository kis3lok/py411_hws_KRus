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


class TextRequestStrategy(RequestStrategy):
    """
    Конкретная реализация стратегии для отправки текстовых запросов.
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    def execute(self, text: str, model: str, history: list = None, image_path: str = None) -> dict:
        """
        Реализует отправку текстового запроса к API Mistral.
        :param text: Текст запроса
        :param model: Модель Mistral
        :param history: История запросов
        :return: Результат запроса
        """
        if history is None:
            history = []
            
        messages = history + [{"role": "user", "content": text}]
        
        try:
            chat_response = self.client.chat.complete(
                model=model,
                messages=messages
            )
                
            assistant_message = chat_response.choices[0].message.content
                
            updated_history = messages + [{"role": "assistant", "content": assistant_message}]
                
            return {
                "response": assistant_message,
                "history": updated_history
            }
                
        except Exception as e:
            raise Exception(f"Непредвиденная ошибка: {str(e)}")


