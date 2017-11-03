"""
В этом модуле описывается класс SoundSensorStates.
"""
from enum import Enum


class States(Enum):
    """
    Состояния звукового датчика.

    Attributes:
        perceived_something (int): Датчик услышал сигнал.
        waiting (int): Ожидание сигнала.
    """
    waiting = 1
    perceived_something = 2
