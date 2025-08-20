import pytest 
from typing import List, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import FunctionalRequirement, FunctionalRestriction
from src.reasoner.weak.states_handlers.frestr_communicator.llm_pipelines import FuncRestrGenerator, FuncRestrGeneratorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import FRESTRGEN_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, func_req, accepted_frestrs, declined_frestrs, expected_output, is_error_expected", FRESTRGEN_TEST_CASES)
def test_frestrgen(agent_stubresps: List[str], task_goal: str, func_req: FunctionalRequirement, 
                  accepted_frestrs: List[FunctionalRestriction], declined_frestrs: List[FunctionalRestriction],
                  expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    frestrgen_config = FuncRestrGeneratorConfig(adriver_config=adriver_config)
    frestrgen_pipeline = FuncRestrGenerator(config=frestrgen_config)

    try:
        real_output = frestrgen_pipeline.generate(task_goal,  func_req, accepted_frestrs, declined_frestrs)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output.statement == expected_output