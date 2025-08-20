import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response

TASK_GOAL1 = 'task goal stub'

AGENT_STUB_ANSWERS1 = ["- user-история #1\n- user-история #2\n- user-история #3", "True", "True", "True"]
BASE_DHISTORY1 = DialogueHistory(
    sequence=[Response(role='ba', text='base ba question #1'),
              Response(role='user', text='base user answer #1')])
DETAILED_DHISTORY1 = DialogueHistory(
    sequence=[Response(role='ba', text='detailed ba question #1'),
              Response(role='user', text='detailed user answer #1')])
USER_STORIES1 = ["user-история #1", "user-история #2", "user-история #3"]

AGENT_STUB_ANSWERS2 = ["- user-история #1\n- user-история #2", "True", "True"]
USER_STORIES2 = ["user-история #1", "user-история #2"]

AGENT_STUB_ANSWERS3 = ["- user-история #1\n- user-история #2\n- user-история #3", "True", "False", "True"]
USER_STORIES3 = ["user-история #1", "user-история #3"]

# agent_stubresps, task_goal, base_dhistory, detailed_dhistory, 
# us_limit, expected_output, is_error_expected
USEXTR_TEST_CASES = [
    # 1. пустая task_goal
    [AGENT_STUB_ANSWERS1, "", BASE_DHISTORY1, DETAILED_DHISTORY1, -1, None, True],
    # 2. пустая base_dhistory
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, DialogueHistory(), DETAILED_DHISTORY1, -1, None, True],
    # 3. пустая detailed_dhistory
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, BASE_DHISTORY1, DialogueHistory(), -1, USER_STORIES1, False],
    # 4. невалидный us_limit
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, 0, None, True],
    # 5. задано фиксированное количество user-историй
    [AGENT_STUB_ANSWERS2, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, 2, USER_STORIES2, False],
    # 6. в числе полученных user-историй присутствуют нерелевантные
    [AGENT_STUB_ANSWERS3, TASK_GOAL1, BASE_DHISTORY1, DETAILED_DHISTORY1, -1, USER_STORIES3, False]
]

# agent_stubresps: List[str], task_goal: str, user_story: str, 
# expected_output: bool, is_error_expected: bool
ISUSVALID_TEST_CASES = [
    # 1. пустой task_goal
    [['True'], '', "user-история #1", None, True],
    # 2. пустой user_story
    [['True'], TASK_GOAL1, "", None, True],
    # 3. Возвращается False
    [['False'], TASK_GOAL1, "user-история #1", False, False],
    # 4. Возвращается True
    [['True'], TASK_GOAL1, "user-история #1", True, False]
]