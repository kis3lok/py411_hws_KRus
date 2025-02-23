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

