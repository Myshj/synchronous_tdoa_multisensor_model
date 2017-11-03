from typing import Set

from MulticastDelegate import MulticastDelegate
from TickTimer import TickTimer
from Time import Time
from TimeRelated import TimeRelated
from .MessageTransmission import MessageTransmission
from network import Message


class Connection(TimeRelated):
    def __init__(
            self,
            time: Time,
            latency: int,
            transmissions: Set[MessageTransmission]
    ) -> None:
        super().__init__(time)
        self._latency = latency
        self._transmissions = transmissions
        self._message_transmitted_broadcaster = MulticastDelegate()
        for transmission in transmissions:
            self._wait_for_transmission_end(transmission)

    @property
    def latency(self) -> int:
        return self._latency

    @property
    def transmissions(self) -> Set[MessageTransmission]:
        return self._transmissions

    @property
    def message_transmitted_broadcaster(self) -> MulticastDelegate:
        return self._message_transmitted_broadcaster

    def transmit(self, message: Message) -> None:
        transmission = self._start_transmission(message)
        self._wait_for_transmission_end(transmission)
        self.transmissions.add(transmission)

    def _start_transmission(self, message: Message) -> MessageTransmission:
        return MessageTransmission(
            message=message,
            timer=TickTimer(
                time=self.time,
                interval=self.latency
            )
        )

    def _wait_for_transmission_end(self, transmission: MessageTransmission) -> None:
        transmission.complete_broadcaster.register(self._on_transmission_complete)

    def _on_transmission_complete(self, transmission: MessageTransmission) -> None:
        self._on_message_transmitted(transmission.message)
        self.transmissions.remove(transmission)

    def _on_message_transmitted(self, message: Message) -> None:
        self._message_transmitted_broadcaster.broadcast(message)
