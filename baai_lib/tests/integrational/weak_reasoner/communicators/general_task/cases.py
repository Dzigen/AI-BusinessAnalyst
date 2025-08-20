import sys
sys.path.insert(0, "../")

from src.reasoner.utils import UserResponse, BAResponse
from src.reasoner.weak.states_handlers.taskg_communicator.utils import TGClarifierCurrentState, TaskGeneralCommunicatorState, \
    TGCAskingState, TGCTaskClassifyingState, TGCInfoExtractingState
from src.reasoner.weak.states_handlers.taskg_communicator.config import BATC_RESPONSE_CONFIG
from src.reasoner.weak.utils import WeakReasonerStatus

TG_URESP_CASE1 = []
TG_BAREST_CASE1 = []
TG_STATUS_CASE1 = []
TG_MSTATE_CASE1 = []

TG_URESP_CASE2 = []
TG_BAREST_CASE2 = []
TG_STATUS_CASE2 = []
TG_MSTATE_CASE2 = []

TG_URESP_CASE3 = []
TG_BAREST_CASE3 = []
TG_STATUS_CASE3 = []
TG_MSTATE_CASE3 = []

# user_responses: List[UserResponse], expected_baresponses: List[BAResponse], expected_status: List[WeakReasonerStatus], expected_modulestate: List[ICommCurrentState]
TGCOM_TEST_CASES = [
    # 1. задаются все вопросы
    [TG_URESP_CASE1, TG_BAREST_CASE1, TG_STATUS_CASE1, TG_MSTATE_CASE1],
    # 2. задаётся минимальное количество вопросов и скип
    [TG_URESP_CASE2, TG_BAREST_CASE2, TG_STATUS_CASE2, TG_MSTATE_CASE2],
    # 3.задаётся задаётся среднее (больше минимального) количество вопросов и скип
    [TG_URESP_CASE3, TG_BAREST_CASE3, TG_STATUS_CASE3, TG_MSTATE_CASE3]
]