import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import UserStory, Scenario
from src.reasoner.weak.states_handlers.scenarios_communicator.llm_pipelines import ScenariosGenerator, ScenariosGeneratorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import SCENGEN_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, user_story, accepted_scenarios, declined_scenarios, expected_output, is_error_expected", SCENGEN_TEST_CASES)
def test_scengen(agent_stubresps: List[str], task_goal: str, user_story: UserStory, 
                 accepted_scenarios: List[Scenario], declined_scenarios: List[Scenario],
                 expected_output: Union[None, Scenario], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    scengen_config = ScenariosGeneratorConfig(adriver_config=adriver_config)
    scengen_pipeline = ScenariosGenerator(config=scengen_config)

    try:
        real_output = scengen_pipeline.generate(task_goal, user_story, accepted_scenarios, declined_scenarios)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output.title == expected_output.title
        assert real_output.steps == expected_output.steps
        assert real_output.related_userstory_ids == expected_output.related_userstory_ids