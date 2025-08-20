from enum import Enum
from dataclasses import dataclass

class RExtractorState(Enum):
    init: int = 0
    extracting_result: int = 1
    done: int = 2

@dataclass
class RExtractorCurrentState:
    base_state: RExtractorState = RExtractorState.init