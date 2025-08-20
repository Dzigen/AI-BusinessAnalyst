from dataclasses import dataclass, field
from typing import List, Union
from copy import deepcopy

from .config import DEFAULT_SREQEXTR_TASK_CONFIG, SREQ_LOG_PATH
from .....utils import DialogueHistory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......specification_model.utils import SystemRequirement
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class SysReqExtractorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    sreq_extr_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_SREQEXTR_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'sysreq_extractor_cache'

    log: Logger = field(default_factory=lambda: Logger(SREQ_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.sreq_extr_task_config.version}|{self.lang}"

class SysReqExtractor(CacheUtils):
    def __init__(self, config: SysReqExtractorConfig = SysReqExtractorConfig(), 
                 cache_kvdriver_config: KeyValueDriverConfig = None,
                 cache_llm_inference: bool = False):
        self.config = config

        if cache_kvdriver_config is not None and self.config.cache_table_name is not None:
            cache_config = deepcopy(cache_kvdriver_config)
            cache_config.db_config.db_info['table'] = self.config.cache_table_name
            self.cachekv = CacheKV(cache_config)
        else:
            self.cachekv = None

        self.agent = AgentDriver.connect(config.adriver_config)

        sreqextr_task_cache_config = None
        if cache_llm_inference:
            sreqextr_task_cache_config = deepcopy(cache_kvdriver_config)

        self.sreqextr_solver = AgentTaskSolver(
            self.agent, self.config.sreq_extr_task_config,
            sreqextr_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose
        
    def get_cache_key(self, task_goal: str, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, sr_limit: int) -> List[str]:
        str_detail_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in base_dhistory.sequence])
        str_base_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in detailed_dhistory.sequence])

        return [self.config.to_str(), task_goal, str_detail_dhistory, str_base_dhistory, str(sr_limit)]

    @CacheUtils.cache_method_output
    def extract(self, task_goal: str, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, sr_limit: int = -1) -> List[SystemRequirement]: 
        if sr_limit == 0:
            raise ValueError
               
        sys_reqs, status = self.sreqextr_solver.solve(lang=self.config.lang, task_goal=task_goal, 
                                base_dhistory=base_dhistory, detailed_dhistory=detailed_dhistory, 
                                sr_limit=sr_limit)
        if status != ReturnStatus.success:
            raise NotImplementedError

        if sr_limit > 0:
            sys_reqs = sys_reqs[:sr_limit]

        return sys_reqs