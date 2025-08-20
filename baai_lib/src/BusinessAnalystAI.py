from dataclasses import dataclass, field
from typing import Union, Dict

from .reasoner import NaiveBAReasonerConfig, WeakBAReasonerConfig, AVAILABLE_BA_REASONERS
from .specification_model import  ReqSpecificationModel, ReqSpecificationModelConfig
from .utils import Logger
from .db_drivers.kv_driver import KeyValueDriverConfig 

BAAI_MAIN_LOG_PATH = "log/main"

@dataclass
class BusinessAnalystAIConfig:
    reasoner_name: str = "naive"
    reasoner_config: Union[NaiveBAReasonerConfig, WeakBAReasonerConfig] = field(default_factory=lambda: NaiveBAReasonerConfig())
    reqspec_model_config: ReqSpecificationModelConfig = field(default_factory=lambda: ReqSpecificationModelConfig())

    log: Logger = field(default_factory=lambda: Logger(BAAI_MAIN_LOG_PATH))
    verbose: bool = False

class BusinessAnalystAI:
    
    def __init__(self, config: BusinessAnalystAIConfig = BusinessAnalystAIConfig(), 
                 cache_kvdriver_config: KeyValueDriverConfig = KeyValueDriverConfig()):
        self.config = config
        self.reqspec_model = ReqSpecificationModel(self.config.reqspec_model_config)
        self.reasoner = AVAILABLE_BA_REASONERS[self.config.reasoner_name](
            self.reqspec_model, self.config.reasoner_config, cache_kvdriver_config)

    def get_task_description(self, format: str = 'markdown') -> Union[Dict[str,Union[Dict[str,str], str]],str]:
        return self.reasoner.get_task_description(format=format)

    def reset(self):
        self.reqspec_model.clear()
        self.reasoner.reset(self.reqspec_model)
