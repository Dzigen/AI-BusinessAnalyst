from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import condusgen_custom_formate, condusgen_custom_postprocess
from .v1 import CONDUSGEN_SUITE_V1

CONDUSGEN_LOG_PATH = 'log/reasoner/naive/us_extractor/agent_tasks/cond_us_gen'

AVAILABLE_CONDUSGEN_TCONFIGS = {
    'v1': CONDUSGEN_SUITE_V1
}

class AgentCondUSGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CONDUSGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_condusgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CONDUSGEN_TCONFIGS[base_config_version],
            formate_context_func=condusgen_custom_formate, postprocess_answer_func=condusgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(CONDUSGEN_LOG_PATH))