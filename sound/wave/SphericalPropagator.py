"""
В этом модуле описывается класс SphericalSoundWavePropagator.
"""
from typing import Set

from .PropagatorStates import PropagatorStates as SoundWavePropagatorStates
from .Spherical import Spherical as SphericalSoundWave

from MulticastDelegate import MulticastDelegate
from Position import Position
from Time import Time
from TimeRelated import TimeRelated
from sound.Sensor import Sensor


class SphericalPropagator(TimeRelated):
    """
    Распространитель сферических звуковых волн.
    """

    def __init__(
            self,
            time: Time,
            sound_wave: SphericalSoundWave,
            sound_sensors: Set[Sensor],
            speed_of_sound: float,
            min_sound_power: float
    ):
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            sound_wave (Spherical): Звуковая волна, которую нужно распространить.
            sound_sensors (Set[Sensor]): Датчики, среди которых нужно распространить звуковую волну.
            speed_of_sound (float): Скорость звука.
            min_sound_power (float): Минимальная сила звука, при которой волну ещё нужно распространять.
        """
        super(SphericalPropagator, self).__init__(time)
        self._state = SoundWavePropagatorStates.propagating
        self._sound_wave = sound_wave
        self._sound_sensors = sound_sensors
        self._speed_of_sound = speed_of_sound
        self._min_sound_power = min_sound_power
        self._end_of_propagation_broadcaster = MulticastDelegate()

    @property
    def state(self) -> SoundWavePropagatorStates:
        """Summary

        Returns:
            PropagatorStates: Description
        """
        return self._state

    @property
    def min_sound_power(self) -> float:
        """
        Возвращает минимальную силу звука, при которой волну ещё нужно распространять.

        Returns:
            float: Минимальная сила звука, при которой волну ещё нужно распространять.
        """
        return self._min_sound_power

    @property
    def end_of_propagation_broadcaster(self) -> MulticastDelegate:
        """
        Возвращает ссылку на уведомитель о том, что звуковая волна распространена и затухла.

        Returns:
            MulticastDelegate: Ссылка на уведомитель о том, что звуковая волна распространена и затухла.
        """
        return self._end_of_propagation_broadcaster

    def on_tick(self):
        """
        Вызывается каждый такт.
        Если звуковая волна ещё не затухла, распространяет её дальше.
        Иначе заканчивает распространения.
        """
        super().on_tick()
        if self._sound_wave.current_power >= self.min_sound_power:
            self._propagate()
        else:
            self._end_propagation()

    def _propagate(self):
        """
        Распространить волну дальше.
        """
        old_radius = self._sound_wave.current_radius
        self._update_radius()
        new_radius = self._sound_wave.current_radius

        self._update_power()

        for sensor in self._sound_sensors:
            distance_to_wave_origin = Position.distance(sensor.position, self._sound_wave.initial_position)
            if old_radius <= distance_to_wave_origin < new_radius:
                sensor.perceive_signal(self._sound_wave.current_power)

    def _end_propagation(self) -> None:
        """
        Закончить распространение звуковой волны и уведомить об этом.
        """
        self._state = SoundWavePropagatorStates.end_of_propagation
        self.end_of_propagation_broadcaster.broadcast()

    def _calculate_power_at_distance(self, initial_power: float, distance: float) -> float:
        """
        Посчитать силу звука на расстоянии от источника при прямолинейном распространении.

        Args:
            initial_power (float): Начальная сила звука.
            distance (float): Расстояние, для которого нужно посчитать силу звука.

        Returns:
            float: Сила звука на заданном расстоянии.
        """
        return initial_power / (distance ** 2)

    def _update_radius(self) -> None:
        """
        Обновить радиус звуковой волны для распространения.

        ВСЕГДА СНАЧАЛА ОБНОВЛЯТЬ РАДИУС.
        СИЛУ ЗВУКА ОБНОВЛЯТЬ ПОСЛЕ.
        """
        current_radius = self._sound_wave.current_radius

        next_radius = current_radius + self._speed_of_sound
        self._sound_wave.current_radius = next_radius

    def _update_power(self) -> None:
        """
        Обновить силу звуковой волны.

        ВСЕГДА СНАЧАЛА ОБНОВЛЯТЬ РАДИУС.
        СИЛУ ЗВУКА ОБНОВЛЯТЬ ПОСЛЕ.
        """
        next_power = self._calculate_power_at_distance(self._sound_wave.initial_power, self._sound_wave.current_radius)
        self._sound_wave.current_power = next_power
