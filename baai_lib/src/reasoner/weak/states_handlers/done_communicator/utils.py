from enum import Enum
from dataclasses import dataclass

class DCommState(Enum):
    notice: int = 0
    done: int = 1

@dataclass
class DCommCurrentState:
    base_state: DCommState = DCommState.notice
