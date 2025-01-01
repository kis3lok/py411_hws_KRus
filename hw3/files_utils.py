
import json


def write_json(data, file_path: str, encoding: str = "utf-8", indent: int = 4) -> None:
    """
    Записывает данные в JSON файл.
    :param data: Данные для записи.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :param indent: Отступы для каждого уровня вложенности.
    :return: None
    """
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)


def read_json(file_path: str, encoding: str = "utf-8") -> dict:
    """
    Читает данные из JSON-файла.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :return: Данные, считанные из файла.
    """
    with open(file_path, "r", encoding=encoding) as file:
        return json.load(file)




def append_json(file_path: str, data: list[dict], encoding: str = "utf-8", indent: int = 4) -> None:
    """
    Добавляет данные в JSON файл.
    :param data: Список словарей с данными для добавления.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :return: None
    """
    
    with open(file_path, "r", encoding=encoding) as file:
        python_data = json.load(file)

    if not isinstance(python_data, list):
        raise TypeError("oonly addding to JSON arrays is supported")

    python_data.extend(data)

    with open(file_path, "w", encoding=encoding) as file:
        json.dump(python_data, file, ensure_ascii=False, indent=4)




# 0000000000000000000000000000
import csv
def write_csv(data: list[list], file_path: str, encoding: str = "utf-8-sig", delimiter: str = ";") -> None:
    """
    Записывает данные в CSV файл.
    :param data: Данные для записи.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :param delimiter: Разделитель данных.
    :return: None
    """
    with open(file_path, "w", encoding=encoding, newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)



def read_csv(file_path: str, encoding: str = "utf-8-sig", delimiter: str = ";") -> list[list]:
    """
    Читает данные из CSV-файла.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :param delimiter: Разделитель данных.
    :return: Данные, считанные из файла.
    """
    with open(file_path, "r", encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)



def append_csv(file_path: str, data, encoding: str = "utf-8-sig", delimiter: str = ";") -> None:
    """
    Добавляет данные в CSV файл.
    :param data: Список списков с данными для добавления.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла.
    :param delimiter: Разделитель данных.
    :return: None
    """
    with open(file_path, "a", encoding=encoding, newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)



