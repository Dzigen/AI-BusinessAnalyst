from enum import Enum

from dataclasses import dataclass
from enum import Enum

class SRestrClarifierState(Enum):
    init: int = 0

    select_act: int = 1
    
    add: int = 2
    delete: int = 3
    edit: int = 4
    recommend: int = 5 

    done: int = 6

class SRestrAddState(Enum):
    init: int = 0
    sreq_selecting: int = 1
    sreqid_validating: int = 2
    adding_srestr: int = 3
    validating: int = 4
    done: int = 5

class SRestrEditState(Enum):
    init: int = 0
    srestr_selecting: int = 1
    srestrid_validating: int = 2
    editing_srestr: int = 3
    validating: int = 4
    done: int = 5

class SRestrDeleteState(Enum):
    init: int = 0
    srestr_selecting: int = 1
    srestrid_validating: int = 2
    done: int = 3

class SRestrRecommendState(Enum):
    init: int = 0
    limit_exceeds: int = 1
    sreq_selecting: int = 2
    sreqid_validating: int = 3
    srestr_recommending: int = 4
    done: int = 5

@dataclass
class SRestrClarifierCurrentState:
    base_state: SRestrClarifierState =  SRestrClarifierState.init
    sadd_state: SRestrAddState = SRestrAddState.init
    sedit_state: SRestrEditState = SRestrEditState.init
    srdelete_state: SRestrDeleteState = SRestrDeleteState.init
    srrecomm_state: SRestrRecommendState = SRestrRecommendState.init