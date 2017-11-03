from typing import Optional

from Position import Position
from computer.software.sound import SignalPerceivedReport


class SensorInfo:
    def __init__(
            self,
            position: Position,
            last_report: Optional[SignalPerceivedReport]
    ) -> None:
        super().__init__()
        self._position = position
        self._last_report = last_report

    @property
    def position(self) -> Position:
        return self._position

    @property
    def last_report(self) -> Optional[SignalPerceivedReport]:
        return self._last_report

    @last_report.setter
    def last_report(self, value: Optional[SignalPerceivedReport]):
        self._last_report = value
