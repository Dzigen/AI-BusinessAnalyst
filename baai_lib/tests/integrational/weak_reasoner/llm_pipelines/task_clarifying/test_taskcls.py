import pytest 
from typing import Dict, List, Set, Union
from copy import deepcopy
import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory
from src.reasoner.weak.states_handlers.taskg_communicator.llm_pipelines.TaskClassifier import TaskClassifier, TaskClassifierConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig
from cases import TASKCLS_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, dhistory, expected_output, is_error_expected", TASKCLS_TEST_CASES)
def test_taskcls(agent_stubresps: List[str], dhistory: DialogueHistory,
                     expected_output: Union[None, str], is_error_expected: bool) -> None:

    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    taskcls_config = TaskClassifierConfig(adriver_config=adriver_config)
    taskcls_pipeline = TaskClassifier(config=taskcls_config)

    try:
        real_output = taskcls_pipeline.is_task_supported(dhistory)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output