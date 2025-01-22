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

    
    
