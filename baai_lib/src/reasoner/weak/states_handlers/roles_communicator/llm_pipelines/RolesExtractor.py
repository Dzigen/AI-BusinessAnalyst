from dataclasses import dataclass, field
from collections import defaultdict
from ......specification_model.utils import Role
from typing import List, Union
from copy import deepcopy

from .config import DEFAULT_RDETECT_TASK_CONFIG, DEFAULT_TEXTR_TASK_CONFIG, REXTR_LOG_PATH
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.data_structs import create_id
from ......specification_model.utils import Role, UserStory
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class RolesExtractorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    roles_detect_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_RDETECT_TASK_CONFIG)
    roles_extract_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_TEXTR_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'roles_extractor_cache'

    log: Logger = field(default_factory=lambda: Logger(REXTR_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.roles_detect_task_config.version}|{self.roles_extract_task_config.version}|{self.lang}"

class RolesExtractor(CacheUtils):
    def __init__(self, config: RolesExtractorConfig = RolesExtractorConfig(), 
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

        rdetect_task_cache_config = None
        rextract_task_cache_config = None
        if cache_llm_inference:
            rdetect_task_cache_config = deepcopy(cache_kvdriver_config)
            rextract_task_cache_config = deepcopy(cache_kvdriver_config)

        self.rdetect_solver = AgentTaskSolver(
            self.agent, self.config.roles_detect_task_config,
            rdetect_task_cache_config)
        self.rextract_solver = AgentTaskSolver(
            self.agent, self.config.roles_extract_task_config,
            rextract_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose
        
    def get_cache_key(self, task_goal: str, user_stories: List[UserStory]) -> List[str]:
        str_userstories = '|'.join([us_item.statement for us_item in user_stories])
        return [self.config.to_str(), task_goal, str_userstories]

    @CacheUtils.cache_method_output
    def extract(self, task_goal: str, user_stories: List[UserStory]) -> List[Role]:
        if len(user_stories) < 1:
            raise ValueError
        
        unique_roles = defaultdict(list)
        for us_item in user_stories:
            is_us_contain_role, status = self.rdetect_solver.solve(
                lang=self.config.lang, task_goal=task_goal, userstory=us_item.statement)
            if status != ReturnStatus.success:
                raise NotImplementedError
            
            if is_us_contain_role:
                extracted_roles, status = self.rextract_solver.solve(
                    lang=self.config.lang, task_goal=task_goal, userstory=us_item.statement)
                if status != ReturnStatus.success:
                    raise NotImplementedError

                for role in extracted_roles:
                    unique_roles[role].append(us_item.id)

        formated_roles = [Role(id=create_id(role), name=role, related_userstory_ids=related_us_ids) for role, related_us_ids in unique_roles.items()]
        return formated_roles