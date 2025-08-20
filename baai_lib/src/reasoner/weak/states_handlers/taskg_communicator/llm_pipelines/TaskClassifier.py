from dataclasses import dataclass, field
from typing import Union, List
from copy import deepcopy

from .config import DEFAULT_TCLS_TASK_CONFIG, TCLASSIFIER_MAIN_LOG_PATH
from .....utils import DialogueHistory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class TaskClassifierConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    tclassify_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_TCLS_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'taskg_cls_cache'

    log: Logger = field(default_factory=lambda: Logger(TCLASSIFIER_MAIN_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.tclassify_task_config.version}|{self.lang}"

class TaskClassifier(CacheUtils):
    def __init__(self, config: TaskClassifierConfig = TaskClassifierConfig(), 
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

        cls_task_cache_config = None
        if cache_llm_inference:
            cls_task_cache_config = deepcopy(cache_kvdriver_config)

        self.cls_solver = AgentTaskSolver(
            self.agent, self.config.tclassify_task_config,
            cls_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose
        
    def get_cache_key(self, base_dhistory: DialogueHistory) -> List[str]:
        str_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in base_dhistory.sequence])
        return [self.config.to_str(), str_dhistory]

    @CacheUtils.cache_method_output
    def is_task_supported(self, base_dhistory: DialogueHistory) -> bool:
        flag, status = self.cls_solver.solve(lang=self.config.lang, dhistory=base_dhistory)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return flag