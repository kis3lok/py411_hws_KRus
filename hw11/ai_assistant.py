
from mistralai import Mistral
from your_api_key import APIKEY
import base64


api = APIKEY

class TextRequest:
    """
    Класс для отправки текстовых запросов нейронке.
    """
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    def send(self, text:str, model:str = "mistral-large-latest", history:list = []) -> dict:
        """
        Отправляет текстовый запрос нейронке и возвращает ответ.
        :param text: Текст запроса
        :param model: Модель Mistral
        :param history: История запросов
        :return: Результат запроса
        """
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


