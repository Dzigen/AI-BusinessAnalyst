from ........utils import AgentTaskSolverConfig, Logger
from ........db_drivers.kv_driver import KeyValueDriverConfig
from .general_parsers import usvalid_custom_formate, usvalid_custom_postprocess
from .v1 import USVALID_SUITE_V1

USVALID_LOG_PATH = 'log/reasoner/weak/us_communicator/llm_pipelines/agent_tasks/us_valid'

AVAILABLE_USVALID_TCONFIGS = {
    'v1': USVALID_SUITE_V1,
    'v2': ... 
}

class AgentUSValidationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_USVALID_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_usvalid_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_USVALID_TCONFIGS[base_config_version],
            formate_context_func=usvalid_custom_formate, postprocess_answer_func=usvalid_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(USVALID_LOG_PATH))