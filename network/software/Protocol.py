from typing import Dict, Set

from Installable import Installable
from MulticastDelegate import MulticastDelegate
from Time import Time
from computer.Computer import Computer
from network.Message import Message
from network.hardware import Adapter


class Protocol(Installable):
    def __init__(
            self,
            time: Time,
            route_table: Dict[str, 'Adapter'],
            host: str
    ) -> None:
        super().__init__(time)
        self._adapters = set()
        self._route_table = route_table
        self._host = host
        self._port_broadcasters = {}

    def port_broadcaster(self, port: int) -> MulticastDelegate:
        if port not in self._port_broadcasters.keys():
            self._port_broadcasters[port] = MulticastDelegate()
        return self._port_broadcasters[port]

    @property
    def adapters(self) -> Set['Adapter']:
        return self._adapters

    @property
    def route_table(self) -> Dict[str, 'Adapter']:
        return self._route_table

    @property
    def host(self) -> str:
        return self._host

    def install(self, computer: Computer):
        super().install(computer)
        self._adapters = {
            hardware for hardware in filter(lambda hardware: isinstance(hardware, Adapter), computer.hardware)
        }
        # map(self._listen_to, self.adapters)
        for adapter in self.adapters:
            self._listen_to(adapter)

    def _listen_to(self, adapter: Adapter):
        adapter.message_received_broadcaster.register(self._on_adapter_received_message)

    def _on_adapter_received_message(self, message: Message):
        if self.is_target_of(message):
            self.port_broadcaster(message.address_to.port).broadcast(message)
        else:
            self.send(message)

    def is_target_of(self, message: Message):
        return self.host == message.address_to.host

    def send(self, message: Message):
        target_host = message.address_to.host
        if not self.has_connection_to(target_host):
            raise ValueError('no connection to target')
        target_adapter = self.route_table[target_host]
        for adapter in self.adapters:
            if adapter.has_connection_to(target_adapter):
                adapter.transmit(message, target_adapter)
                return
        raise ValueError('adapters have no connections to target')

    def has_connection_to(self, host: str):
        return host in self.route_table.keys()
