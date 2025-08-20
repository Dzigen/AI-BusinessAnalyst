from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import condrgen_custom_formate, condrgen_custom_postprocess
from .v1 import CONDRGEN_SUITE_V1

CONDRGEN_LOG_PATH = 'log/reasoner/naive/r_extractor/agent_tasks/cond_r_gen'

AVAILABLE_CONDRGEN_TCONFIGS = {
    'v1': CONDRGEN_SUITE_V1
}

class AgentCondRGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CONDRGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_condrgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CONDRGEN_TCONFIGS[base_config_version],
            formate_context_func=condrgen_custom_formate, postprocess_answer_func=condrgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(CONDRGEN_LOG_PATH))