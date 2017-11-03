"""
В этом модуле описывается класс Time.
"""
from MulticastDelegate import MulticastDelegate


class Time(object):
    """
    Отсчитывает время в тактах и уведомляет об этом.
    """

    def __init__(self) -> None:
        """
        Конструктор.
        """
        super(Time, self).__init__()
        self._tick_broadcaster = MulticastDelegate()
        self._current_tick = 0

    @property
    def tick_broadcaster(self) -> MulticastDelegate:
        """
        Возвращает ссылку на распространителя информации о тактах.

        Returns:
            MulticastDelegate: Ссылка на распространитель информации о тактах.
        """
        return self._tick_broadcaster

    @property
    def current_tick(self) -> int:
        """
        Возвращает текущий такт.

        Returns:
            int: Текущий такт.
        """
        return self._current_tick

    def to_next_tick(self) -> None:
        """
        Уведомляет всех об окончании текущего такта и переходит на следующий такт.
        """
        self.tick_broadcaster.broadcast()
        self._current_tick += 1
