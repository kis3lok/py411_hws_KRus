

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

    def write_file(self, *data: str, encoding: str = "utf-8") -> None:
            """
            Записывает переданную строку в файл. Если файл существует, он перезаписывается.
            :param data: Строка с данными для записи.
            :param encoding: Кодировка файла.
            :return: None
            """
            try:
                with open(self.file_path, "w", encoding=encoding) as file:
                    for line in data:  
                        file.write(line + "\n")
            except Exception as e:
                print(f'An error accured while trying to write to the file: {e}')


    def append_file(self, *data: str, encoding: str = "utf-8") -> None:
        """
        Добавляет переданную строку в конец файла. Если файл не существует, он будет создан.
        :param data: Строка с данными для добавления.
        :param encoding: Кодировка файла.
        :return: None
        """
        try:
            with open(self.file_path, "a", encoding=encoding) as file:
                for line in data:
                    file.write(line + "\n")
        except Exception as e:
            print(f'An error accured while trying to append to the file: {e}')
