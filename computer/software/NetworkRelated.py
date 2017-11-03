from Installable import Installable
from Time import Time
from computer import Computer
from network import Address
from network.software import Protocol
from network import Message as NetworkMessage


class NetworkRelated(Installable):
    def __init__(self, time: Time, address: Address) -> None:
        super().__init__(time)
        self._address = address
        self._protocol = None

    @property
    def address(self) -> Address:
        return self._address

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    def install(self, computer: Computer):
        super().install(computer)
        self._connect_to_network_protocol()

    def is_for_me(self, message: NetworkMessage):
        return message.address_to == self.address

    def _connect_to_network_protocol(self):
        for software in self.computer.software:
            if isinstance(software, Protocol):
                if software.host == self.address.host:
                    self._protocol = software
                    software.port_broadcaster(self.address.port).register(self._on_network_message)
                    return
        raise ValueError('network protocol not available')

    def _on_network_message(self, message: NetworkMessage):
        pass
