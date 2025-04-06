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
        

class ChatFacade:
    """
    Фасад предоставляет единый интерфейс для пользователя и управляет взаимодействием с RequestStrategy.
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.text_strategy = TextRequestStrategy(api_key=self.api_key)
        self.image_strategy = ImageRequestStrategy(api_key=self.api_key)
        
        self.models = {
            "text": ["mistral-large-latest"],
            "image": ["pixtral-12b-2409"]
        }
        
        self.strategies = {
            "text": self.text_strategy,
            "image": self.image_strategy
        }
        
        self.current_strategy_type = "text"
        self.current_strategy = self.text_strategy
        self.current_model = "mistral-large-latest"
        
        self.history = []
    
    def change_strategy(self, strategy_type: str) -> None:
        """
        Метод для смены текущей стратегии запроса.
        :param strategy_type: Тип стратегии ('text' или 'image')
        """
        if strategy_type not in self.strategies:
            raise ValueError(f"Неизвестный тип стратегии: {strategy_type}. Доступные типы: {list(self.strategies.keys())}")
        
        self.current_strategy_type = strategy_type
        self.current_strategy = self.strategies[strategy_type]
        
        self.current_model = self.models[strategy_type][0]
    
    def select_model(self) -> str:
        """
        Позволяет выбрать модель из списка, соответствующую текущей стратегии.
        :return: Выбранная модель
        """
        available_models = self.models[self.current_strategy_type]
        print(f"Доступные модели для стратегии {self.current_strategy_type}: {available_models}")
        
        model = input(f"Выберите модель (или нажмите Enter для использования {available_models[0]}): ")
        
        if not model or model not in available_models:
            model = available_models[0]
            print(f"Выбрана модель по умолчанию: {model}")
        
        self.current_model = model
        return model
    
    def ask_question(self, text: str, model: str = None, image_path: str = None) -> dict:
        """
        Основной метод для отправки запроса. Делегирует выполнение запроса текущей стратегии.
        :param text: Текст запроса
        :param model: Модель для использования 
        :param image_path: Путь к изображению
        :return: Словарь с ответом и обновленной историей
        """
        if model is None:
            model = self.current_model
        
        if self.current_strategy_type == "image" and image_path is None:
            image_path = input("Введите путь к изображению: ")
        
        try:
            result = self.current_strategy.execute(
                text=text,
                model=model,
                history=self.history,
                image_path=image_path
            )
            
            self.history = result["history"]
            return result
        
        except Exception as e:
            error_message = f"Ошибка при выполнении запроса: {str(e)}"
            print(error_message)
            return {"response": error_message, "history": self.history}
    
    def get_history(self) -> list:
        """
        Возвращает историю запросов и ответов.
        :return: История сообщений
        """
        return self.history
    
    def clear_history(self) -> None:
        """
        Очищает историю сообщений.
        """
        self.history = []
        print("История сообщений очищена.")
    
    def __call__(self):
        """
        Интерактивный режим работы с чатом
        """
        print('Добро пожаловать в чат с нейронкой')
        print('Команды: "выход" - завершить работу, "история" - показать историю, "очистить" - очистить историю')
        print('         "стратегия" - сменить стратегию, "модель" - выбрать модель')
        
        try:
            strategy_type = input("Выберите стратегию (text/image): ").lower()
            if strategy_type in self.strategies:
                self.change_strategy(strategy_type)
            else:
                print(f"Неизвестная стратегия. Используется стратегия по умолчанию: {self.current_strategy_type}")
            
            self.select_model()
            
            while True:
                question = input("\nВаш вопрос: ")
                
                if question.lower() == 'выход':
                    break
                
                elif question.lower() == 'история':
                    print("\nИстория сообщений:")
                    for msg in self.history:
                        print(f"{msg['role']}: {msg['content']}")
                    continue
                
                elif question.lower() == 'очистить':
                    self.clear_history()
                    continue
                
                elif question.lower() == 'стратегия':
                    strategy_type = input("Выберите стратегию (text/image): ").lower()
                    if strategy_type in self.strategies:
                        self.change_strategy(strategy_type)
                        print(f"Стратегия изменена на: {self.current_strategy_type}")
                    else:
                        print(f"Неизвестная стратегия. Используется текущая стратегия: {self.current_strategy_type}")
                    continue
                
                elif question.lower() == 'модель':
                    self.select_model()
                    continue
                
                image_path = None
                if self.current_strategy_type == "image":
                    image_path = input("Введите путь к изображению: ")
                
                result = self.ask_question(
                    text=question,
                    image_path=image_path
                )
                
                print(f"\nОтвет: {result['response']}")
                
        except KeyboardInterrupt:
            print("\nРабота программы прервана пользователем.")
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
        
        print("\nДо свидания!")

