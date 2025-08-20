from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import cnonfgen_custom_formate, cnonfgen_custom_postprocess
from .v1 import CNONFG_SUITE_V1

CNONFG_LOG_PATH = 'log/reasoner/naive/nfreq_extractor/agent_tasks/cond_nonf_gen'

AVAILABLE_CNONFG_TCONFIGS = {
    'v1': CNONFG_SUITE_V1
}

class AgentCNonFGConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CNONFG_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_cnonfg_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CNONFG_TCONFIGS[base_config_version],
            formate_context_func=cnonfgen_custom_formate, postprocess_answer_func=cnonfgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(CNONFG_LOG_PATH))