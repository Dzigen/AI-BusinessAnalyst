import pytest 
from typing import Dict, List, Set
import sys
sys.path.insert(0, "../")

from src.reasoner.utils import UserResponse, BAResponse
from src.reasoner.weak.states_handlers.init_communicator.utils import ICommCurrentState
from src.reasoner.weak.states_handlers.init_communicator.InitCommunicator import InitCommunicator
from src.reasoner.weak.utils import WeakReasonerStatus


from cases import INITCOM_TEST_CASES

@pytest.mark.parametrize("steps, user_responses, expected_baresponses, expected_status, expected_modulestate", INITCOM_TEST_CASES)
def test_initcommun(steps: int , user_responses: List[UserResponse], expected_baresponses: List[BAResponse], 
                    expected_status: List[WeakReasonerStatus], expected_modulestate: List[ICommCurrentState]) -> None:
    
    ic_module = InitCommunicator()

    current_status = expected_status[0]
    for i in range(steps):
        if current_status == WeakReasonerStatus.waiting_interaction:
            real_baresponse, new_status, done_state = ic_module.prepare_response()

            assert real_baresponse.ba_text == expected_baresponses[i].ba_text
            assert real_baresponse.available_global_signals == expected_baresponses[i].available_global_signals
            assert real_baresponse.available_state_signals == expected_baresponses[i].available_state_signals
            assert real_baresponse.is_userinput_locked == expected_baresponses[i].is_userinput_locked
            assert real_baresponse.user_base_answer == expected_baresponses[i].user_base_answer

            assert new_status == expected_status[i+1]
            assert done_state is None
        else:
            raise AssertionError

        assert ic_module.STATE.base_state == expected_modulestate[i+1].base_state