"""
В этом модуле описывается класс NetworkAdapter.
"""
from typing import Dict

from Hardware import Hardware
from MulticastDelegate import MulticastDelegate
from Position import Position
from Time import Time
from .Connection import Connection
from .MessageStatus import MessageStatus
from network import Message


class Adapter(Hardware):
    """
    Сетевой адаптер.
    """

    def __init__(
            self,
            time: Time,
            position: Position,
            connections: Dict['Adapter', Connection],
            message_statuses: Dict[Message, MessageStatus],
            messages_to_transmit: Dict[Message, 'Adapter']
    ):
        super(Adapter, self).__init__(time, position)
        self._connections = connections
        for connection in connections.values():
            self._listen_to(connection)
        self._message_statuses = message_statuses
        self._messages_to_transmit = messages_to_transmit
        self._message_received_broadcaster = MulticastDelegate()

    @property
    def connections(self) -> Dict['Adapter', Connection]:
        return self._connections

    @property
    def message_statuses(self) -> Dict[Message, MessageStatus]:
        return self._message_statuses

    @property
    def messages_to_transmit(self) -> Dict[Message, 'Adapter']:
        return self._messages_to_transmit

    @property
    def message_received_broadcaster(self) -> MulticastDelegate:
        return self._message_received_broadcaster

    def connect(self, target: 'Adapter', connection: Connection):
        self.connections[target] = connection
        self._listen_to(connection)

    def transmit(self, message: Message, target: 'Adapter'):
        if target is self:
            self._notify_about_received_message(message)
            return
        if not self.has_connection_to(target):
            raise ValueError('no connection to target')
        self.messages_to_transmit[message] = target
        self.message_statuses[message] = MessageStatus.to_transmit

    def has_connection_to(self, target: 'Adapter'):
        return target in self.connections.keys() or target is self

    def knows_about_message(self, message: Message):
        return message in self.message_statuses.keys()

    def _listen_to(self, connection: Connection):
        connection.message_transmitted_broadcaster.register(self._on_connection_transmitted_message)

    def _on_connection_transmitted_message(self, message: Message):
        if not self.knows_about_message(message):
            self._on_message_received(message)
        elif self.message_statuses[message] == MessageStatus.transmitting:
            self._on_message_transmitted(message)
        else:
            raise ValueError('connection transmitted message that I did not send')

    def _on_message_received(self, message: Message):
        self.message_statuses[message] = MessageStatus.received

    def _on_message_transmitted(self, message: Message):
        self.message_statuses[message] = MessageStatus.transmitted

    def on_tick(self) -> None:
        super().on_tick()
        for message, status in self.message_statuses.copy().items():
            if status == MessageStatus.to_transmit:
                self.connections[self.messages_to_transmit[message]].transmit(message)
                self.message_statuses[message] = MessageStatus.transmitting
            elif status == MessageStatus.transmitted:
                self.messages_to_transmit.pop(message)
                self.message_statuses.pop(message)
            elif status == MessageStatus.received:
                self._notify_about_received_message(message)
                self.message_statuses.pop(message)

    def _notify_about_received_message(self, message: Message):
        self.message_received_broadcaster.broadcast(message)
