from dataclasses import dataclass, field
from typing import List, Union
from copy import deepcopy

from .config import DEFAULT_FRESTRGEN_TASK_CONFIG, FRESTR_LOG_PATH
from ....utils import WeakReasonerState
from ......specification_model import ReqSpecificationModel
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......specification_model.utils import FunctionalRequirement, FunctionalRestriction
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class FuncRestrGeneratorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    frestr_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_FRESTRGEN_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'funcrestr_generator_cache'

    log: Logger = field(default_factory=lambda: Logger(FRESTR_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.frestr_gen_task_config.version}|{self.lang}"

class FuncRestrGenerator(CacheUtils):
    def __init__(self, config: FuncRestrGeneratorConfig = FuncRestrGeneratorConfig(), 
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

        frestrgen_task_cache_config = None
        if cache_llm_inference:
            frestrgen_task_cache_config = deepcopy(cache_kvdriver_config)

        self.frestrgen_solver = AgentTaskSolver(
            self.agent, self.config.frestr_gen_task_config,
            frestrgen_task_cache_config)
        
    def get_cache_key(self, task_goal: str, func_req: FunctionalRequirement, accepted_frestrs: List[FunctionalRestriction], 
                 declined_frestrs: List[FunctionalRestriction]) -> List[str]:
        
        str_accepted_frestr = '|'.join([frestr.statement for frestr in accepted_frestrs])
        str_declined_frestr = '|'.join([frestr.statement for frestr in declined_frestrs])

        return [self.config.to_str(), task_goal, func_req.statement, str_accepted_frestr, str_declined_frestr]

    @CacheUtils.cache_method_output
    def generate(self, task_goal: str, func_req: FunctionalRequirement, accepted_frestrs: List[FunctionalRestriction], 
                 declined_frestrs: List[FunctionalRestriction]) -> FunctionalRestriction:
        new_frestr, status = self.frestrgen_solver.solve(
            lang=self.config.lang, task_goal=task_goal, func_req=func_req.statement,
            accepted_frestrs=accepted_frestrs, declined_frestrs=declined_frestrs)
        if status != ReturnStatus.success:
            raise NotImplementedError

        return new_frestr