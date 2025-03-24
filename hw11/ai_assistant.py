
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

class ImageRequest:
    """
    Класс для отправки запросов, включающих изображение.
    """
    def __init__(self, api_key:str) -> None:
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
        
    def send(self, text:str, image_path:str, model:str = "pixtral-12b-2409", history:list = []) -> dict:
        """
        Отправляет мультимедийный запрос нейронке и возвращает ответ.
        :param text: Текст запроса пользователя
        :param image_path: Путь к изображению
        :param model: Модель для использования (по умолчанию pixtral-12b-2409)
        :param history: История предыдущих сообщений
        :return: Словарь с ответом и обновленной историей        
        """

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
        
