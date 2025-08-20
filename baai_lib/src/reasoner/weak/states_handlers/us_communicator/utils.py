from dataclasses import dataclass
from enum import Enum

class USExtractingState(Enum):
    init: int = 0
    done: int = 1

class USAddState(Enum):
    init: int = 0
    adding_us: int = 1
    validating: int = 2
    done: int = 3

class USEditState(Enum):
    init: int = 0
    us_selecting: int = 1
    usid_validating: int = 2
    editing_us: int = 3
    validating: int = 4
    done: int = 5

class USDeleteState(Enum):
    init: int = 0
    us_selecting: int = 1
    usid_validating: int = 2
    done: int = 3

class USClarifierState(Enum):
    init: int = 0
    us_extracting: int = 1
    select_act: int = 2
    
    add: int = 3
    delete: int = 4
    edit: int = 5

    done: int = 6

@dataclass
class USClarifierCurrentState:
    base_state: USClarifierState = USClarifierState.init
    usextr_state: USExtractingState = USExtractingState.init
    usadd_state: USAddState = USAddState.init
    usdelete_state: USDeleteState = USDeleteState.init
    usedit_state: USEditState = USEditState.init