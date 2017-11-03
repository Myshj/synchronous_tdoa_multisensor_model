from network import Message, Address


class MessageWithTimestamp(Message):
    def __init__(
            self,
            address_from: Address,
            address_to: Address,
            tick: int
    ):
        super().__init__(address_from, address_to)
        self._tick = tick

    @property
    def tick(self) -> int:
        return self._tick