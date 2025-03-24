
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
        
class ChatFacade:
    """
    Единый интерфейс для пользователя
    """
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key
        self.text_request = TextRequest(api_key=self.api_key)
        self.image_request = ImageRequest(api_key=self.api_key)
        self.models = {"TextRequest": ["mistral-large-latest"], "ImageRequest": ["pixtral-12b-2409"]}
        self.modes = {"TextRequest": self.text_request, "ImageRequest": self.image_request}
        self.current_mode = "TextRequest"  
        self.current_model = "mistral-large-latest"  
        self.history = []  
    
    def select_mode(self, mode:str = None) -> str:
        """
        Выбирает режим работы.
        :param mode: Режим работы
        :return: Режим работы
        """
        if mode is None:
            mode = input("Выберите режим: TextRequest или ImageRequest: ")
        
        if mode not in self.modes:
            raise Exception("Такого режима не существует.")
        
        self.current_mode = mode
        return mode
    
    def select_model(self, mode:str = None) -> str:
        """
        Выбирает модель для работы.
        :param mode: Режим работы
        :return: Модель
        """
        if mode is None:
            mode = self.current_mode
            
        if mode == "TextRequest":
            model = input(f"Выберите модель из списка: {self.models['TextRequest']}: ")
            if model not in self.models["TextRequest"]:
                model = self.models["TextRequest"][0] 
        elif mode == "ImageRequest":
            model = input(f"Выберите модель из списка: {self.models['ImageRequest']}: ")
            if model not in self.models["ImageRequest"]:
                model = self.models["ImageRequest"][0] 
        
        self.current_model = model
        return model
    
    def load_image(self, image_path:str = None) -> str:
        """
        Загружает изображение.
        :param image_path: Путь к изображению
        :return: Путь к изображению
        """
        if image_path is None:
            image_path = input("Введите путь к изображению: ")
        return image_path
    
    def ask_question(self, question:str, mode:str = None, model:str = None, image_path:str = None) -> str:
        """
        Отправляет вопрос к нейронке в выбранном режиме и возвращает ответ.
        :param question: Вопрос
        :param mode: Режим работы
        :param model: Модель для работы
        :param image_path: Путь к изображению
        :return: Ответ
        """
        
        if mode:
            self.select_mode(mode)
        
        if model:
            self.current_model = model
        elif not self.current_model:
            self.select_model()
        
        try:
            if self.current_mode == "TextRequest":
                result = self.text_request.send(
                    text=question,
                    model=self.current_model,
                    history=self.history
                )
            elif self.current_mode == "ImageRequest":
                if not image_path:
                    image_path = self.load_image()
                
                result = self.image_request.send(
                    text=question,
                    image_path=image_path,
                    model=self.current_model,
                    history=self.history
                )
            
            self.history = result["history"]
            
            return result["response"]
        
        except Exception as e:
            print(f"Ошибка при обработке запроса: {str(e)}")
            return f"Произошла ошибка: {str(e)}"
    
    def get_history(self) -> None:
        """
        Возвращает историю переписки
        """
        
        print(self.history)
    
    def __call__(self):
        """
        Интерактивный режим работы с чатом
        """
        
        print('добро пожаловать в чат-ассистент! Для вывода истории напишите "показать историю"')
        
        try:
            self.select_mode()
           
            self.select_model()
            
            image_path = None
            if self.current_mode == "ImageRequest":
                image_path = self.load_image()
            
            while True:
               
                question = input("\nВаш вопрос (или 'выход' для завершения): ")
                
                if question.lower() == 'выход':
                    break
                
                if question.lower() == 'показать историю':
                    self.get_history()
                    break
               
                response = self.ask_question(
                    question=question,
                    image_path=image_path if self.current_mode == "ImageRequest" else None
                )
    
                print(f"\nОтвет: {response}")
                
        except KeyboardInterrupt:
            print("\nРабота программы прервана пользователем.")
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
        
        print("\nДо свидания!")

if __name__ == "__main__":
    facade = ChatFacade(api)
    facade()
