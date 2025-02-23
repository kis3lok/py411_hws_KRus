from typing import List, Tuple, Set, Dict, Callable, Iterable, Iterator, Any, Union, Optional
# 1

def password_checker(func: Callable) -> Callable:
    """
    Декоратор для проверки пароля
    :param func: функция, которую декорируем
    :return: функция
    """
    nums = "0123456789"
    caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    regs = "abcdefghijklmnopqrstuvwxyz"
    specs = "!@#$%^&*()_+"
    def wrapper(passw:str):

        if len(passw) >= 8 and  any(i in nums for i in passw) and any(i in caps for i in passw) and any(i in regs for i in passw) and any(i in specs for i in passw):
            return func(passw)
        else:
            raise ValueError
            

    return wrapper

@password_checker
def register_user(passw:str) -> None:
    """
    Функция регистрации пользователя с проверкой пароля
    :param passw: пароль пользователя
    :return: None
    """
    print('The password is alr!')


register_user("Aa1!aaaa")
# register_user("aaaA1!a")
# register_user("Aaaaa!aa")
# register_user("aa1!aaa")
# register_user("Aaa1aaa")
# register_user("AAAAA!1AAA")

# 2
import csv

def password_validator(length: int = 8, nums: int = 1, uppercase: int = 1, lowercase: int = 1, special_chars: int = 1) -> Callable:
    """
    Обёртка декоратора для проврки пароля с аргументами
    :param length: необходимая длина пароля
    :param nums: необходимое количество цифр
    :param uppercase: необходимое количество заглавных букв
    :param lowercase: необходимое количество строчных букв
    :param special_chars: необходимое количество специальных символов
    :return: декоратор
    """
    def decorator(func: Callable) -> Callable:   
        """
        Декоратор для проверки пароля
        :param func: функция, которую декорируем
        :return: функция
        """
        def wrapper(username:str, passw: str):
            upprcs = sum(1 for i in passw if i.isupper())
            lwrcs = sum(1 for i in passw if i.islower())
            spcl = sum(1 for i in passw if not i.isalnum())
            nmbrs = sum(1 for i in passw if i.isdigit())
            if len(passw) >= length and nmbrs >= nums and upprcs >= uppercase and lwrcs >= lowercase and spcl >= special_chars:
                return func(username,passw )
            else:
                raise ValueError('The password is not valid, please check the requirements.')

        return wrapper
    return decorator
    
