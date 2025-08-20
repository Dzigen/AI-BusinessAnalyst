from enum import Enum
from dataclasses import dataclass

class BPClarifierState(Enum):
    init: int = 0
    clarify: int = 1
    done: int = 2

class BPCAskingState(Enum):
    init: int = 0
    question_preparing: int = 1
    limit_exceeded: int = 2

@dataclass
class BPClarifierCurrentState:
    base_state: BPClarifierState = BPClarifierState.init
    askq_state: BPCAskingState = BPCAskingState.init
