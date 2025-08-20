from dataclasses import dataclass
from enum import Enum


class ICommState(Enum):
    init: int = 0
    done: int = 1

@dataclass
class ICommCurrentState:
    base_state: ICommState = ICommState.init