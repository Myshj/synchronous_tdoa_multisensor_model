from enum import Enum


class MessageStatus(Enum):
    received = 1
    to_transmit = 2
    transmitting = 3
    transmitted = 4
