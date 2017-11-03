"""
В этом модуле описывается класс MulticastDelegate.
"""
from typing import Callable
from weakref import WeakMethod


class MulticastDelegate(object):
    """
    Хранит ссылки на функции.
    Вызывает их всех при выполнении метода broadcast.
    """

    def __init__(self):
        """
        Конструктор.
        """
        super(MulticastDelegate, self).__init__()
        self._listeners = set()

    def register(self, listener: Callable) -> None:
        """
        Регистрирует ссылку функцию для последующих вызовов.
        В дальнейшем вызовы broadcast будут вызывать и эту функцию.

        Args:
            listener (Callable): Функция для последующих вызовов.
        """
        self._listeners.add(WeakMethod(listener))

    def unregister(self, listener: Callable) -> None:
        """
        Удаляет ссылку на функцию.
        В дальнейшем вызовы broadcast не будут вызывать эту функцию.

        Args:
            listener (Callable): Функция для удаления.
        """
        self._listeners.discard(WeakMethod(listener))

    def broadcast(self, *args, **kwargs) -> None:
        """
        Вызывает все зарегистрированные функции с заданными аргументами.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Аргументы с ключевыми словами.
        """
        deleted_listeners = set()
        for listener in self._listeners.copy():
            if listener():
                listener()(*args, **kwargs)
            else:
                deleted_listeners.add(listener)
        self._listeners -= deleted_listeners
