"""Summary
"""
from typing import Dict

import numpy


class Position(object):
    """
    Позиция в трёхмерном пространстве.

    Attributes:
        x (float): Координата x.
        y (float): Координата y.
        z (float): Координата z.
    """

    def __str__(self) -> str:
        return 'x={0}, y={1}, z={2}'.format(self.x, self.y, self.z)

    def __init__(
            self,
            x: float,
            y: float,
            z: float
    ):
        """
        Конструктор

        Args:
            x (float): Координата x.
            y (float): Координата y.
            z (float): Координата z.
        """
        super(Position, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def as_array(self) -> numpy.array:
        """
        Возвращает представление позиции в виде массива [x, y, z].

        Returns:
            numpy.array: Представление позиции в виде массива [x, y, z]
        """
        return numpy.array((self.x, self.y, self.z))

    def as_dict(self) -> Dict[str, float]:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    @staticmethod
    def from_dict(dictionary: Dict[str, float]) -> 'Position':
        return Position(
            x=dictionary.get('x', 0.0),
            y=dictionary.get('y', 0.0),
            z=dictionary.get('z', 0.0)
        )

    @staticmethod
    def distance(a, b) -> float:
        """
        Считает расстояние между двумя позициями.

        Args:
            a (TYPE): Позиция A.
            b (TYPE): Позиция B.

        Returns:
            float: Расстояние между двумя позициями.
        """
        return numpy.linalg.norm(a.as_array() - b.as_array())

    @property
    def x(self) -> float:
        """
        Возвращает текущее значение координаты x.

        Returns:
            float: Текущее значение координаты x.
        """
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """
        Устанавливает новое значение координаты x.

        Args:
            value (float): Новое значение координаты x.
        """
        self._x = value

    @property
    def y(self) -> float:
        """
        Возвращает текущее значение координаты y.

        Returns:
            float: Текущее значение координаты y.
        """
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """
        Устанавливает новое значение координаты y.

        Args:
            value (float): Новое значение координаты y.
        """
        self._y = value

    @property
    def z(self) -> float:
        """
        Возвращает текущее значение координаты z.

        Returns:
            float: Текущее значение координаты z.
        """
        return self._z

    @z.setter
    def z(self, value: float) -> None:
        """
        Устанавливает новое значение координаты z.

        Args:
            value (float): Новое значение координаты z.
        """
        self._z = value
