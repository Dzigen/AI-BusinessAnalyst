import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory
from src.reasoner.weak.states_handlers.us_communicator.llm_pipelines import UserStoriesExtractor, UserStoriesExtractorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import USEXTR_TEST_CASES, ISUSVALID_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, base_dhistory, detailed_dhistory, us_limit, expected_output, is_error_expected", USEXTR_TEST_CASES)
def test_usextr(agent_stubresps: List[str], task_goal: str, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, 
                     us_limit: int, expected_output: Union[None, List[str]], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    usextr_config = UserStoriesExtractorConfig(adriver_config=adriver_config)
    usextr_pipeline = UserStoriesExtractor(config=usextr_config)

    try:
        real_output = usextr_pipeline.extract_userstories(task_goal, base_dhistory, detailed_dhistory, us_limit)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        real_us_statements = list(map(lambda us: us.statement, real_output))
        assert len(real_us_statements) == len(expected_output)
        assert set(real_us_statements) == set(expected_output)

@pytest.mark.parametrize("agent_stubresps, task_goal, user_story, expected_output, is_error_expected", ISUSVALID_TEST_CASES)
def test_isusvalid(agent_stubresps: List[str], task_goal: str, user_story: str, expected_output: bool, is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    usextr_config = UserStoriesExtractorConfig(adriver_config=adriver_config)
    usextr_pipeline = UserStoriesExtractor(config=usextr_config)

    try:
        real_output = usextr_pipeline.is_userstory_valid(task_goal, user_story)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert expected_output == real_output