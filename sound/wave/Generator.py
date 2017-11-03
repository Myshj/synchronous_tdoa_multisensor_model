"""
В этом модуле описывается класс SoundWaveGenerator
"""
from .Spherical import Spherical as SphericalSoundWave

from MulticastDelegate import MulticastDelegate
from Physical import Physical
from Position import Position
from TickTimer import TickTimer
from Time import Time
from sound.wave.GeneratorStates import GeneratorStates


class Generator(Physical):
    """
    С заданной периодичностью генерирует сферические звуковые волны.
    """

    def __init__(
            self,
            time: Time,
            position: Position,
            interval: int,
            power: float
    ):
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            position (Position): Позиция объекта в пространстве.
            interval (int): Интервал между генерациями волн.
            power (float): Сила генерируемых волн.
        """
        super(Generator, self).__init__(time, position)
        self._interval = interval
        self._prepare_to_wave_generation()
        self._power = power
        self._wave_generated_broadcaster = MulticastDelegate()

    @property
    def interval(self) -> int:
        """
        Возвращает интервал между генерациями волн.

        Returns:
            int: Интервал между генерациями волн.
        """
        return self._interval

    @property
    def power(self) -> float:
        """
        Возвращает силу генерируемых волн.

        Returns:
            float: Сила генерируемых волн.
        """
        return self._power

    @property
    def wave_generated_broadcaster(self) -> MulticastDelegate:
        """
        Возвращает уведомитель о генерациях волн.

        Returns:
            MulticastDelegate: Уведомитель о генерациях волн.
        """
        return self._wave_generated_broadcaster

    def on_tick(self) -> None:
        """
        Вызывается каждый такт.
        Если истёк интервал между генерациями волн, то генерирует новую волну и готовится к генерации следующей.
        """
        super().on_tick()
        if self._state == GeneratorStates.time_to_generate_wave:
            self._generate_wave()
            self._prepare_to_wave_generation()

    def _prepare_to_wave_generation(self) -> None:
        """
        Подготовка к генерации следующей волны.
        """
        self._sound_generation_timer = TickTimer(self.time, self.interval)
        self._sound_generation_timer.time_elapsed_broadcaster.register(self._it_is_time_to_generate_wave)
        self._state = GeneratorStates.waiting

    def _it_is_time_to_generate_wave(self) -> None:
        """
        Уведомление самого себя о том, что в скором времени нужно будет генерировать новую волну.
        """
        self._state = GeneratorStates.time_to_generate_wave

    def _generate_wave(self) -> None:
        """
        Генерирование новой звуковой волны и уведомление об этом.
        """
        self._wave_generated_broadcaster.broadcast(
            SphericalSoundWave(
                initial_position=self.position,
                initial_power=self.power
            )
        )
