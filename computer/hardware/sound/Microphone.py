from Position import Position
from Time import Time
from sound import Sensor as SoundSensor
from Hardware import Hardware
from .States import States
from MulticastDelegate import MulticastDelegate


class Microphone(Hardware):
    def __init__(
            self,
            time: Time,
            position: Position,
            sensor: SoundSensor,
            state: States
    ) -> None:
        super().__init__(time, position)
        self._sensor = sensor
        sensor.perceived_something_broadcaster.register(self._on_sensor_activated)
        self._state = state
        self._signal_perceived_broadcaster = MulticastDelegate()

    @property
    def sensor(self) -> SoundSensor:
        return self._sensor

    @property
    def state(self) -> States:
        return self._state

    @property
    def signal_perceived_broadcaster(self) -> MulticastDelegate:
        return self._signal_perceived_broadcaster

    def _on_sensor_activated(self, power: float):
        if self.state == States.waiting:
            self.signal_perceived_broadcaster.broadcast(power)
