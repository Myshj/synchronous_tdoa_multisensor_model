"""
В этом модуле описывается класс SphericalSoundWave.
"""
from Position import Position
from sound.wave.Wave import Wave


class Spherical(Wave):
    """
    Сферическая звуковая волна.
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
        super(Spherical, self).__init__(initial_position, initial_power)
        self._current_radius = 0.0
        self._current_power = self.initial_power

    @property
    def current_radius(self) -> float:
        """
        Возвращает текущий радиус сферической звуковой волны.

        Returns:
            float: Текущий радиус сферической звуковой волны.
        """
        return self._current_radius

    @current_radius.setter
    def current_radius(self, value: float) -> None:
        """
        Устанавливает новый радиус сферической звуковой волны.

        Args:
            value (float): Новый радиус сферической звуковой волны.
        """
        self._current_radius = value

    @property
    def current_power(self) -> float:
        """
        Возвращает текущую силу звука сферической звуковой волны.

        Returns:
            float: Текущая сила звука сферической звуковой волны.
        """
        return self._current_power

    @current_power.setter
    def current_power(self, value: float) -> None:
        """
        Устанавливает новую силу звука сферической звуковой волны.

        Args:
            value (float): Новая сила звука сферической звуковой волны.
        """
        self._current_power = value
