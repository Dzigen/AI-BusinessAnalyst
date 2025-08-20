import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import UserStory
from src.reasoner.weak.states_handlers.roles_communicator.llm_pipelines import RolesExtractor, RolesExtractorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import REXTR_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, user_stories, expected_output, is_error_expected", REXTR_TEST_CASES)
def test_gie_extract(agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory],
                     expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    rextr_config = RolesExtractorConfig(adriver_config=adriver_config)
    rextr_pipeline = RolesExtractor(config=rextr_config)

    try:
        real_output = rextr_pipeline.extract(task_goal, user_stories)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        real_role_names = list(map(lambda role: role.name, real_output))
        assert len(real_role_names) == len(expected_output)
        assert set(real_role_names) == set(expected_output)