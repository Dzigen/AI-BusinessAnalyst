from ........utils import AgentTaskSolverConfig, Logger
from ........db_drivers.kv_driver import KeyValueDriverConfig
from .general_parsers import usgen_custom_formate, usgen_custom_postprocess
from .v1 import USGEN_SUITE_V1

USGEN_LOG_PATH = 'log/reasoner/weak/us_communicator/llm_pipelines/agent_tasks/us_gen'

AVAILABLE_USGEN_TCONFIGS = {
    'v1': USGEN_SUITE_V1,
    'v2': ... 
}

class AgentUSGenerationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_USGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_usgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_USGEN_TCONFIGS[base_config_version],
            formate_context_func=usgen_custom_formate, postprocess_answer_func=usgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(USGEN_LOG_PATH))