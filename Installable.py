from typing import Optional

from Software import Software
from Time import Time
from computer.Computer import Computer


class Installable(Software):

    def __init__(self, time: Time) -> None:
        super().__init__(time)
        self._computer = None

    def install(self, computer: Computer):
        computer.software.add(self)
        self._computer = computer

    @property
    def computer(self) -> Optional[Computer]:
        return self._computer
