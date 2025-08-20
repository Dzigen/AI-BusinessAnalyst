import pytest 
from typing import Dict, List, Tuple, Union
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory
from src.reasoner.weak.states_handlers.taskg_communicator.llm_pipelines import GeneralInfoExtractor, GeneralInfoExtractorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import GIE_EXTRACT_TEST_CASES, GIE_SUMMIN_TEST_CASES, \
    GIE_SUMMST_TEST_CASES, GIE_SUMMTG_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, dhistory, expected_output, is_error_expected", GIE_EXTRACT_TEST_CASES)
def test_gie_extract(agent_stubresps: List[str], dhistory: DialogueHistory, 
                     expected_output: Union[None, Tuple[str,str,str]], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    gie_config = GeneralInfoExtractorConfig(adriver_config=adriver_config)
    gie_pipeline = GeneralInfoExtractor(config=gie_config)

    try:
        real_output = gie_pipeline.extract(dhistory)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output

@pytest.mark.parametrize("agent_stubresps, dhistory, task_goal, expected_output, is_error_expected", GIE_SUMMIN_TEST_CASES)
def test_gie_summin(agent_stubresps: List[str], dhistory: DialogueHistory, task_goal: str, 
                     expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    gie_config = GeneralInfoExtractorConfig(adriver_config=adriver_config)
    gie_pipeline = GeneralInfoExtractor(config=gie_config)

    try:
        real_output = gie_pipeline.summarize_integration(dhistory, task_goal)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output

@pytest.mark.parametrize("agent_stubresps, dhistory, task_goal, expected_output, is_error_expected", GIE_SUMMST_TEST_CASES)
def test_gie_summst(agent_stubresps: List[str], dhistory: DialogueHistory, task_goal: str, 
                     expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    gie_config = GeneralInfoExtractorConfig(adriver_config=adriver_config)
    gie_pipeline = GeneralInfoExtractor(config=gie_config)

    try:
        real_output = gie_pipeline.summarize_sub_tasks(dhistory, task_goal)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output

@pytest.mark.parametrize("agent_stubresps, dhistory, expected_output, is_error_expected", GIE_SUMMTG_TEST_CASES)
def test_gie_summtg(agent_stubresps: List[str], dhistory: DialogueHistory,
                     expected_output: Union[None, str], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    gie_config = GeneralInfoExtractorConfig(adriver_config=adriver_config)
    gie_pipeline = GeneralInfoExtractor(config=gie_config)

    try:
        real_output = gie_pipeline.summarize_task_goal(dhistory)
    except NotImplementedError:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert real_output == expected_output