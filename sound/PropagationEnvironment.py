"""
В этом модуле описывается класс SoundPropagationEnvironment.
"""
from weakref import WeakSet

from Time import Time
from TimeRelated import TimeRelated
from sound.Sensor import Sensor
from sound.wave import (
    Wave as SoundWave,
    Generator as SoundWaveGenerator,
    PropagatorStates as SoundWavePropagatorStates,
    Spherical as SphericalSoundWave,
    SphericalPropagator as SphericalSoundWavePropagator
)


class PropagationEnvironment(TimeRelated):
    """
    Среда распространения звука от источников к датчикам.
    """

    def __init__(
            self,
            time: Time,
            speed_of_sound: float,
            min_sound_power: float
    ):
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            speed_of_sound (float): Скорость звука в среде.
            min_sound_power (float): Минимальная сила звука, при которой его ещё нужно распространять.
        """
        super(PropagationEnvironment, self).__init__(time)
        self._speed_of_sound = speed_of_sound
        self._min_sound_power = min_sound_power
        self._sound_sources = WeakSet()
        self._sound_sensors = WeakSet()
        self._propagators = set()

    @property
    def speed_of_sound(self) -> float:
        """
        Возвращает скорость звука в среде.

        Returns:
            float: Скорость звука в среде.
        """
        return self._speed_of_sound

    @property
    def min_sound_power(self) -> float:
        """
        Возвращает минимальную силу звука, при которой его ещё нужно распространять.

        Returns:
            float: Минимальная сила звука, при которой его ещё нужно распространять.
        """
        return self._min_sound_power

    def register_sound_sensor(self, sound_sensor: Sensor) -> None:
        """
        Регистрация звукового датчика в среде.
        Теперь этот датчик сможет слышать звук от источников звука в среде.

        Args:
            sound_sensor (Sensor): Звуковой датчик для регистрации.
        """
        self._sound_sensors.add(sound_sensor)

    def unregister_sound_sensor(self, sound_sensor: Sensor) -> None:
        """
        Удаление звукового датчика из среды.
        Теперь этот датчик не сможет слышать звук от источников звука в среде.

        Args:
            sound_sensor (Sensor): Звуковой датчик для удаления.
        """
        self._sound_sensors.discard(sound_sensor)

    def register_sound_source(self, sound_source: SoundWaveGenerator) -> None:
        """
        Регистрация источника звука в среде.
        Теперь звуковые датчики смогут услышать сигналы от этого источника.

        Args:
            sound_source (Generator): Источник звука для регистрации.
        """
        self._sound_sources.add(sound_source)
        sound_source.wave_generated_broadcaster.register(self._on_sound_wave_generated)

    def unregister_sound_source(self, sound_source: SoundWaveGenerator) -> None:
        """
        Удаление источника звука из среды.
        Теперь звуковые датчики не смогут услышать сигналы от этого источника.

        Args:
            sound_source (Generator): Источник звука для удаления.
        """
        self._sound_sources.discard(sound_source)
        sound_source.wave_generated_broadcaster.unregister(self._on_sound_wave_generated)

    def _on_sound_wave_generated(self, sound_wave: SoundWave) -> None:
        """
        Вызывается каждый раз при генерации звуковой волны связанными источниками звука.
        Начинает распространение сгенерированной звуковой волны.

        Args:
            sound_wave (Wave): Сгенерированная звуковая волна.
        """
        self._start_wave_propagation(sound_wave)

    def _start_wave_propagation(self, sound_wave: SoundWave) -> None:
        """
        Начинает распространение звуковой волны.

        Args:
            sound_wave (Wave): Звуковая волна для распространения.
        """
        if isinstance(sound_wave, SphericalSoundWave):
            propagator = SphericalSoundWavePropagator(
                time=self.time,
                sound_wave=sound_wave,
                sound_sensors=self._sound_sensors,
                speed_of_sound=self.speed_of_sound,
                min_sound_power=self.min_sound_power
            )
            propagator.end_of_propagation_broadcaster.register(self._clean_propagators)
            self._propagators.add(propagator)

    def _clean_propagators(self) -> None:
        """
        Удаляет из множества распространителей волн тех, чьи волны уже затухли.
        """
        for propagator in self._propagators.copy():
            if propagator.state == SoundWavePropagatorStates.end_of_propagation:
                self._propagators.discard(propagator)
