import os
from typing import Union
from PIL import Image
from pillow_heif import register_heif_opener


class ImageCompressor:

    def __init__(self, quality:int) -> None:
        # self.input_path = input_path
        self.__quality = quality
        self.supported_formats = ("png", "jpg", "jpeg")
    
    @property
    def get_quality(self) -> int:
        """
        Возвращает текущее качество сжатия.
        :return: self.__quality
        """
        return self.__quality
    @get_quality.setter
    def set_quality(self, quality: int) -> None:
        """
        Задает новое качество сжатия.
        :param quality (int): Новое качество сжатия.
        :return: None
        """
        self.__quality = quality
    
    def compress_image(self, input_path: str, output_path: str) -> None:
        """
        Метод сжатия изображений.
        :param input_path (str): Путь к исходному изображению.
        :param output_path (str): Путь для сохранения сжатого изображения.
        :return: None
        """
        with Image.open(input_path) as img:
            img.save(output_path, "HEIF", quality=self.__quality)
        print(f"Сжато: {input_path} -> {output_path}")
    
    
    def process_directory(self, directory: str) -> None:
        """
        Метод обработки директории.
        :param directory (str): Путь к директории.
        :return: None
        """
        for root, _, files in os.walk(directory):
            for file in files:
                # Проверяем расширение файла
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    input_path = os.path.join(root, file)
                    output_path = os.path.splitext(input_path)[0] + '.heic'
                    self.compress_image(input_path, output_path)
    def __call__(self, input_path: str, output_path: str) -> None:
        """
        Основная метод программы. Обрабатывает входной путь и запускает сжатие изображений.
        :param input_path (str): Путь к исходному изображению или директории.
        :param output_path (str): Путь для сохранения сжатого изображения.
        :return: None
        """
        register_heif_opener()
        input_path = input_path.strip('"')  # Удаляем кавычки, если они есть
        output_path = output_path.strip('"')
    
        if os.path.exists(input_path):
            if os.path.isfile(input_path):
                # Если указан путь к файлу, обрабатываем только этот файл
                print(f"Обрабатываем файл: {input_path}")
                output_path = os.path.splitext(input_path)[0] + '.heic'
                self.compress_image(input_path, output_path)
            elif os.path.isdir(input_path):
                # Если указан путь к директории, обрабатываем все файлы в ней
                print(f"Обрабатываем директорию: {input_path}")
                # Если директория сохранения не существует, создаем ее.
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                self.process_directory(input_path)
                # Функция process_directory рекурсивно обойдет все поддиректории
                # и обработает все поддерживаемые изображения
        else:
            print("Указанный путь не существует")

def main():
    """
    Функция для поулчения путей к файлам и запуска сжатия.
    """
    user_input: str = input("Введите путь к файлу или директории: ")
    user_output: str = input("Введите путь для сохранения сжатого изображения(ий): ")
    compressor = ImageCompressor(80)
    compressor(user_input, user_output)

if __name__ == "__main__":
    main()

    
    
