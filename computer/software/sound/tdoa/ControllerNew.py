import itertools
import statistics
from typing import Dict, Optional, Set

from Position import Position
from TickTimer import TickTimer
from Time import Time
from computer.software.sound import SignalPerceivedReport
from network import Address, Message as NetworkMessage
from .ControllerState import ControllerState
from .LocatedObjectsReporter import LocatedObjectsReporter
from .Locator import Locator
from .SensorInfo import SensorInfo


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
        # self._state = state
        self._speed_of_sound = speed_of_sound
        self._max_wait_time = self._calculate_max_wait_time(self._calculate_distance_between_sensors())
        # self._active_timer = active_timer
        self._address_numbers = [address for address in self.sensor_controllers.keys()]
        self._locator = Locator(
            microphone_positions=[
                self.sensor_controllers[address].position.as_dict() for address in self._address_numbers
            ],
            speed_of_sound=self.speed_of_sound
        )
        self._reports = set()
        self._reports_ttl = {}
        # if active_timer is not None:
        #     self._listen_to_active_timer()

    @property
    def reports(self) -> Set[SignalPerceivedReport]:
        return self._reports

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

    def on_tick(self) -> None:
        super().on_tick()
        self._clean_old_reports()

    def _clean_old_reports(self):
        reports_to_remove = {
            r for r in filter(
            lambda report: self._reports_ttl[report] == 0,
            self.reports
        )
        }
        self._reports.difference_update(reports_to_remove)
        for report in reports_to_remove:
            self._reports_ttl.pop(report)

        for report in self._reports_ttl.keys():
            self._reports_ttl[report] -= 1

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

    def _on_sensor_perceived_signal(self, report: SignalPerceivedReport):
        self._remember_last_report(report)
        self._locate()

    def _all_sensors_reported(self):
        return all((info.last_report is not None for info in self.sensor_controllers.values()))

    def _sensor_already_reported(self, address: Address):
        return self.sensor_controllers[address].last_report is not None

    def _locate(self):
        groups = [c for c in itertools.combinations(self.reports, 5)]
        for group in groups:
            reports = list(group)
            sensors = [report.sensor for report in reports]
            if len(set(sensors)) < 5:
                continue

            # Прямой расчет позиции
            ticks = [
                report.tick for report in reports
            ]

            levels = [
                report.power for report in reports
            ]
            start_tick = min(ticks)
            times_of_arrival_related_to_first_heared_sensor = [tick - start_tick for tick in ticks]
            source_position = Position.from_dict(
                dictionary=Locator(
                    microphone_positions=[sensor.position.as_dict() for sensor in sensors],
                    speed_of_sound=self.speed_of_sound
                ).locate(
                    transit_times=times_of_arrival_related_to_first_heared_sensor
                )
            )

            possible_start_levels = [

                pow(Position.distance(source_position, sensors[i].position), 2) * levels[i] for i in range(0, 5)
            ]

            # max_level = max(possible_start_levels)
            # possible_start_levels = [
            #     l / max_level for l in possible_start_levels.copy()
            # ]

            variance = statistics.pvariance(possible_start_levels)

            if variance < 100:
                self.reports.difference_update(reports)
                print(source_position, variance)

    def _remember_last_report(self, report: SignalPerceivedReport):
        self.reports.add(report)
        self._reports_ttl[report] = 1000

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
