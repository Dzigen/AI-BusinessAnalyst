import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response

TASK_GOAL1 = 'task goal stub'

AGENT_STUB_ANSWERS1 = ["- сис. требование #1\n- сис. требование #2\n- сис. требование #3\n"]
BASE_DHISTORY1 = DialogueHistory(sequence=[
    Response(role='ba', text="base ba question #1"),
    Response(role='user', text="base user answer #1")])
DETAILED_DHISTORY1 = DialogueHistory(sequence=[
    Response(role='ba', text="detailed ba question #1"),
    Response(role='user', text="detailed user answer #1")])
EXPECTED_OUTPUT1 = ['сис. требование #1', 'сис. требование #2', 'сис. требование #3']


# agent_stubresps: List[str], task_goal: str, base_dhistory: DialogueHistory, 
# detailed_dhistory: DialogueHistory, sr_limit: int, 
# expected_output: Union[None, List[SystemRequirement]], is_error_expected: bool
SREQEXTR_TEST_CASES = [
    # 1. пустая task_goal
    [AGENT_STUB_ANSWERS1, "", BASE_DHISTORY1, DETAILED_DHISTORY1, -1, None, True],
    # 2. пустая base_dhistory
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, DialogueHistory(), DETAILED_DHISTORY1, -1, None, True],
    # 3. пустая detailed_dhistory
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, -1, EXPECTED_OUTPUT1, False],
    # 4. невалидная sr_limit
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, 0, None, True],
    # 5. задано фиксированное количество системных требований
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, 2, EXPECTED_OUTPUT1[:2], False],
]