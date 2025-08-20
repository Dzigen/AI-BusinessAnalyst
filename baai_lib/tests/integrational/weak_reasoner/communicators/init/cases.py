import sys
sys.path.insert(0, "../")

from src.reasoner.utils import UserResponse, BAResponse
from src.reasoner.weak.states_handlers.init_communicator.utils import ICommCurrentState, ICommState
from src.reasoner.weak.states_handlers.init_communicator.config import BAIC_RESPONSE_CONFIG
from src.reasoner.weak.utils import WeakReasonerStatus

IC_URESP_CASE1 = [None, None]
IC_BAREST_CASE1 = [BAIC_RESPONSE_CONFIG[ICommState.init].ba_response, BAIC_RESPONSE_CONFIG[ICommState.done].ba_response]
IC_STATUS_CASE1 = [WeakReasonerStatus.waiting_interaction, BAIC_RESPONSE_CONFIG[ICommState.init].reasoner_newstatus, BAIC_RESPONSE_CONFIG[ICommState.done].reasoner_newstatus]
IC_MSTATE_CASE1 = [ICommCurrentState(), BAIC_RESPONSE_CONFIG[ICommState.init].stage_newstate, BAIC_RESPONSE_CONFIG[ICommState.done].stage_newstate]

# user_responses: List[UserResponse], expected_baresponses: List[BAResponse], expected_status: List[WeakReasonerStatus], expected_modulestate: List[ICommCurrentState]
INITCOM_TEST_CASES = [
    # позитивный тест
    [2, IC_URESP_CASE1, IC_BAREST_CASE1, IC_STATUS_CASE1, IC_MSTATE_CASE1]
]