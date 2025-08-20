from enum import Enum
from dataclasses import dataclass

class FRExtractorState(Enum):
    init: int = 0
    extract_results: int = 1
    done: int = 2
    
@dataclass
class FRExtractorCurrentState:
    base_state: FRExtractorState = FRExtractorState.init

