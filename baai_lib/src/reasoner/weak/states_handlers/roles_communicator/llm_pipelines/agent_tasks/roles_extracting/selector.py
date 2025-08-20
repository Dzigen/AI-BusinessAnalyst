from .general_parsers import rextr_custom_formate, rextr_custom_postprocess
from .v1 import REXTR_SUITE_V1
from ........utils import AgentTaskSolverConfig, Logger


REXTR_LOG_PATH = 'log/reasoner/weak/r_communicator/llm_pipelines/agent_tasks/r_extr'

AVAILABLE_REXTR_TCONFIGS = {
    'v1': REXTR_SUITE_V1,
    'v2': ... 
}

class AgentRolesExtrTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_REXTR_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_rextr_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_REXTR_TCONFIGS[base_config_version],
            formate_context_func=rextr_custom_formate, postprocess_answer_func=rextr_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(REXTR_LOG_PATH))