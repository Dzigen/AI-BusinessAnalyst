import pytest 
from typing import List, Union, Dict, Tuple
import sys
from copy import deepcopy
sys.path.insert(0, "../")

from src.specification_model.utils import FunctionalRequirement, FunctionalRequirementGroup, UserStory, Scenario
from src.reasoner.weak.states_handlers.freq_communicator.llm_pipelines import FuncReqExtractor, FuncReqExtractorConfig
from src.agents.connectors.StubAgentConnector import DEFAULT_STUBAGENT_CONFIG
from src.agents import AgentDriverConfig

from cases import EXTRACT_BASE_FREQS_TEST_CASES, EXTRACT_BASE_GFREQ_TEST_CASES, \
    SUMM_BASE_GFREQ_TEST_CASES, GROUP_FREQS_TEST_CASES, REPHRASE_FREQ_GROUPS_TEST_CASES, \
        FORMATE_GFREQ_TEST_CASES, FREQ_EXTRACT_TEST_CASES

@pytest.mark.parametrize("agent_stubresps, task_goal, user_stories, accepted_scenarios, expected_output, is_error_expected",
                          EXTRACT_BASE_FREQS_TEST_CASES)
def test_extract_basefreqs(agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
                          accepted_scenarios: Dict[int, List[Scenario]], expected_output: Union[None,Dict[str,List[str]]], 
                          is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_output = freqextr_pipeline.extract_base_freqs(task_goal, user_stories, accepted_scenarios)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert len(real_output) == len(expected_output)
        for us_id, expected_freqs in expected_output.items():
            assert us_id in real_output.keys()
            assert len(real_output[us_id]) == len(expected_freqs)
            assert set(real_output[us_id]) == set(expected_freqs) 


@pytest.mark.parametrize("agent_stubresps, task_goal, user_stories, us_to_basefreqs_map, expected_output, is_error_expected",
                          EXTRACT_BASE_GFREQ_TEST_CASES)
def test_extract_basegfreqnames(agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
                          us_to_basefreqs_map: Dict[str,List[str]], expected_output: Union[None,List[str]], 
                          is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_output = freqextr_pipeline.extract_base_gfreq_names(task_goal, user_stories, us_to_basefreqs_map)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert len(real_output) == len(expected_output)
        assert set(real_output) == set(expected_output) 

@pytest.mark.parametrize("agent_stubresps, task_goal, base_gfreq_names, expected_output, is_error_expected",
                          SUMM_BASE_GFREQ_TEST_CASES)
def test_summ_basegfreqnames(agent_stubresps: List[str], task_goal: str,  base_gfreq_names: List[str], 
                             expected_output: Union[None,List[str]], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_output = freqextr_pipeline.summ_basegfreq_names(task_goal, base_gfreq_names)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert len(real_output) == len(expected_output)
        assert set(real_output) == set(expected_output) 


@pytest.mark.parametrize("agent_stubresps, task_goal, user_stories, summ_gfreq_names, us_to_basefreqs_map, expected_output, is_error_expected",
                          GROUP_FREQS_TEST_CASES)
def test_group_freqsbysummnames(agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
                                summ_gfreq_names: List[str], us_to_basefreqs_map: Dict[str,List[str]],
                                expected_output: Union[None, Dict[int, List[str]]], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_output = freqextr_pipeline.group_freqs_by_summnames(task_goal, user_stories, summ_gfreq_names, us_to_basefreqs_map)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert len(real_output) == len(expected_output)
        for sumgidx, expected_freqs in expected_output.items():
            assert sumgidx in real_output.keys()
            assert len(real_output[sumgidx]) == len(expected_freqs)
            assert set(real_output[sumgidx]) == set(expected_freqs) 

@pytest.mark.parametrize("agent_stubresps, task_goal, summ_gfreq_names, sumgidx_to_freqs_map, expected_output, is_error_expected",
                          REPHRASE_FREQ_GROUPS_TEST_CASES)
def test_rephrase_freqgroups(agent_stubresps: List[str], task_goal: str, summ_gfreq_names: List[str], 
                             sumgidx_to_freqs_map: Dict[int, List[str]], 
                             expected_output: Union[None, Dict[int, List[FunctionalRequirement]]], 
                             is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_output = freqextr_pipeline.rephrase_freq_groups(task_goal, summ_gfreq_names, sumgidx_to_freqs_map)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        
        assert len(real_output) == len(expected_output)
        for sumgidx, expected_freqs in expected_output.items():
            assert sumgidx in real_output.keys()
            
            expected_freqs = [freq.statement for freq in expected_freqs]
            real_freqs = [freq.statement for freq in real_output[sumgidx]]
            
            assert len(real_freqs) == len(expected_freqs)
            assert set(real_freqs) == set(expected_freqs) 


@pytest.mark.parametrize("agent_stubresps, summ_gfreq_names, sumgidx_to_rephrased_freqs_map, expected_fgroups, expected_freqs, is_error_expected",
                          FORMATE_GFREQ_TEST_CASES)
def test_formate_freqgroups(agent_stubresps: List[str], summ_gfreq_names: List[str], 
                            sumgidx_to_rephrased_freqs_map: Dict[int, List[FunctionalRequirement]],
                            expected_fgroups: Dict[str, FunctionalRequirementGroup], expected_freqs:  Dict[str, FunctionalRequirement],
                            is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_fgroups, real_freqs = freqextr_pipeline.formate_freq_groups(summ_gfreq_names, sumgidx_to_rephrased_freqs_map)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        
        assert len(real_fgroups) == len(expected_fgroups)
        assert len(real_freqs) == len(expected_freqs)

        flatten_expected_freqs = [freq.statement for freq in expected_freqs.values()]
        flatten_real_freqs = [freq.statement for freq in real_freqs.values()]
        assert set(flatten_real_freqs) == set(flatten_expected_freqs)

        for real_fgroup in real_fgroups.values():
            assert real_fgroup.id in expected_fgroups.keys()
            expected_fgroup = expected_fgroups[real_fgroup.id]
            assert real_fgroup.title == expected_fgroup.title
            
            cur_real_freqs = [real_freqs[real_freq_id].statement for real_freq_id in real_fgroup.grouped_funcreq_ids]
            cur_expected_freqs = [expected_freqs[expected_freq_id].statement for expected_freq_id in expected_fgroup.grouped_funcreq_ids]
            assert len(cur_real_freqs) == len(cur_expected_freqs)
            assert set(cur_real_freqs) == set(cur_expected_freqs)

@pytest.mark.parametrize("agent_stubresps, task_goal, user_stories, accepted_scenarios, expected_fgroups, expected_freqs, is_error_expected", 
                         FREQ_EXTRACT_TEST_CASES)
def test_freq_extract(agent_stubresps: List[str], task_goal: str, user_stories: List[UserStory], 
                  accepted_scenarios: Dict[int, List[Scenario]], expected_fgroups: Dict[str, FunctionalRequirementGroup], 
                  expected_freqs: Dict[str, FunctionalRequirement], is_error_expected: bool) -> None:
    agent_config = deepcopy(DEFAULT_STUBAGENT_CONFIG)
    agent_config.ext_params['stub_answers'] = agent_stubresps
    adriver_config = AgentDriverConfig(name='stub', agent_config=agent_config)
    
    freqextr_config = FuncReqExtractorConfig(adriver_config=adriver_config)
    freqextr_pipeline = FuncReqExtractor(config=freqextr_config)

    try:
        real_fgroups, real_freqs = freqextr_pipeline.extract(task_goal, user_stories, accepted_scenarios)
    except (ValueError, NotImplementedError) as e:
        assert is_error_expected
    else:
        assert not is_error_expected
        assert len(real_fgroups) == len(expected_fgroups)
        assert len(expected_freqs) == len(real_freqs)

        for real_fgroup in real_fgroups:
            assert real_fgroup.id in expected_fgroup.keys()
            expected_fgroup = expected_fgroups[real_fgroup.id]
            assert real_fgroup.title == expected_fgroup.title
            
            real_freqs = [real_freqs[real_freq_id].statement for real_freq_id in real_fgroup.grouped_funcreq_ids]
            expected_freqs = [expected_freqs[expected_freq_id].statement for expected_freq_id in expected_fgroup.grouped_funcreq_ids]
            assert len(real_freqs) == len(expected_freqs)
            assert set(real_freqs) == set(expected_freqs)
