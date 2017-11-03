from typing import Set

from Hardware import Hardware
from Software import Software


class Computer:
    def __init__(
            self,
            hardware: Set[Hardware],
            software: Set[Software]
    ) -> None:
        super().__init__()
        self._hardware = hardware
        self._software = software

    @property
    def hardware(self) -> Set[Hardware]:
        return self._hardware

    @property
    def software(self) -> Set[Software]:
        return self._software
