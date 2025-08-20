from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import rdetect_custom_formate, rdetect_custom_postprocess
from .v1 import RDETECT_SUITE_V1

RDETECT_LOG_PATH = 'log/reasoner/weak/r_communicator/llm_pipelines/agent_tasks/r_detect'

AVAILABLE_RDETECT_TCONFIGS = {
    'v1': RDETECT_SUITE_V1,
    'v2': ... 
}

class AgentRolesDetectrTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_RDETECT_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_rdetect_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_RDETECT_TCONFIGS[base_config_version],
            formate_context_func=rdetect_custom_formate, postprocess_answer_func=rdetect_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(RDETECT_LOG_PATH))