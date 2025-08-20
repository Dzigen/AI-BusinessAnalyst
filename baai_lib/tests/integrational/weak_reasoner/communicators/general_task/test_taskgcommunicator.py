import pytest 
from typing import Dict, List, Set
import sys
sys.path.insert(0, "../")

from src.reasoner.utils import UserResponse, BAResponse
from src.reasoner.weak.states_handlers.taskg_communicator.utils import TGClarifierCurrentState
from src.reasoner.weak.states_handlers.taskg_communicator import TaskGeneralCommunicator
from src.reasoner.weak.utils import WeakReasonerStatus
from src.specification_model.utils import RequirementsInfo
from src.specification_model.ReqSpecificationModel import ReqSpecificationModel, ReqSpecificationModelConfig

from cases import TGCOM_TEST_CASES

@pytest.mark.parametrize("steps, user_responses, expected_baresponses, expected_status, expected_modulestate", TGCOM_TEST_CASES)
def test_tgcommun(steps: int , user_responses: List[UserResponse], expected_baresponses: List[BAResponse], 
                    expected_status: List[WeakReasonerStatus], expected_modulestate: List[TGClarifierCurrentState]) -> None:
    
    tg_module = TaskGeneralCommunicator()

    current_status = expected_status[0]
    for i in range(steps):
        if current_status == WeakReasonerStatus.waiting_interaction:
            real_baresponse, new_status, done_state = tg_module.prepare_response()

            assert real_baresponse.ba_text == expected_baresponses[i].ba_text
            assert real_baresponse.available_global_signals == expected_baresponses[i].available_global_signals
            assert real_baresponse.available_state_signals == expected_baresponses[i].available_state_signals
            assert real_baresponse.is_userinput_locked == expected_baresponses[i].is_userinput_locked
            assert real_baresponse.user_base_answer == expected_baresponses[i].user_base_answer

            assert new_status == expected_status[i+1]
            assert done_state is None
        elif current_status == WeakReasonerStatus.waiting_response:
            tg_module.process_response(user_responses[i])

        else:
            raise AssertionError

        assert tg_module.STATE.base_state == expected_modulestate[i+1].base_state