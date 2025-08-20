from dataclasses import dataclass
from enum import Enum

class FRestrClarifierState(Enum):
    init: int = 0

    select_act: int = 1
    
    add: int = 2
    delete: int = 3
    edit: int = 4
    recommend: int = 5 

    done: int = 6

class FRestrAddState(Enum):
    init: int = 0
    freq_selecting: int = 1
    freqid_validating: int = 2
    adding_frestr: int = 3
    validating: int = 4
    done: int = 5

class FRestrEditState(Enum):
    init: int = 0
    frestr_selecting: int = 1
    frestrid_validating: int = 2
    editing_frestr: int = 3
    validating: int = 4
    done: int = 5

class FRestrDeleteState(Enum):
    init: int = 0
    frestr_selecting: int = 1
    frestrid_validating: int = 2
    done: int = 3

class FRestrRecommendState(Enum):
    init: int = 0
    limit_exceeds: int = 1
    freq_selecting: int = 2
    freqid_validating: int = 3
    frestr_recommending: int = 4
    done: int = 5

@dataclass
class FRestrClarifierCurrentState:
    base_state: FRestrClarifierState =  FRestrClarifierState.init
    fadd_state: FRestrAddState = FRestrAddState.init
    fedit_state: FRestrEditState = FRestrEditState.init
    frdelete_state: FRestrDeleteState = FRestrDeleteState.init
    frrecomm_state: FRestrRecommendState = FRestrRecommendState.init