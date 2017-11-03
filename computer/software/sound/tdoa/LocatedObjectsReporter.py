from typing import Set

from Position import Position
from Time import Time
from computer.software import NetworkRelated
from .ObjectLocatedReport import ObjectLocatedReport
from network import Address


class LocatedObjectsReporter(NetworkRelated):
    def __init__(
            self,
            time: Time,
            address: Address,
            addresses_to_send_reports: Set[Address]
    ) -> None:
        super().__init__(time, address)
        self._addresses_to_send_reports = addresses_to_send_reports

    @property
    def addresses_to_send_reports(self) -> Set[Address]:
        return self._addresses_to_send_reports

    def _report(self, position: Position):
        for address in self.addresses_to_send_reports:
            self.protocol.send(
                ObjectLocatedReport(
                    address_from=self.address,
                    address_to=address,
                    tick=self.time.current_tick,
                    position=position
                )
            )
