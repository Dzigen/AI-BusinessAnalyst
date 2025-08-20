from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import condqgen_custom_formate, condqgen_custom_postprocess
from .v1 import CONDQGEN_SUITE_V1

CONDQGEN_LOG_PATH = 'log/reasoner/naive/t_clarifier/agent_tasks/cond_q_gen'

AVAILABLE_CONDQGEN_TCONFIGS = {
    'v1': CONDQGEN_SUITE_V1
}

class AgentCondQGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CONDQGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_condqgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CONDQGEN_TCONFIGS[base_config_version],
            formate_context_func=condqgen_custom_formate, postprocess_answer_func=condqgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(CONDQGEN_LOG_PATH))