import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response

DIALOGUE_HISTORY1= DialogueHistory(
    sequence=[
        Response(role='ba', text='ba question #1'),
        Response(role='user', text='user answer #1')])

TASK_GOAL_STUB1 = 'task goal stub'
SUB_TASKS_STUB1 = 'sub tasks stub'
INTGR_INFO_STUB1 = 'integration info stub'

# agent stub-answers, dhistory, expected_output, is_error_expected
TASKCLS_TEST_CASES = [
# 0. Пустая история диалога
[['False'], DialogueHistory(), None, True],
# 1. False return
[['False'], DIALOGUE_HISTORY1, False, False],
# 2. True return
[['True'], DIALOGUE_HISTORY1, True, False]
]

# agent stub-answers, dhistory, expected_output, is_error_expected
GIE_EXTRACT_TEST_CASES = [
# 0. Пустая история диалога
[[TASK_GOAL_STUB1, SUB_TASKS_STUB1, INTGR_INFO_STUB1], DialogueHistory(), None, True],
# 1. Позитивный тест
[[TASK_GOAL_STUB1, SUB_TASKS_STUB1, INTGR_INFO_STUB1], DIALOGUE_HISTORY1, 
 (TASK_GOAL_STUB1, SUB_TASKS_STUB1, INTGR_INFO_STUB1), False]
]

# agent stub-answers, dhistory, task_goal, expected_output, is_error_expected
GIE_SUMMIN_TEST_CASES = [
# 0. Пустая история диалога
[[INTGR_INFO_STUB1],  DialogueHistory(), TASK_GOAL_STUB1, None, True],
# 1. Пустая task goal
[[INTGR_INFO_STUB1],  DIALOGUE_HISTORY1, "", None, True],
# 2. позитивный тест
[[INTGR_INFO_STUB1],  DIALOGUE_HISTORY1, TASK_GOAL_STUB1, INTGR_INFO_STUB1, False]
]

# agent stub-answers, dhistory, task_goal, expected_output, is_error_expected
GIE_SUMMST_TEST_CASES = [
# 0. Пустая история диалога
[[SUB_TASKS_STUB1],  DialogueHistory(), TASK_GOAL_STUB1, None, True],
# 1. Пустая task goal
[[SUB_TASKS_STUB1],  DIALOGUE_HISTORY1, "", None, True],
# 2. позитивный тест
[[SUB_TASKS_STUB1],  DIALOGUE_HISTORY1, TASK_GOAL_STUB1, SUB_TASKS_STUB1, False]
]

# agent stub-answers, dhistory, expected_output, is_error_expected
GIE_SUMMTG_TEST_CASES = [
# 0. Пустая история диалога
[[TASK_GOAL_STUB1],  DialogueHistory(), None, True],
# 1. позитивный тест
[[TASK_GOAL_STUB1],  DIALOGUE_HISTORY1, TASK_GOAL_STUB1, False]
]
