import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import SystemRequirement, SystemRestriction
from src.reasoner.weak.states_handlers.srestr_communicator.llm_pipelines import SysRestrGenerator, SysRestrGeneratorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import SRESTRGEN_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, sys_req, accepted_srestrs, declined_srestrs, expected_output, is_error_expected", SRESTRGEN_TEST_CASES)
def test_srestrgen(agent_stubresps: List[str], task_goal: str, sys_req: SystemRequirement, 
                  accepted_srestrs: List[SystemRestriction], declined_srestrs: List[SystemRestriction],
                  expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    srestrgen_config = SysRestrGeneratorConfig(adriver_config=adriver_config)
    srestrgen_pipeline = SysRestrGenerator(config=srestrgen_config)

    try:
        real_output = srestrgen_pipeline.generate(task_goal,  sys_req, accepted_srestrs, declined_srestrs)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output.statement == expected_output