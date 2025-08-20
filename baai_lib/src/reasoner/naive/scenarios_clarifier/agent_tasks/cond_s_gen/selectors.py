from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import condsgen_custom_formate, condsgen_custom_postprocess
from .v1 import CONDSGEN_SUITE_V1

condsgen_LOG_PATH = 'log/reasoner/naive/s_extractor/agent_tasks/cond_s_gen'

AVAILABLE_CONDSGEN_TCONFIGS = {
    'v1': CONDSGEN_SUITE_V1
}

class AgentCondSGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CONDSGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_condsgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CONDSGEN_TCONFIGS[base_config_version],
            formate_context_func=condsgen_custom_formate, postprocess_answer_func=condsgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(condsgen_LOG_PATH))