"""
В этом модуле описывается класс SoundWaveGeneratorStates.
"""
from enum import Enum


class GeneratorStates(Enum):
    """
    Состояния генератора звуковых волн.

    Attributes:
        time_to_generate_wave (int): Звуковая волна будет сгенерирована в ближайшем будущем.
        waiting (int): Ожидание сигнала на генерацию звуковой волны.
    """
    waiting = 1
    time_to_generate_wave = 2
