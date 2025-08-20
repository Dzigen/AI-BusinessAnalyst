from dataclasses import dataclass, field
from typing import Union, List
from copy import deepcopy

from .config import DEFAULT_USGEN_TASK_CONFIG, DEFAULT_USVALID_TASK_CONFIG, USEXTR_LOG_PATH
from .....utils import DialogueHistory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......specification_model.utils import UserStory
from ......db_drivers.kv_driver import KeyValueDriverConfig
from ......agents import AgentDriverConfig, AgentDriver
from ......utils import Logger, AgentTaskSolver, AgentTaskSolverConfig, ReturnStatus
from ......utils.cache_kv import CacheKV, CacheUtils

@dataclass
class UserStoriesExtractorConfig:
    lang: str = 'ru'
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    userstory_gen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_USGEN_TASK_CONFIG)
    userstory_valid_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_USVALID_TASK_CONFIG)
    cache_table_name: Union[str, None] = 'us_extractor_cache'

    log: Logger = field(default_factory=lambda: Logger(USEXTR_LOG_PATH))
    verbose: bool = False

    def to_str(self):
        return f"{self.adriver_config.to_str()}|{self.userstory_gen_task_config.version}|{self.userstory_valid_task_config.version}|{self.lang}"


class UserStoriesExtractor(CacheUtils):
    
    def __init__(self, config: UserStoriesExtractorConfig = UserStoriesExtractorConfig(), 
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

        usgen_task_cache_config = None
        usvalid_task_cache_config = None
        if cache_llm_inference:
            usgen_task_cache_config = deepcopy(cache_kvdriver_config)
            usvalid_task_cache_config = deepcopy(cache_kvdriver_config)

        self.usgen_solver = AgentTaskSolver(
            self.agent, self.config.userstory_gen_task_config,
            usgen_task_cache_config)
        self.usvalid_solver = AgentTaskSolver(
            self.agent, self.config.userstory_valid_task_config,
            usvalid_task_cache_config)
        
        self.log = config.log
        self.verbose = config.verbose
        
    def is_userstory_valid(self, task_goal: str, user_story: str) -> bool:
        valid_flag, status = self.usvalid_solver.solve(lang=self.config.lang, task_goal=task_goal, user_story=user_story)
        if status != ReturnStatus.success:
            raise NotImplementedError
        return valid_flag

    def get_cache_key(self, task_goal: str, base_dhistory: DialogueHistory, 
                      detailed_dhistory: DialogueHistory, us_limit: int) -> List[str]:
        str_detail_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in detailed_dhistory.sequence])
        str_base_dhistory = '\n'.join([f"{item.role}: {item.text}" for item in base_dhistory.sequence])

        return [self.config.to_str(), str_base_dhistory, str_detail_dhistory, task_goal, str(us_limit)]

    @CacheUtils.cache_method_output
    def extract_userstories(self, task_goal: str, base_dhistory: DialogueHistory, 
                            detailed_dhistory: DialogueHistory, us_limit: int = -1) -> List[UserStory]:
        if us_limit == 0:
            raise ValueError
        
        user_stories, status = self.usgen_solver.solve(
            lang=self.config.lang, task_goal=task_goal, base_dhistory=base_dhistory, detailed_dhistory=detailed_dhistory, us_limit=us_limit)
        if status != ReturnStatus.success:
            raise NotImplementedError
        
        if us_limit > 0:
            user_stories = user_stories[:us_limit]
        
        #validated_userstories = [user_story for user_story in user_stories if self.is_userstory_valid(task_goal, user_story.statement)]
        return user_stories