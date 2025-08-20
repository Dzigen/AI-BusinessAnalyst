import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import SystemRequirement
from src.reasoner.utils import DialogueHistory
from src.reasoner.weak.states_handlers.sreq_communicator.llm_pipelines import SysReqExtractor, SysReqExtractorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import SREQEXTR_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, base_dhistory, detailed_dhistory, sr_limit, expected_output, is_error_expected", SREQEXTR_TEST_CASES)
def test_sreqextr(agent_stubresps: List[str], task_goal: str, base_dhistory: DialogueHistory, 
                  detailed_dhistory: DialogueHistory, sr_limit: int, 
                  expected_output: Union[None, List[SystemRequirement]], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    sreqextr_config = SysReqExtractorConfig(adriver_config=adriver_config)
    sreqextr_pipeline = SysReqExtractor(config=sreqextr_config)

    try:
        real_output = sreqextr_pipeline.extract(task_goal, base_dhistory, detailed_dhistory, sr_limit)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        real_sreqs_statements = list(map(lambda role: role.statement, real_output))
        assert len(real_sreqs_statements) == len(expected_output)
        assert set(real_sreqs_statements) == set(expected_output)