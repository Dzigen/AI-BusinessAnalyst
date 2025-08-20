from dataclasses import dataclass, field
from typing import List, Union
from time import time
from copy import deepcopy

from .config import DEFAULT_STITLEGEN_TASK_CONFIG, DEFAULT_SSTEPSGEN_TASK_CONFIG, SGEN_LOG_PATH
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.data_structs import create_id
from ......specification_model.utils import UserStory, Scenario
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class ScenariosGeneratorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    stitle_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_STITLEGEN_TASK_CONFIG)
    ssteps_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_SSTEPSGEN_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'scenarios_generator_cache'

    log: Logger = field(default_factory=lambda: Logger(SGEN_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.ssteps_gen_task_config.version}|{self.stitle_gen_task_config.version}|{self.lang}"

class ScenariosGenerator(CacheUtils):
    def __init__(self, config: ScenariosGeneratorConfig = ScenariosGeneratorConfig(), 
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

        ssgen_task_cache_config = None
        stgen_task_cache_config = None
        if cache_llm_inference:
            ssgen_task_cache_config = deepcopy(cache_kvdriver_config)
            stgen_task_cache_config = deepcopy(cache_kvdriver_config)

        self.stgen_solver = AgentTaskSolver(
            self.agent, self.config.stitle_gen_task_config,
            stgen_task_cache_config)
        self.ssgen_solver = AgentTaskSolver(
            self.agent, self.config.ssteps_gen_task_config,
            ssgen_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose

    def get_cache_key(self, task_goal: str, user_story: UserStory, accepted_scenarios: List[Scenario], 
                      declined_scenarios: List[Scenario]) -> List[str]:
        str_accepted_s = '|'.join([scenario.formate_to_str() for scenario in accepted_scenarios])
        str_declined_s = '|'.join([scenario.formate_to_str() for scenario in declined_scenarios])

        return [self.config.to_str(), task_goal, user_story.statement, str_accepted_s, str_declined_s]

    @CacheUtils.cache_method_output
    def generate(self, task_goal: str, user_story: UserStory, accepted_scenarios: List[Scenario], 
                 declined_scenarios: List[Scenario]) -> Scenario:        
        s_title, status = self.stgen_solver.solve(lang=self.config.lang, task_goal=task_goal, 
                                user_story=user_story.statement, accepted_scenarios=accepted_scenarios,
                                declined_scenarios=declined_scenarios)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        s_steps, status = self.ssgen_solver.solve(lang=self.config.lang, task_goal=task_goal, 
                                user_story=user_story.statement, scenario_title=s_title)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        new_scenario = Scenario(id=create_id(f"{s_title}\n{s_steps}"), title=s_title,
            steps=s_steps, related_userstory_ids=[user_story.id])
        return new_scenario