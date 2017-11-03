import itertools
import statistics
from typing import Dict, Optional, Set

from Position import Position
from TickTimer import TickTimer
from Time import Time
from computer.software.sound import SignalPerceivedReport
from .LocatedObjectsReporter import LocatedObjectsReporter
from network import Address, Message as NetworkMessage
from .ControllerState import ControllerState
from .SensorInfo import SensorInfo
from .Locator import Locator


class Controller(LocatedObjectsReporter):
    def __init__(
            self,
            time: Time,
            address: Address,
            addresses_to_send_reports: Set[Address],
            sensor_controllers: Dict[Address, SensorInfo],
            state: ControllerState,
            speed_of_sound: float,
            active_timer: Optional[TickTimer]
    ) -> None:
        super().__init__(time, address, addresses_to_send_reports)
        if len(sensor_controllers) < 5:
            raise ValueError('too few sensors')
        self._sensor_controllers = sensor_controllers
        self._state = state
        self._speed_of_sound = speed_of_sound
        self._max_wait_time = self._calculate_max_wait_time(self._calculate_distance_between_sensors())
        self._active_timer = active_timer
        self._address_numbers = [address for address in self.sensor_controllers.keys()]
        self._locator = Locator(
            microphone_positions=[
                self.sensor_controllers[address].position.as_dict() for address in self._address_numbers
            ],
            speed_of_sound=self.speed_of_sound
        )
        if active_timer is not None:
            self._listen_to_active_timer()

    @property
    def sensor_controllers(self) -> Dict[Address, SensorInfo]:
        return self._sensor_controllers

    @property
    def state(self) -> ControllerState:
        return self._state

    @property
    def speed_of_sound(self) -> float:
        return self._speed_of_sound

    @property
    def max_wait_time(self) -> int:
        return self._max_wait_time

    @property
    def active_timer(self) -> TickTimer:
        return self._active_timer

    def _calculate_max_wait_time(self, max_distance_between_sensors: float):
        return int(max_distance_between_sensors * 1.25 / self.speed_of_sound)

    def _calculate_distance_between_sensors(self):
        return max(
            [
                Position.distance(pair[0].position, pair[1].position) for pair in
                itertools.combinations(self.sensor_controllers.values(), 2)
            ]
        )

    def is_from_controlled_sensors(self, message: NetworkMessage):
        return message.address_from in self.sensor_controllers.keys()

    def is_valid_message_from_controlled_sensor(self, message: NetworkMessage):
        if not self.is_for_me(message):
            raise ValueError('message not for me')
        return self.is_for_me(message) and self.is_from_controlled_sensors(message)

    def _on_sensor_perceived_signal(self, report: NetworkMessage):
        if self.state == ControllerState.waiting:
            self._remember_last_report(report)
            self._activate()
        elif self.state == ControllerState.active:
            if self._sensor_already_reported(report.address_from):
                pass
            else:
                self._remember_last_report(report)

    def _all_sensors_reported(self):
        return all((info.last_report is not None for info in self.sensor_controllers.values()))

    def _sensor_already_reported(self, address: Address):
        return self.sensor_controllers[address].last_report is not None

    def _activate(self):
        self._state = ControllerState.active
        self._active_timer = TickTimer(self.time, self.max_wait_time)
        self._listen_to_active_timer()

    def _remember_last_report(self, report):
        self.sensor_controllers[report.address_from].last_report = report

    def _listen_to_active_timer(self):
        self._active_timer.time_elapsed_broadcaster.register(self._on_activity_time_elapsed)

    def _on_activity_time_elapsed(self):
        if self._all_sensors_reported():
            self._report(
                position=self._calculate_estimated_position()
            )

            self._forget_last_reports()
            self._active_timer = None
            self._state = ControllerState.waiting
        else:
            raise ValueError('not all sensors reported')

    def _calculate_average_signal_power(self) -> float:
        return statistics.mean([info.last_report.power for info in self.sensor_controllers.values()])

    def _calculate_estimated_position(self) -> Position:
        ticks = [
            self.sensor_controllers[address].last_report.tick for address in self._address_numbers
        ]
        start_tick = min(ticks)
        return Position.from_dict(self._locator.locate([[tick - start_tick] for tick in ticks]))

    def _forget_last_reports(self):
        for info in self.sensor_controllers.values():
            info.last_report = None

    def _on_network_message(self, message: NetworkMessage):
        super()._on_network_message(message)

        if isinstance(message, SignalPerceivedReport) and self.is_valid_message_from_controlled_sensor(message):
            self._on_sensor_perceived_signal(message)
