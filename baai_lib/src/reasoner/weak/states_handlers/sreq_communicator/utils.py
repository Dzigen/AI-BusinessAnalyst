from enum import Enum
from dataclasses import dataclass

class SReqExtractingState(Enum):
    init: int = 0
    done: int = 1

class SReqAddState(Enum):
    init: int = 0
    adding_sreq: int = 1
    validating: int = 2
    done: int = 3

class SReqEditState(Enum):
    init: int = 0
    sreq_selecting: int = 1
    sreqid_validating: int = 2
    editing_sreq: int = 3
    validating: int = 4
    done: int = 5

class SReqDeleteState(Enum):
    init: int = 0
    sreq_selecting: int = 1
    sreqid_validating: int = 2
    done: int = 3

class SReqClarifierState(Enum):
    init: int = 0
    sreq_extracting: int = 1
    select_act: int = 2
    
    add: int = 3
    delete: int = 4
    edit: int = 5

    done: int = 6

@dataclass
class SReqClarifierCurrentState:
    base_state: SReqClarifierState = SReqClarifierState.init

    srextr_state: SReqExtractingState = SReqExtractingState.init
    
    sradd_state: SReqAddState = SReqAddState.init
    srdelete_state: SReqDeleteState = SReqDeleteState.init
    sredit_state: SReqEditState = SReqEditState.init