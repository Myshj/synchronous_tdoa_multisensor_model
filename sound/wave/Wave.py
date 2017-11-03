"""
В этом модуле описывается класс SoundWave.
"""
from Position import Position


class Wave(object):
    """
    Базовый класс для всех звуковых волн.
    """

    def __init__(
            self,
            initial_position: Position,
            initial_power: float
    ):
        """
        Конструктор.

        Args:
            initial_position (Position): Начальная позиция волны.
            initial_power (float): Начальная сила звука.
        """
        super(Wave, self).__init__()
        self._initial_position = initial_position
        self._initial_power = initial_power

    @property
    def initial_position(self) -> Position:
        """
        Возвращает начальную позицию волны.

        Returns:
            Position: Начальная позиция волны.
        """
        return self._initial_position

    @property
    def initial_power(self) -> float:
        """
        Возвращает начальную силу звука.

        Returns:
            float: Начальная сила звука.
        """
        return self._initial_power
