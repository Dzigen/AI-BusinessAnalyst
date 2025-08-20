from dataclasses import dataclass, field
from copy import deepcopy
from typing import Union, List

from .config import DEFAULT_BPCQGEN_TASK_CONFIG, BPCLARIFIER_LOG_PATH
from .....utils import DialogueHistory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class BPClarifierConfig:
    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    cqgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_BPCQGEN_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'bpcq_gen_cache'

    log: Logger = field(default_factory=lambda: Logger(BPCLARIFIER_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.cqgen_task_config.version}|{self.lang}"

class BPClarifier(CacheUtils):
    def __init__(self, config: BPClarifierConfig = BPClarifierConfig(), 
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

        cqgen_task_cache_config = None
        if cache_llm_inference:
            cqgen_task_cache_config = deepcopy(cache_kvdriver_config)

        self.cqgen_solver = AgentTaskSolver(
            self.agent, self.config.cqgen_task_config,
            cqgen_task_cache_config)
        
    def get_cache_key(self, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory) -> List[str]:
        str_detailed_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in detailed_dhistory.sequence])
        str_base_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in  base_dhistory.sequence])

        return [self.config.to_str(), str_base_dhistory, str_detailed_dhistory]

    @CacheUtils.cache_method_output
    def generate_question(self, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory) -> str:
        new_question, status = self.cqgen_solver.solve(
            lang=self.config.lang, base_dhistory=base_dhistory,
            detailed_dhistory=detailed_dhistory)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        return new_question