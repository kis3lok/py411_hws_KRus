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


class ImageRequestStrategy(RequestStrategy):
    """
    Конкретная реализация стратегии для отправки запросов с изображением.
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    def _encode_image(self, image_path: str) -> bytes:
        """
        Кодирует изображение в Base64.
        :param image_path: Путь к изображению
        :return: Кодированное изображение
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = image_file.read()
                return encoded_image
        except FileNotFoundError:
            raise Exception("Файл не был найден.")
        except Exception as e:
            raise Exception(f"Непредвиденная ошибка при чтении изображения: {e}")
        
    def execute(self, text: str, model: str, history: list = None, image_path: str = None) -> dict:
        """
        Реализует отправку мультимодального запроса, объединяющего текст и изображение.
        :param text: Текст запроса пользователя
        :param model: Модель для использования
        :param history: История предыдущих сообщений
        :param image_path: Путь к изображению
        :return: Словарь с ответом и обновленной историей        
        """
        if history is None:
            history = []
            
        if image_path is None:
            raise ValueError("Для ImageRequestStrategy необходимо указать путь к изображению")

        try:
            image_bytes = self._encode_image(image_path)
            
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            image_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
            
            messages = history + [image_message]
            
            chat_response = self.client.chat.complete(
                model=model,
                messages=messages
            )
            
            result = chat_response.choices[0].message.content
            
            updated_history = messages + [{"role": "assistant", "content": result}]
            
            return {
                "response": result,
                "history": updated_history
            }
        except Exception as e:
            raise Exception(f"Ошибка при обработке изображения: {e}")
        

