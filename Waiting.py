from MulticastDelegate import MulticastDelegate
from TickTimer import TickTimer


class Waiting:
    def __init__(
            self,
            timer: TickTimer
    ) -> None:
        super().__init__()
        self._timer = timer
        timer.time_elapsed_broadcaster.register(self._on_complete)
        self._complete_broadcaster = MulticastDelegate()

    @property
    def timer(self) -> TickTimer:
        return self._timer

    @property
    def complete_broadcaster(self) -> MulticastDelegate:
        return self._complete_broadcaster

    def _on_complete(self):
        pass
