"""
В этом модуле описывается класс SoundSensor.
"""
from MulticastDelegate import MulticastDelegate
from Physical import Physical
from Position import Position
from Time import Time


class Sensor(Physical):
    """
    Датчик звука.
    """

    def __init__(
            self,
            time: Time,
            position: Position,
            min_sound_power: float
    ):
        """
        Конструктор.

        Args:
            time (Time): Время, в котором существует объект.
            position (Position): Позиция объекта в пространстве.
            min_sound_power (float): Минимальная слышимая сила звука.
        """
        super(Sensor, self).__init__(time, position)
        self._min_sound_power = min_sound_power
        self._perceived_something_broadcaster = MulticastDelegate()

    @property
    def min_sound_power(self) -> float:
        """
        Возвращает минимальную слышимую силу звука.

        Returns:
            float: Минимальная слышимая сила звука.
        """
        return self._min_sound_power

    @property
    def perceived_something_broadcaster(self) -> MulticastDelegate:
        """
        Возвращает ссылку на уведомитель о том. что датчик что-то услышал.

        Returns:
            MulticastDelegate: Ссылка на уведомитель о том. что датчик что-то услышал.
        """
        return self._perceived_something_broadcaster

    def perceive_signal(self, power: float) -> None:
        """
        Услышать сигнал заданной силы.
        Если сила поступившего сигнала меньше заданного порога, то такой сигнал услышан не будет.

        Args:
            power (float): Сила поступившего сигнала.

        Returns:
            None: Description
        """
        if power < self.min_sound_power:
            return
        self._notify_about_perceived_signal(power)

    def _notify_about_perceived_signal(self, power: float) -> None:
        """
        Уведомление о последнем услышанном сигнале.
        """
        self.perceived_something_broadcaster.broadcast(power)
