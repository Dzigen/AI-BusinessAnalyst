import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response
from src.specification_model.utils import FunctionalRestriction, FunctionalRequirement

TASK_GOAL_STUB1 = 'task goal stub'

AGENT_STUB_ANSWER1 = ["функциональное ограничение #1"]
SYSREQ_STUB1 = FunctionalRequirement(id='1', statement="функциональное требование #1")
ACCEPTED_FRESTR_STUB1 = [FunctionalRestriction(id='2', statement='функциональное ограничение #2'), FunctionalRestriction(id='3', statement='функциональное ограничение #3')]
DECLINED_FRESTR_STUB1 = [FunctionalRestriction(id='4', statement='функциональное ограничение #4'), FunctionalRestriction(id='5', statement='функциональное ограничение #5')]

#agent_stubresps: List[str], task_goal: str, func_req: FunctionalRequirement, 
# accepted_frestrs: List[FunctionalRestriction], declined_frestrs: List[FunctionalRestriction],
# expected_output: Union[None, str], is_error_expected: bool
FRESTRGEN_TEST_CASES = [
    # 1. пустая task_goal
    [AGENT_STUB_ANSWER1, "", SYSREQ_STUB1, ACCEPTED_FRESTR_STUB1, DECLINED_FRESTR_STUB1, None, True],
    # 2. пустой accepted_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, [], DECLINED_FRESTR_STUB1, AGENT_STUB_ANSWER1[0], False],
    # 3. пустой declined_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, ACCEPTED_FRESTR_STUB1, [], AGENT_STUB_ANSWER1[0], False],
    # 3. пустые accepted_srestrs и declined_srestrs
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, [], [], AGENT_STUB_ANSWER1[0], False],
    # 4. позитивный тест
    [AGENT_STUB_ANSWER1, TASK_GOAL_STUB1, SYSREQ_STUB1, ACCEPTED_FRESTR_STUB1, DECLINED_FRESTR_STUB1, AGENT_STUB_ANSWER1[0], False]
]