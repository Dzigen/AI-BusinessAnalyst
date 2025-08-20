import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response
from src.specification_model.utils import SystemRequirement, SystemRestriction

TASK_GOAL_STUB1 = 'task goal stub'

AGENT_STUB_ANSWER1 = ["системное ограничение #1"]
SYSREQ_STUB1 = SystemRequirement(id='1', statement="Системное требование #1")
ACCEPTED_SRESTR_STUB1 = [SystemRestriction(id='2', statement='системное ограничение #2'), SystemRestriction(id='3', statement='системное ограничение #3')]
DECLINED_SRESTR_STUB1 = [SystemRestriction(id='4', statement='системное ограничение #4'), SystemRestriction(id='5', statement='системное ограничение #5')]

# agent_stubresps: List[str], task_goal: str, sys_req: SystemRequirement, 
# accepted_srestrs: List[SystemRestriction], declined_srestrs: List[SystemRestriction],
# expected_output: Union[None, str], is_error_expected: bool
SRESTRGEN_TEST_CASES = [
    # 1. пустая task_goal
    [AGENT_STUB_ANSWER1, "", SYSREQ_STUB1, ACCEPTED_SRESTR_STUB1, DECLINED_SRESTR_STUB1, None, True],
    # 2. пустой accepted_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, [], DECLINED_SRESTR_STUB1, AGENT_STUB_ANSWER1[0], False],
    # 3. пустой declined_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, ACCEPTED_SRESTR_STUB1, [], AGENT_STUB_ANSWER1[0], False],
    # 4. пустой accepted_srestrs и declined_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, [], [], AGENT_STUB_ANSWER1[0], False],
    # 5. позитивный тест
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, ACCEPTED_SRESTR_STUB1, DECLINED_SRESTR_STUB1, AGENT_STUB_ANSWER1[0], False],
]