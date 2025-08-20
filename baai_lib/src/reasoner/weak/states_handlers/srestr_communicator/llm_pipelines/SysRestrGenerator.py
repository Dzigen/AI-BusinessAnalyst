from dataclasses import dataclass, field
from typing import List, Union
from copy import deepcopy

from .config import DEFAULT_SRESTRGEN_TASK_CONFIG, SRESTR_LOG_PATH
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......specification_model.utils import SystemRequirement, SystemRestriction
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class SysRestrGeneratorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    srestr_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_SRESTRGEN_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'sysrestr_generator_cache'

    log: Logger = field(default_factory=lambda: Logger(SRESTR_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.srestr_gen_task_config.version}|{self.lang}"

class SysRestrGenerator(CacheUtils):
    def __init__(self, config: SysRestrGeneratorConfig = SysRestrGeneratorConfig(), 
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

        srestrgen_task_cache_config = None
        if cache_llm_inference:
            srestrgen_task_cache_config = deepcopy(cache_kvdriver_config)

        self.srestrgen_solver = AgentTaskSolver(
            self.agent, self.config.srestr_gen_task_config,
            srestrgen_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose
        
    def get_cache_key(self, task_goal: str, sys_req: SystemRequirement, accepted_srestrs: List[SystemRestriction], 
                 declined_srestrs: List[SystemRestriction]) -> List[str]:
        str_accepted_srestrs = '|'.join([srestr.statement for srestr in accepted_srestrs])
        str_declined_srestrs = '|'.join([srestr.statement for srestr in declined_srestrs])

        return [self.config.to_str(), task_goal, sys_req.statement, str_accepted_srestrs, str_declined_srestrs]

    @CacheUtils.cache_method_output
    def generate(self, task_goal: str, sys_req: SystemRequirement, accepted_srestrs: List[SystemRestriction], 
                 declined_srestrs: List[SystemRestriction]) -> SystemRestriction:
        
        new_srestr, status = self.srestrgen_solver.solve(
            lang=self.config.lang, task_goal=task_goal, sys_req=sys_req.statement,
            accepted_sys_restrs=accepted_srestrs, declined_sys_restrs=declined_srestrs)
        if status != ReturnStatus.success:
            raise NotImplementedError

        return new_srestr