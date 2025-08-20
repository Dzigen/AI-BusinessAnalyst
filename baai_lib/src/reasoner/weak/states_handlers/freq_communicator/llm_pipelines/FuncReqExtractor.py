from dataclasses import dataclass, field
from typing import List, Union, Tuple, Dict
from collections import defaultdict
from functools import reduce
from copy import deepcopy

from .config import DEFAULT_FREQEXTRACT_TASK_CONFIG, DEFAULT_BASEFREQGGEN_TASK_CONFIG, \
    DEFAULT_SUMFREQGGEN_TASK_CONFIG, DEFAULT_RELFREQGDETECT_TASK_CONFIG, \
        DEFAULT_RELFREQGEXTRACT_TASK_CONFIG, DEFAULT_FREQGREFORM_TASK_CONFIG, FREQ_LOG_PATH
from ......specification_model import ReqSpecificationModel
from ......specification_model.utils import UserStory, Scenario
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......specification_model.utils import FunctionalRequirement, FunctionalRequirementGroup
from ......utils.cache_kv import CacheKV, CacheUtils
from ......utils.data_structs import create_id

@dataclass
class FuncReqExtractorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    s_freq_extr_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_FREQEXTRACT_TASK_CONFIG)
    
    base_rgroups_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_BASEFREQGGEN_TASK_CONFIG)
    summ_rgroups_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_SUMFREQGGEN_TASK_CONFIG)
    
    rel_greps_detect_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_RELFREQGDETECT_TASK_CONFIG)
    rel_greps_extr_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_RELFREQGEXTRACT_TASK_CONFIG)

    greqs_reform_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_FREQGREFORM_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'funcreq_extractor_cache'

    log: Logger = field(default_factory=lambda: Logger(FREQ_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        str_base_config = f"{self.adriver_config.to_str()}|{self.lang}"
        str_rgroups_gen = f"{self.base_rgroups_gen_task_config.version}|{self.summ_rgroups_gen_task_config.version}"
        str_rel_greps = f"{self.rel_greps_detect_task_config.version}|{self.rel_greps_extr_task_config.version}"

        return f"{str_base_config}|{self.s_freq_extr_task_config.version}|{str_rgroups_gen}|{str_rel_greps}|{self.greqs_reform_task_config.version}"

class FuncReqExtractor(CacheUtils):
    def __init__(self, config: FuncReqExtractorConfig = FuncReqExtractorConfig(), 
                 cache_kvdriver_config: KeyValueDriverConfig = None,
                 cache_llm_inference: bool = False):
        self.log = config.log
        self.verbose = config.verbose
        self.config = config

        if cache_kvdriver_config is not None and self.config.cache_table_name is not None:
            cache_config = deepcopy(cache_kvdriver_config)
            cache_config.db_config.db_info['table'] = self.config.cache_table_name
            self.cachekv = CacheKV(cache_config)
        else:
            self.cachekv = None

        self.agent = AgentDriver.connect(config.adriver_config)

        s_freqextr_task_cache_config = None
        b_rgroupsgen_task_cache_config = None
        s_rgroupsgen_task_cache_config = None
        rel_grepsdetect_task_cache_config = None
        rel_grepsextr_task_cache_config = None
        greqs_reform_task_cache_config = None
        if cache_llm_inference:
            s_freqextr_task_cache_config = deepcopy(cache_kvdriver_config)
            b_rgroupsgen_task_cache_config = deepcopy(cache_kvdriver_config)
            s_rgroupsgen_task_cache_config = deepcopy(cache_kvdriver_config)
            rel_grepsdetect_task_cache_config = deepcopy(cache_kvdriver_config)
            rel_grepsextr_task_cache_config = deepcopy(cache_kvdriver_config)
            greqs_reform_task_cache_config = deepcopy(cache_kvdriver_config)

        self.s_freqextr_solver = AgentTaskSolver(
            self.agent, self.config.s_freq_extr_task_config,
            s_freqextr_task_cache_config)
        
        self.b_rgroupsgen_solver = AgentTaskSolver(
            self.agent, self.config.base_rgroups_gen_task_config,
            b_rgroupsgen_task_cache_config)
        self.s_rgroupsgen_solver = AgentTaskSolver(
            self.agent, self.config.summ_rgroups_gen_task_config,
            s_rgroupsgen_task_cache_config)
        
        self.rel_grepsdetect_solver = AgentTaskSolver(
            self.agent, self.config.rel_greps_detect_task_config,
            rel_grepsdetect_task_cache_config)
        self.rel_grepsextr_solver = AgentTaskSolver(
            self.agent, self.config.rel_greps_extr_task_config,
            rel_grepsextr_task_cache_config)
        
        self.greqs_reform_solver = AgentTaskSolver(
            self.agent, self.config.greqs_reform_task_config,
            greqs_reform_task_cache_config)
        
    def get_cache_key(self,  task_goal: str, user_stories: List[UserStory], accepted_scenarios: Dict[str, List[Scenario]]) -> List[str]:
        
        str_user_stories = '|'.join([us.statement for us in user_stories])
        flatten_scenarios = reduce(lambda acc, v: acc + v, list(accepted_scenarios.values()), [])
        str_scenarios = '|'.join([scenario.formate_to_str() for scenario in flatten_scenarios])

        return [self.config.to_str(), task_goal, str_user_stories, str_scenarios]

    def extract_base_freqs(self, task_goal: str, user_stories: List[UserStory], 
                           accepted_scenarios: Dict[str, List[Scenario]]) -> Dict[str,List[str]]:
        if len(user_stories) < len(accepted_scenarios.keys()):
            raise ValueError
        
        us_to_freqs_map = dict()
        for user_story in user_stories:
            if user_story.id not in accepted_scenarios.keys():
                continue
            cur_accepted_scenarios = accepted_scenarios[user_story.id]
            unique_raw_freqs = set()

            for scenario in cur_accepted_scenarios:
                raw_freq, status = self.s_freqextr_solver.solve(
                    lang=self.config.lang, task_goal=task_goal, user_story=user_story.statement, 
                    scenario=scenario)
                if status != ReturnStatus.success:
                    raise NotImplementedError
                unique_raw_freqs.update(raw_freq)

            if len(unique_raw_freqs) > 0:
                us_to_freqs_map[user_story.id] = list(unique_raw_freqs)

        return us_to_freqs_map

    def extract_base_gfreq_names(self, task_goal: str, user_stories: List[UserStory], 
                                 us_to_basefreqs_map: Dict[str,List[str]]) -> List[str]:
        if len(user_stories) < len(us_to_basefreqs_map.keys()):
            raise ValueError
        
        base_gfreq_names = set()
        for user_story in user_stories:
            if user_story.id not in us_to_basefreqs_map:
                continue
            
            cur_freqs = us_to_basefreqs_map[user_story.id]
            if len(cur_freqs) < 1:
                continue

            cur_bgfreqs, status = self.b_rgroupsgen_solver.solve(
                lang=self.config.lang, task_goal=task_goal, user_story=user_story.statement, func_reqs=cur_freqs)
            if status != ReturnStatus.success:
                raise NotImplementedError
            base_gfreq_names.update(cur_bgfreqs)

        return list(base_gfreq_names)
    
    def summ_basegfreq_names(self, task_goal: str, base_gfreq_names: List[str]) -> List[str]:
        summ_gfreq_names, status = self.s_rgroupsgen_solver.solve(
            lang=self.config.lang, task_goal=task_goal, base_gnames=base_gfreq_names)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return summ_gfreq_names
    
    def group_freqs_by_summnames(self, task_goal: str, user_stories: List[UserStory], summ_gfreq_names: List[str], 
                                 us_to_basefreqs_map: Dict[str,List[str]]) -> Dict[int, List[str]]:
        if len(summ_gfreq_names) < 1:
            raise ValueError
        if len(user_stories) < len(us_to_basefreqs_map.keys()):
            raise ValueError
        
        sumgidx_to_freqs_map = defaultdict(list)
        for user_story in user_stories:
            if user_story.id not in us_to_basefreqs_map.keys():
                continue 
            cur_freqs = us_to_basefreqs_map[user_story.id]
            
            for i, cur_sumgfreq_name in enumerate(summ_gfreq_names):
                if len(cur_freqs) < 1:
                    continue

                is_cur_group_detected, status = self.rel_grepsdetect_solver.solve(
                    lang=self.config.lang, task_goal=task_goal, 
                    current_freqt=cur_sumgfreq_name, other_freqts=summ_gfreq_names[i:],
                    func_reqs=cur_freqs)
                if status != ReturnStatus.success:
                    raise NotImplementedError

                if not is_cur_group_detected:
                    continue

                cur_extracted_freq_idxs, status = self.rel_grepsextr_solver.solve(
                    lang=self.config.lang, task_goal=task_goal, 
                    current_freqt=cur_sumgfreq_name, other_freqts=summ_gfreq_names[i:],
                    func_reqs=cur_freqs)
                if status != ReturnStatus.success:
                    raise NotImplementedError
                
                filterd_freqs = [cur_freqs[freq_idx] for freq_idx in cur_extracted_freq_idxs]
                sumgidx_to_freqs_map[i] += filterd_freqs

                cur_freqs = [cur_freqs[freq_idx] for freq_idx in range(len(cur_freqs)) if freq_idx not in cur_extracted_freq_idxs]
                
        return dict(sumgidx_to_freqs_map)
    
    def rephrase_freq_groups(self, task_goal: str, summ_gfreq_names: List[str], 
                             sumgidx_to_freqs_map: Dict[int, List[str]]) -> Dict[int, List[FunctionalRequirement]]:
        if len(summ_gfreq_names) < 1:
            raise ValueError
        if len(summ_gfreq_names) < len(sumgidx_to_freqs_map.keys()):
            raise ValueError
        
        rephrased_freq_groups = dict()
        for sumgidx, raw_freqs in sumgidx_to_freqs_map.items():
            if len(raw_freqs) < 1:
                continue

            cur_rephrased_freqs, status = self.greqs_reform_solver.solve(
                lang=self.config.lang, task_goal=task_goal, 
                freq_title=summ_gfreq_names[sumgidx], freqs=raw_freqs)
            if status != ReturnStatus.success:
                raise NotImplementedError
            
            rephrased_freq_groups[sumgidx] = cur_rephrased_freqs

        return rephrased_freq_groups
    
    def formate_freq_groups(self, summ_gfreq_names: List[str], 
                            sumgidx_to_rephrased_freqs_map: Dict[int, List[FunctionalRequirement]])\
                                -> Tuple[Dict[str, FunctionalRequirementGroup],Dict[str, FunctionalRequirement]]:
        if len(summ_gfreq_names) < 1:
            raise ValueError
        if len(summ_gfreq_names) < len(sumgidx_to_rephrased_freqs_map.keys()):
            raise ValueError
        
        formated_freq_groups = dict()
        formated_freqs = dict()
        for sumgidx, freqs in sumgidx_to_rephrased_freqs_map.items():
            if len(freqs) < 1:
                continue

            cur_gname = summ_gfreq_names[sumgidx]
            formated_freq_group = FunctionalRequirementGroup(
                id=create_id(cur_gname), title=cur_gname,
                grouped_funcreq_ids=[freq.id for freq in freqs])
            formated_freq_groups[formated_freq_group.id] = formated_freq_group

            formated_freqs.update({freq.id: freq for freq in freqs})
        
        return formated_freq_groups, formated_freqs

    @CacheUtils.cache_method_output
    def extract(self, task_goal: str, user_stories: List[UserStory], accepted_scenarios: Dict[str, List[Scenario]])\
          -> Tuple[Dict[str, FunctionalRequirementGroup], Dict[str, FunctionalRequirement]]:
        
        us_to_basefreqs_map = self.extract_base_freqs(task_goal, user_stories,accepted_scenarios) 
        base_gfreq_names = self.extract_base_gfreq_names(task_goal, user_stories, us_to_basefreqs_map)

        summ_gfreq_names = self.summ_basegfreq_names(task_goal, base_gfreq_names)
        sumgidx_to_freqs_map = self.group_freqs_by_summnames(task_goal, user_stories, summ_gfreq_names, 
                                                             us_to_basefreqs_map)

        sumgidx_to_rephrased_freqs_map = self.rephrase_freq_groups(task_goal, summ_gfreq_names, 
                                                                   sumgidx_to_freqs_map)
        formated_freq_groups, formated_freqs = self.formate_freq_groups(
            summ_gfreq_names, sumgidx_to_rephrased_freqs_map)
        
        return formated_freq_groups, formated_freqs
                
