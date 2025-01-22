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
    
    
    
