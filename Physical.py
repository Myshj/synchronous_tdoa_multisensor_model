"""
В этом модуле описывается класс Physical.
"""
from Position import Position
from Time import Time
from TimeRelated import TimeRelated


class Physical(TimeRelated):
    """
    Базовый класс для всех физических объектов.
    """

    def __init__(
            self,
            time: Time,
            position: Position
    ) -> None:
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            position (Position): Позиция объекта в пространстве.
        """
        super(Physical, self).__init__(time)
        self._position = position

    @property
    def position(self) -> Position:
        """
        Возвращает позицию объекта в пространстве.

        Returns:
            Position: Позиция объекта в пространстве.
        """
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        """
        Устанавливает новую позицию объекта в пространстве.

        Args:
            value (Position): Новая позиция объекта в пространстве.
        """
        self.position.x = value.x
        self.position.y = value.y
        self.position.z = value.z
