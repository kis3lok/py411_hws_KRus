

class TxtFileHandler:
    """
    Класс для работы с TXT файлами. Читает, записывает, добавляет.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self, encoding: str = "utf-8") -> str:
        """
        Читает содержимое файла и возвращает его в виде строки. Возвращает пустую строку, если файл не найден.
        :param encoding: Кодировка файла.
        :return: Содержимое файла в виде строки.
        """
        try:
            with open(self.file_path, "r", encoding=encoding) as file:
                data = file.read()
            return data
        except FileNotFoundError:
            print("File '{self.file_path}' not found")
            return ""
        except Exception as e:
            print(f'An error accured while trying to read the file: {e}')

    