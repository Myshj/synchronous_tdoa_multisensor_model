import statistics
from typing import Set

from Position import Position
from TickTimer import TickTimer
from Waiting import Waiting


class Filtration(Waiting):
    def __init__(
            self,
            timer: TickTimer,
            points: Set[Position],
            max_deviations: Position
    ) -> None:
        super().__init__(timer)
        if len(points) == 0:
            raise ValueError('should contain at least one point')
        self._points = points
        self._update_reference()
        self._max_deviations = max_deviations

    @property
    def reference(self) -> Position:
        return self._reference

    @property
    def max_deviations(self) -> Position:
        return self._max_deviations

    def is_near_reference(self, point: Position):
        return (
            abs(point.x - self.reference.x) < self.max_deviations.x and
            abs(point.y - self.reference.y) < self.max_deviations.y and
            abs(point.z - self.reference.z) < self.max_deviations.z
        )

    def add(self, point: Position):
        self._points.add(point)
        self._update_reference()

    def _update_reference(self):
        self._reference = Position(
            x=statistics.mean([point.x for point in self._points]),
            y=statistics.mean([point.y for point in self._points]),
            z=statistics.mean([point.z for point in self._points])
        )

    def _on_complete(self):
        super()._on_complete()
        self.complete_broadcaster.broadcast(self)

