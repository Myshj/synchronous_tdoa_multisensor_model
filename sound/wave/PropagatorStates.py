"""
В этом модуле описывается класс SoundWavePropagatorStates.
"""
from enum import Enum


class PropagatorStates(Enum):
    """
    Состояния распространителя звуковых волн.

    Attributes:
        end_of_propagation (int): Звуковая волна распространена и затухла.
        propagating (int): Звуковая волна распространяется.
    """
    propagating = 1
    end_of_propagation = 2
