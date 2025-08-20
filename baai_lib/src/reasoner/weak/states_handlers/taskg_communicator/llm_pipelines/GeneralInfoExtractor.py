from dataclasses import dataclass, field
from typing import Tuple, Union, List
from copy import deepcopy

from .config import DEFAULT_GTSUMM_TASK_CONFIG, DEFAULT_STSUMM_TASK_CONFIG, \
    DEFAULT_INGRSUMM_TASK_CONFIG, GINFOEXTR_MAIN_LOG_PATH
from .....utils import DialogueHistory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class GeneralInfoExtractorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    gtask_summ_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_GTSUMM_TASK_CONFIG)
    subt_summ_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_STSUMM_TASK_CONFIG)
    intgr_summ_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_INGRSUMM_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'ginfo_extractor_cache'

    log: Logger = field(default_factory=lambda: Logger(GINFOEXTR_MAIN_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.gtask_summ_task_config.version}|{self.subt_summ_task_config.version}|{self.intgr_summ_task_config.version}|{self.lang}"


class GeneralInfoExtractor(CacheUtils):

    def __init__(self, config: GeneralInfoExtractorConfig = GeneralInfoExtractorConfig(), 
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

        gtasksumm_task_cache_config = None
        subtsumm_task_cache_config = None
        intgrsumm_task_cache_config = None
        if cache_llm_inference:
            gtasksumm_task_cache_config = deepcopy(cache_kvdriver_config)
            subtsumm_task_cache_config = deepcopy(cache_kvdriver_config)
            intgrsumm_task_cache_config = deepcopy(cache_kvdriver_config)

        self.gtasksumm_solver = AgentTaskSolver(
            self.agent, self.config.gtask_summ_task_config,
            gtasksumm_task_cache_config)
        self.subtsumm_solver = AgentTaskSolver(
            self.agent, self.config.subt_summ_task_config,
            subtsumm_task_cache_config)
        self.intgrsumm_solver = AgentTaskSolver(
            self.agent, self.config.intgr_summ_task_config,
            intgrsumm_task_cache_config)

    def summarize_task_goal(self, dhistory: DialogueHistory) -> str:
        summary, status = self.gtasksumm_solver.solve(
            lang=self.config.lang, dhistory=dhistory)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return summary

    def summarize_sub_tasks(self, dhistory: DialogueHistory, task_goal: str) -> str:
        summary, status = self.subtsumm_solver.solve(
            lang=self.config.lang, dhistory=dhistory, task_goal=task_goal)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return summary

    def summarize_integration(self, dhistory: DialogueHistory, task_goal: str) -> str:
        summary, status = self.intgrsumm_solver.solve(
            lang=self.config.lang, dhistory=dhistory, task_goal=task_goal)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return summary

    def get_cache_key(self, base_dhistory: DialogueHistory) -> List[str]:
        str_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in base_dhistory.sequence])

        return [self.config.to_str(), str_dhistory]

    @CacheUtils.cache_method_output
    def extract(self, base_dhistory: DialogueHistory) -> Tuple[str,str,str]:
        task_goal = self.summarize_task_goal(base_dhistory)
        sub_tasks = self.summarize_sub_tasks(base_dhistory, task_goal)
        integration = self.summarize_integration(base_dhistory, task_goal)

        return task_goal, sub_tasks, integration