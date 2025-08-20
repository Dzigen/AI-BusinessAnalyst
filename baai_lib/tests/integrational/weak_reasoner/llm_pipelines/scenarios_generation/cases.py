import sys
sys.path.insert(0, "../")

from src.specification_model.utils import UserStory, Scenario

TASK_GOAL_STUB = 'task goal stub'
AGENT_STUB_RESPONSE1 = ["Название сценария использования #1", "1. шаг сценария #1.1\n2. шаг сценария #1.2\n3. шаг сценария #1.3"]
USER_STORY1 = UserStory(id='1', statement="Пользовательская история #1")
ACCEPTED_SCEN1 = [Scenario(id='2', title="Название сценария использования #2", steps=["шаг сценария #2.1", "шаг сценария #2.2"])]
DECLINED_SCEN1 = [Scenario(id='3', title="Название сценария использования #3", steps=["шаг сценария #3.1", "шаг сценария #3.2", "шаг сценария #3.3"]),
                  Scenario(id='4', title="Название сценария использования #4", steps=["шаг сценария #4.1", "шаг сценария #4.2"])]
NEW_SCENARIO1 = Scenario(id='1', title="Название сценария использования #1", steps=["шаг сценария #1.1", "шаг сценария #1.2", "шаг сценария #1.3"],
                         related_userstory_ids=[USER_STORY1.id])

# agent_stubresps: List[str], task_goal: str, user_story: UserStory, 
# accepted_scenarios: List[Scenario], declined_scenarios: List[Scenario],
# expected_output: Union[None, Scenario], is_error_expected: bool
SCENGEN_TEST_CASES = [
    # 1. пустая task_goal
    [AGENT_STUB_RESPONSE1, "", USER_STORY1, ACCEPTED_SCEN1, DECLINED_SCEN1, None, True],
    # 2. пустой accepted_scenarios
    [AGENT_STUB_RESPONSE1, TASK_GOAL_STUB, USER_STORY1, [], DECLINED_SCEN1, NEW_SCENARIO1, False],
    # 3. пустой declined_scenarios
    [AGENT_STUB_RESPONSE1, TASK_GOAL_STUB, USER_STORY1, ACCEPTED_SCEN1, [], NEW_SCENARIO1, False],
    # 4. пустой accepted_scenarios и declined_scenarios
    [AGENT_STUB_RESPONSE1, TASK_GOAL_STUB, USER_STORY1, [], [], NEW_SCENARIO1, False],
    # 5. позитивный тест
    [AGENT_STUB_RESPONSE1, TASK_GOAL_STUB, USER_STORY1, ACCEPTED_SCEN1,  DECLINED_SCEN1, NEW_SCENARIO1, False]
]