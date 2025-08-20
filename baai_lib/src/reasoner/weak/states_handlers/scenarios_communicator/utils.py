from enum import Enum
from dataclasses import dataclass

class SClarifierState(Enum):
    init: int = 0
    
    select_act: int = 1
    delete: int = 2
    recommend: int = 3 

    done: int = 4

class SDeleteState(Enum):
    init: int = 0
    s_selecting: int = 1
    sid_validating: int = 2
    done: int = 3

class SRecommendState(Enum):
    init: int = 0
    limit_exceeds: int = 1
    us_selecting: int = 2
    usid_validating: int = 3
    s_recommending: int = 4
    done: int = 6

@dataclass
class SClarifierCurrentState:
    base_state: SClarifierState =  SClarifierState.init
    sdelete_state: SDeleteState = SDeleteState.init
    srecomm_state: SRecommendState = SRecommendState.init