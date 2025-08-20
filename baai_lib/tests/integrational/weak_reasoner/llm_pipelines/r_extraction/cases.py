import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response
from src.specification_model.utils import UserStory

TASK_GOAL1 = 'task goal stub'

AGENT_STUB_ANSWERS1 = ["True", "- роль#1", 'True', "- роль#2\n- роль#3"]
USER_STORIES1 = [UserStory(id='1', statement="user-история #1"), UserStory(id='2', statement="user-история #2")]
ROLES1 = ["роль#1", "роль#2", "роль#3"]

AGENT_STUB_ANSWERS2 = ["False", "False"]
USER_STORIES2 = [UserStory(id='1', statement="user-история #3"), UserStory(id='2', statement="user-история #4")]
ROLES2 = []

AGENT_STUB_ANSWERS3 = ["True", "- роль#3\n- роль#4", 'True', "- роль#4\n- роль#5"]
USER_STORIES3 = [UserStory(id='1', statement="user-история #5"), UserStory(id='2', statement="user-история #6")]
ROLES3 = ["роль#3", "роль#4", "роль#5"]

# agent_stubresps, task_goal, user_stories, expected_output, is_error_expected
REXTR_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS1, "", USER_STORIES1, None, True],
    # 2. user_stories отсутствуют
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, [], None, True],
    # 3. из всех user-историй было извлечено мин 1 роль
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, USER_STORIES1, ROLES1, False],
    # 4. было извлечено нуль ролей
    [AGENT_STUB_ANSWERS2, TASK_GOAL1, USER_STORIES2, ROLES2, False],
    # 5. присутствуют user-истории, в которых содержаться пересекающиеся роли
    [AGENT_STUB_ANSWERS3, TASK_GOAL1, USER_STORIES3, ROLES3, False]
]