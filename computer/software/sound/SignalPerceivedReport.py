from network import MessageWithTimestamp, Address
from computer.hardware.sound import Microphone


class SignalPerceivedReport(MessageWithTimestamp):
    def __init__(
            self,
            address_from: Address,
            address_to: Address,
            sensor: Microphone,
            power: float,
            tick: int
    ):
        super().__init__(address_from, address_to, tick)
        self._sensor = sensor
        self._power = power

    @property
    def power(self) -> float:
        return self._power

    @property
    def sensor(self) -> Microphone:
        return self._sensor

    def __str__(self):
        return 'signal perceived at {tick} with power {power}'.format(tick=self.tick, power=self.power)
