import pytest 
from typing import Dict, List, Tuple, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory
from src.reasoner.weak.states_handlers.bp_communicator.llm_pipelines import BPClarifier, BPClarifierConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import BPCLRF_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, base_dhistory, detail_dhistory, expected_output, is_error_expected", BPCLRF_TEST_CASES)
def test_gie_extract(agent_stubresps: List[str], base_dhistory: DialogueHistory, detail_dhistory: DialogueHistory,
                     expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    bpc_config = BPClarifierConfig(adriver_config=adriver_config)
    bpc_pipeline = BPClarifier(config=bpc_config)

    try:
        real_output = bpc_pipeline.generate_question(base_dhistory, detail_dhistory)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output