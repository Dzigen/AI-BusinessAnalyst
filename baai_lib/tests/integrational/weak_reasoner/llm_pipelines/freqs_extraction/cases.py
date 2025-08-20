import pytest 
from typing import List, Union, Dict
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import UserStory, Scenario, \
    FunctionalRequirement, FunctionalRequirementGroup
from src.utils.data_structs import create_id

TASK_GOAL1 = 'task goal stub'

AGENT_STUB_ANSWERS1 = ["- сырое функ. требование #1\n- сырое функ. требование #2\n- сырое функ. требование #3",
                       "- сырое функ. требование #4\n- сырое функ. требование #5\n- сырое функ. требование #6",
                       "- сырое функ. требование #7\n- сырое функ. требование #8"]
USER_STORIES1 = [UserStory(id='1', statement="user-история #1"), UserStory(id='2', statement="user-история #2")]
ACCEPTED_SCENARIOS1 = {"1": [Scenario(id="1", title="название сценария #1", steps=["шаг #1.1", "шаг #1.2", "шаг #1.3", "шаг #1.4"])],
                       "2": [Scenario(id="2", title="название сценария #2", steps=["шаг #2.1", "шаг #2.2", "шаг #2.3", "шаг #2.4"]),
                             Scenario(id="3", title="название сценария #3", steps=["шаг #3.1", "шаг #3.2"]),]}
EXPECTED_BASE_FREQS1 = {"1": ["сырое функ. требование #1", "сырое функ. требование #2", "сырое функ. требование #3"],
                        "2": ["сырое функ. требование #4", "сырое функ. требование #5", "сырое функ. требование #6", "сырое функ. требование #7", "сырое функ. требование #8"]}


AGENT_STUB_ANSWERS2 = ["- сырое функ. требование #4\n- сырое функ. требование #5\n- сырое функ. требование #6",
                       "- сырое функ. требование #7\n- сырое функ. требование #8"]
ACCEPTED_SCENARIOS2 = {"1": [],
                       "2": [Scenario(id="2", title="название сценария #2", steps=["шаг #2.1", "шаг #2.2", "шаг #2.3", "шаг #2.4"]),
                             Scenario(id="3", title="название сценария #3", steps=["шаг #3.1", "шаг #3.2"]),]}
EXPECTED_BASE_FREQS2 = {"2": ["сырое функ. требование #4", "сырое функ. требование #5", "сырое функ. требование #6", "сырое функ. требование #7", "сырое функ. требование #8"]}


# agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory],
# accepted_scenarios: Dict[int, List[Scenario]], 
# expected_output: Union[None,Dict[str,List[str]]], is_error_expected: bool
EXTRACT_BASE_FREQS_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS1, "", USER_STORIES1, ACCEPTED_SCENARIOS1, None, True],
    # 2. нуль user_stories
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, [], ACCEPTED_SCENARIOS1, None, True],
    # 3. нуль сценариев
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, USER_STORIES1, {USER_STORIES1[0].id: [], USER_STORIES1[1].id: []}, dict(), False],
    # 4. присутствуют user-истории, у которых нуль сценариев
    [AGENT_STUB_ANSWERS2, TASK_GOAL1, USER_STORIES1, ACCEPTED_SCENARIOS2, EXPECTED_BASE_FREQS2, False],
    # 5. позитивный тест
    [AGENT_STUB_ANSWERS1, TASK_GOAL1, USER_STORIES1, ACCEPTED_SCENARIOS1, EXPECTED_BASE_FREQS1, False]
]

AGENT_STUB_ANSWERS3 = ["- base gname #1\n- base gname #2\n- base gname #3\n- base gname #4\n"]
US_TO_BASEFREQS_MAP1= {"1": [],
                        "2": ["сырое функ. требование #4", "сырое функ. требование #5", "сырое функ. требование #6", "сырое функ. требование #7", "сырое функ. требование #8"]}
EXPECTED_BG_NAMES1 = ["base gname #1", "base gname #2", "base gname #3", "base gname #4"]

AGENT_STUB_ANSWERS4 = ["- base gname #1\n- base gname #2\n- base gname #3\n- base gname #4\n", "- base gname #5\n- base gname #6\n- base gname #7"]
US_TO_BASEFREQS_MAP2= {"1": ["сырое функ. требование #1", "сырое функ. требование #2", "сырое функ. требование #3"],
                        "2": ["сырое функ. требование #4", "сырое функ. требование #5", "сырое функ. требование #6", "сырое функ. требование #7", "сырое функ. требование #8"]}
EXPECTED_BG_NAMES2 = ["base gname #1", "base gname #2", "base gname #3", "base gname #4", "base gname #5","base gname #6","base gname #7"]

# agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
# us_to_basefreqs_map: Dict[str,List[str]], expected_output: Union[None,List[str]], 
# is_error_expected: bool
EXTRACT_BASE_GFREQ_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS3, "", USER_STORIES1, US_TO_BASEFREQS_MAP1, None, True],
    # 2. нуль user_stories
    [AGENT_STUB_ANSWERS3, TASK_GOAL1, [], US_TO_BASEFREQS_MAP1, None, True],
    # 3. нуль функциональных требований
    [AGENT_STUB_ANSWERS3, TASK_GOAL1,  USER_STORIES1, {'1': [], '2': []}, [], False],
    # 4. присутствуют user-истории, у которых нуль функ. требований
    [AGENT_STUB_ANSWERS3, TASK_GOAL1,  USER_STORIES1, US_TO_BASEFREQS_MAP1, EXPECTED_BG_NAMES1, False],
    # 5. позитивный тест
    [AGENT_STUB_ANSWERS4, TASK_GOAL1,  USER_STORIES1, US_TO_BASEFREQS_MAP2, EXPECTED_BG_NAMES2, False]
    
]

AGENT_STUB_ANSWERS5 = ["- summ gname #1\n- summ gname #2"]
BASE_GFREQ_NAMES1 = ["base gname #1", "base gname #2", "base gname #3", "base gname #4"]
EXPECTED_SUMM_GFREQ_NAMES1 = ["summ gname #1", "summ gname #2"]

# agent_stubresps: List[str], task_goal: str,  base_gfreq_names: List[str], 
# expected_output: Union[None,List[str]], is_error_expected: bool
SUMM_BASE_GFREQ_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS5, "", BASE_GFREQ_NAMES1, None, True],
    # 2. нуль base_gfreq_names
    [AGENT_STUB_ANSWERS5, TASK_GOAL1, [], None, True],
    # 3. позитивный тест
    [AGENT_STUB_ANSWERS5, TASK_GOAL1, BASE_GFREQ_NAMES1, EXPECTED_SUMM_GFREQ_NAMES1, False]
]

SUMM_GFREQ_NAMES1 = ['summ gname #1', 'summ gname #2', 'summ gname #3']

AGENT_STUB_ANSWERS6 = ["False", "True", "1, 2", "True", "1", "True", "1", "True", "2, 3", "True", "1, 2"]
EXPECTED_SUMMG_TO_FREQ_MAP1 = {
    0: ["сырое функ. требование #4"],
    1: ["сырое функ. требование #1", "сырое функ. требование #2", "сырое функ. требование #6", "сырое функ. требование #7"],
    2: ["сырое функ. требование #3", "сырое функ. требование #5", "сырое функ. требование #8"]
}

AGENT_STUB_ANSWERS7 = ["True", "1, 2", "False", "True", "1, 2, 3"]
EXPECTED_SUMMG_TO_FREQ_MAP2 = {
    0: ["сырое функ. требование #4", "сырое функ. требование #5"],
    2: ["сырое функ. требование #6", "сырое функ. требование #7", "сырое функ. требование #8"]
}

# agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
# summ_gfreq_names: List[str], us_to_basefreqs_map: Dict[str,List[str]],
# expected_output: Union[None, Dict[int, List[str]]], is_error_expected: bool
GROUP_FREQS_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS6, "", USER_STORIES1, SUMM_GFREQ_NAMES1, US_TO_BASEFREQS_MAP2, None, True],
    # 2. нуль user_stories
    [AGENT_STUB_ANSWERS6, TASK_GOAL1, [], SUMM_GFREQ_NAMES1, US_TO_BASEFREQS_MAP2, None, True],
    # 3. нуль summ_gfreq_names
    [AGENT_STUB_ANSWERS6, TASK_GOAL1, USER_STORIES1, [], US_TO_BASEFREQS_MAP2, None, True],
    # 4. нуль функциональных требований
    [AGENT_STUB_ANSWERS6, TASK_GOAL1, USER_STORIES1, SUMM_GFREQ_NAMES1, {'1': [], '2': []}, dict(), False],
    # 5. присутствуют user-истории, у которых нуль функ. требований
    [AGENT_STUB_ANSWERS7, TASK_GOAL1, USER_STORIES1, SUMM_GFREQ_NAMES1, US_TO_BASEFREQS_MAP1, EXPECTED_SUMMG_TO_FREQ_MAP2, False],
    # 6. позитивный тест
    [AGENT_STUB_ANSWERS6, TASK_GOAL1, USER_STORIES1, SUMM_GFREQ_NAMES1, US_TO_BASEFREQS_MAP2, EXPECTED_SUMMG_TO_FREQ_MAP1, False]
]

AGENT_STUB_ANSWERS8 = ["- спец функ треб #1\n- спец функ треб #2\n", "- спец функ треб #3\n- спец функ треб #4\n- спец функ треб #5", "- спец функ треб #6\n- спец функ треб #7"]
SUMMG_TO_FREQ_MAP1 = {
    0: ["сырое функ. треб #1", "сырое функ. треб #2", "сырое функ. треб #3", "сырое функ. треб #4"],
    1: ["сырое функ. треб #5", "сырое функ. треб #6"],
    2: ["сырое функ. треб #7"]
}
EXPECTED_FREQ_REPHRASE1 = {
    0: [FunctionalRequirement(id="1", statement="спец функ треб #1"), FunctionalRequirement(id="2", statement="спец функ треб #2")],
    1: [FunctionalRequirement(id="3", statement="спец функ треб #3"), FunctionalRequirement(id="4", statement="спец функ треб #4"), FunctionalRequirement(id="5", statement="спец функ треб #5")],
    2: [FunctionalRequirement(id="6", statement="спец функ треб #6"), FunctionalRequirement(id="7", statement="спец функ треб #7")]
}

AGENT_STUB_ANSWERS9 = ["- спец функ треб #1\n- спец функ треб #2\n", "- спец функ треб #6\n- спец функ треб #7"]
SUMMG_TO_FREQ_MAP2 = {
    0: ["сырое функ. треб #1", "сырое функ. треб #2", "сырое функ. треб #3", "сырое функ. треб #4"],
    1: [],
    2: ["сырое функ. треб #7"]
}
EXPECTED_FREQ_REPHRASE2 = {
    0: [FunctionalRequirement(id="1", statement="спец функ треб #1"), FunctionalRequirement(id="2", statement="спец функ треб #2")],
    2: [FunctionalRequirement(id="6", statement="спец функ треб #6"), FunctionalRequirement(id="7", statement="спец функ треб #7")]
}

# agent_stubresps: List[str], task_goal: str, summ_gfreq_names: List[str], 
# sumgidx_to_freqs_map: Dict[int, List[str]], 
# expected_output: Union[None, Dict[int, List[FunctionalRequirement]]], 
# is_error_expected: bool
REPHRASE_FREQ_GROUPS_TEST_CASES = [
    # 1. пустой task_goal
    [AGENT_STUB_ANSWERS8, "", SUMM_GFREQ_NAMES1, SUMMG_TO_FREQ_MAP1, None, True],
    # 2. нуль summ_gfreq_names
    [AGENT_STUB_ANSWERS8, TASK_GOAL1, [], SUMMG_TO_FREQ_MAP1, None, True],
    # 3. нуль функциональных требований
    [AGENT_STUB_ANSWERS8, TASK_GOAL1, SUMM_GFREQ_NAMES1, {0: [], 1: [], 2: []}, dict(), False],
    # 4. присутствуют группы, в которых нуль фунциональных требований
    [AGENT_STUB_ANSWERS9, TASK_GOAL1, SUMM_GFREQ_NAMES1, SUMMG_TO_FREQ_MAP2, EXPECTED_FREQ_REPHRASE2, False],
    # 5. позитивный тест
    [AGENT_STUB_ANSWERS8, TASK_GOAL1, SUMM_GFREQ_NAMES1, SUMMG_TO_FREQ_MAP1, EXPECTED_FREQ_REPHRASE1, False]
]

SUMMG_TO_FREQ_REPHRASED1 = {
    0: [FunctionalRequirement(id="1", statement="спец функ треб #1"), FunctionalRequirement(id="2", statement="спец функ треб #2")],
    1: [FunctionalRequirement(id="3", statement="спец функ треб #3"), FunctionalRequirement(id="4", statement="спец функ треб #4"), FunctionalRequirement(id="5", statement="спец функ треб #5")],
    2: [FunctionalRequirement(id="6", statement="спец функ треб #6"), FunctionalRequirement(id="7", statement="спец функ треб #7")]
}

EXPECTED_FORMATED_GROUPS1 = {
    create_id(SUMM_GFREQ_NAMES1[0]): FunctionalRequirementGroup(
        id=create_id(SUMM_GFREQ_NAMES1[0]), title=SUMM_GFREQ_NAMES1[0], 
        grouped_funcreq_ids=[SUMMG_TO_FREQ_REPHRASED1[0][0].id, SUMMG_TO_FREQ_REPHRASED1[0][1].id]
    ),
    create_id(SUMM_GFREQ_NAMES1[1]): FunctionalRequirementGroup(
        id=create_id(SUMM_GFREQ_NAMES1[1]), title=SUMM_GFREQ_NAMES1[1], 
        grouped_funcreq_ids=[SUMMG_TO_FREQ_REPHRASED1[1][0].id, SUMMG_TO_FREQ_REPHRASED1[1][1].id, SUMMG_TO_FREQ_REPHRASED1[1][2].id]
    ),
    create_id(SUMM_GFREQ_NAMES1[2]): FunctionalRequirementGroup(
        id=create_id(SUMM_GFREQ_NAMES1[2]), title=SUMM_GFREQ_NAMES1[2], 
        grouped_funcreq_ids=[SUMMG_TO_FREQ_REPHRASED1[2][0].id, SUMMG_TO_FREQ_REPHRASED1[2][1].id]
    )
}
EXPECTED_FORMATED_FREQS1 = {
    "1": FunctionalRequirement(id="1", statement="спец функ треб #1"),
    "2": FunctionalRequirement(id="2", statement="спец функ треб #2"),
    "3": FunctionalRequirement(id="3", statement="спец функ треб #3"),
    "4": FunctionalRequirement(id="4", statement="спец функ треб #4"),
    "5": FunctionalRequirement(id="5", statement="спец функ треб #5"),
    "6": FunctionalRequirement(id="6", statement="спец функ треб #6"),
    "7": FunctionalRequirement(id="7", statement="спец функ треб #7"),
}

SUMMG_TO_FREQ_REPHRASED2 = {
    0: [FunctionalRequirement(id="1", statement="спец функ треб #1"), FunctionalRequirement(id="2", statement="спец функ треб #2")],
    1: [],
    2: [FunctionalRequirement(id="6", statement="спец функ треб #6"), FunctionalRequirement(id="7", statement="спец функ треб #7")]
}

EXPECTED_FORMATED_GROUPS2 = {
    create_id(SUMM_GFREQ_NAMES1[0]): FunctionalRequirementGroup(
        id=create_id(SUMM_GFREQ_NAMES1[0]), title=SUMM_GFREQ_NAMES1[0], 
        grouped_funcreq_ids=[SUMMG_TO_FREQ_REPHRASED1[0][0].id, SUMMG_TO_FREQ_REPHRASED1[0][1].id]
    ),
    create_id(SUMM_GFREQ_NAMES1[2]): FunctionalRequirementGroup(
        id=create_id(SUMM_GFREQ_NAMES1[2]), title=SUMM_GFREQ_NAMES1[2], 
        grouped_funcreq_ids=[SUMMG_TO_FREQ_REPHRASED1[2][0].id, SUMMG_TO_FREQ_REPHRASED1[2][1].id]
    )
}
EXPECTED_FORMATED_FREQS2 = {
    "1": FunctionalRequirement(id="1", statement="спец функ треб #1"),
    "2": FunctionalRequirement(id="2", statement="спец функ треб #2"),
    "6": FunctionalRequirement(id="6", statement="спец функ треб #6"),
    "7": FunctionalRequirement(id="7", statement="спец функ треб #7"),
}

# agent_stubresps: List[str], summ_gfreq_names: List[str], 
# sumgidx_to_rephrased_freqs_map: Dict[int, List[FunctionalRequirement]], 
# expected_fgroups: Dict[str, FunctionalRequirementGroup], 
# expected_freqs: Dict[str, FunctionalRequirement], is_error_expected: bool
FORMATE_GFREQ_TEST_CASES = [
    # 1. нуль summ_gfreq_names
    [[], [], SUMMG_TO_FREQ_REPHRASED1, None, None, True],
    # 2. нуль функциональных требований 
    [[], SUMM_GFREQ_NAMES1, {0: [], 1: [], 2: []}, dict(), dict(), False],
    # 3. присутствуют группы, в которых нуль фунциональных требований
    [[], SUMM_GFREQ_NAMES1, SUMMG_TO_FREQ_REPHRASED2, EXPECTED_FORMATED_GROUPS2, EXPECTED_FORMATED_FREQS2, False],
    # 4. позитивный тест
    [[], SUMM_GFREQ_NAMES1, SUMMG_TO_FREQ_REPHRASED1, EXPECTED_FORMATED_GROUPS1, EXPECTED_FORMATED_FREQS1, False]
]

# agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
# accepted_scenarios: Dict[int, List[Scenario]], expected_fgroups: Dict[str, FunctionalRequirementGroup], 
# expected_freqs: Dict[str, FunctionalRequirement], is_error_expected: bool
FREQ_EXTRACT_TEST_CASES = [
    # 1. пустой task_goal
    # 2. нуль user_stories
    # 3. нуль сценариев
    # 4. присутствуют user-истории, у которых нуль сценариев
    # 5. позитивный тест
]