"""
В этом модуле описывается класс TimeRelated.
"""
from Tickable import Tickable
from Time import Time


class TimeRelated(Tickable):
    """
    Базовый класс для всех объектов, существующих во времени.
    """

    def __init__(self, time: Time) -> None:
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
        """
        super(TimeRelated, self).__init__()
        self._time = time
        self.time.tick_broadcaster.register(self.on_tick)

    @property
    def time(self) -> Time:
        """
        Возвращает время, в котором существует объект.

        Returns:
            Time: Время, в котором существует объект.
        """
        return self._time
