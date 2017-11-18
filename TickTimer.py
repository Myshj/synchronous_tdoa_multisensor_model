"""
В этом модуле описывается класс TickTimer.
"""
from MulticastDelegate import MulticastDelegate
from Time import Time
from TimeRelated import TimeRelated


class TickTimer(TimeRelated):
    """
    Отсчитывает заданное число тактов, после чего уведомляет всех о том, что отсчёт завершен.
    """

    def __init__(
            self,
            time: Time,
            interval: int
    ) -> None:
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            interval (int): Число тактов до события.
        """
        super(TickTimer, self).__init__(time)
        self._interval = interval
        self._ticks_remaining = self.interval
        self._time_elapsed_broadcaster = MulticastDelegate()

    @property
    def interval(self) -> int:
        """
        Возвращает заданный интервал работы.

        Returns:
            int: Заданный интервал работы.
        """
        return self._interval

    @property
    def ticks_remaining(self) -> int:
        """
        Возвращает число тактов до события.

        Returns:
            int: Число тактов до события.
        """
        return self._ticks_remaining

    @property
    def time_elapsed_broadcaster(self) -> MulticastDelegate:
        """
        Возвращает уведомитель о вышедшем времени.

        Returns:
            MulticastDelegate: Уведомитель о вышедшем времени.
        """
        return self._time_elapsed_broadcaster

    def on_tick(self) -> None:
        """
        Вызывается каждый такт.
        Отсчитыает время до события.
        """
        super().on_tick()
        if self.ticks_remaining == 0:
            self.time_elapsed_broadcaster.broadcast()
        self._ticks_remaining -= 1
