from typing import Set

from Position import Position
from TickTimer import TickTimer
from Time import Time
from computer.software.sound.duplicates_filter import Filtration
from computer.software.sound.tdoa import LocatedObjectsReporter, ObjectLocatedReport
from network import Address, Message as NetworkMessage


class Filter(LocatedObjectsReporter):
    def __init__(
            self,
            time: Time,
            address: Address,
            addresses_to_send_reports: Set[Address],
            time_window: int,
            max_deviation_in_space: float,
            filtrations: Set[Filtration]
    ) -> None:
        super().__init__(time, address, addresses_to_send_reports)
        self._max_deviation_in_space = max_deviation_in_space
        self._time_window = time_window
        self._filtrations = filtrations
        for filtration in filtrations:
            self._wait_for_filtration_end(filtration)

    @property
    def timer(self) -> int:
        return self._time_window

    def _wait_for_filtration_end(self, filtration: Filtration):
        filtration.complete_broadcaster.register(self._on_filtration_complete)

    def _on_filtration_complete(self, filtration: Filtration):
        self._report(filtration.reference)
        self._filtrations.remove(filtration)
        print(filtration.reference)

    def _on_network_message(self, message: NetworkMessage):
        super()._on_network_message(message)
        if isinstance(message, ObjectLocatedReport):
            self._on_new_report(message)

    def _on_new_report(self, report: ObjectLocatedReport):
        for filtration in self._filtrations:
            if filtration.is_near_reference(report.position):
                filtration.add(report.position)
                return
        self._start_new_filtration(report)

    def _start_new_filtration(self, report: ObjectLocatedReport):
        filtration = Filtration(
                timer=TickTimer(
                    time=self.time,
                    interval=self._time_window
                ),
                points={report.position},
                max_deviations=Position(
                    x=self._max_deviation_in_space,
                    y=self._max_deviation_in_space,
                    z=self._max_deviation_in_space
                )
            )
        self._wait_for_filtration_end(filtration)
        self._filtrations.add(filtration)
