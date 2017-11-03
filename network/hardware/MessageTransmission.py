from MulticastDelegate import MulticastDelegate
from TickTimer import TickTimer
from Waiting import Waiting
from network import Message


class MessageTransmission(Waiting):
    def __init__(
            self,
            message: Message,
            timer: TickTimer
    ) -> None:
        super().__init__(timer)
        self._message = message

    @property
    def message(self) -> Message:
        return self._message

    @property
    def timer(self) -> TickTimer:
        return self._timer

    def _on_complete(self):
        self._complete_transmission()

    def _complete_transmission(self):
        self.complete_broadcaster.broadcast(self)
