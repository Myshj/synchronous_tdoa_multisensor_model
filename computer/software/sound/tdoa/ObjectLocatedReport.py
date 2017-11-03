from Position import Position
from network import Address, MessageWithTimestamp


class ObjectLocatedReport(MessageWithTimestamp):
    def __init__(
            self,
            address_from: Address,
            address_to: Address,
            tick: int,
            position: Position
    ):
        super().__init__(address_from, address_to, tick)
        self._position = position

    @property
    def position(self) -> Position:
        return self._position
