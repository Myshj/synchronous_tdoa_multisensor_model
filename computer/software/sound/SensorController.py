from typing import Set

from Time import Time
from computer import Computer
from computer.hardware.sound import Microphone
from computer.software import NetworkRelated
from network import Address
from .SignalPerceivedReport import SignalPerceivedReport


class SensorController(NetworkRelated):
    def __init__(
            self,
            time: Time,
            address: Address,
            addresses_to_report_about_signals: Set[Address]

    ) -> None:
        super().__init__(time, address)
        self._addresses_to_report_about_signals = addresses_to_report_about_signals
        self._sensor = None

    @property
    def addresses_to_report_about_signals(self) -> Set[Address]:
        return self._addresses_to_report_about_signals

    @property
    def sensor(self) -> Microphone:
        return self._sensor

    def install(
            self,
            computer: Computer
    ):
        super().install(computer)
        self._connect_to_sensor()

    def _connect_to_sensor(self):
        for hardware in self.computer.hardware:
            if isinstance(hardware, Microphone):
                self._sensor = hardware
                hardware.signal_perceived_broadcaster.register(self._on_sensor_perceived_signal)
                return
        raise ValueError('microphone not available')

    def _on_sensor_perceived_signal(self, power: float):
        for address_to_report in self.addresses_to_report_about_signals:
            self.protocol.send(
                SignalPerceivedReport(
                    address_from=self.address,
                    address_to=address_to_report,
                    sensor=self.sensor,
                    power=power,
                    tick=self.time.current_tick
                )
            )
