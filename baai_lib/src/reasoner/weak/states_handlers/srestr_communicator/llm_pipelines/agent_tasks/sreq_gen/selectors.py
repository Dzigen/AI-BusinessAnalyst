from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import srestrgen_custom_formate, srestrgen_custom_postprocess
from .v1 import SRESTRGEN_SUITE_V1

SRESTRGEN_LOG_PATH = 'log/reasoner/weak/srestr_communicator/llm_pipelines/agent_tasks/srestr_gen'

AVAILABLE_SRESTRGEN_TCONFIGS = {
    'v1': SRESTRGEN_SUITE_V1
}

class AgentSysRestrGenerationConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_SRESTRGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_srestrgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_SRESTRGEN_TCONFIGS[base_config_version],
            formate_context_func=srestrgen_custom_formate, postprocess_answer_func=srestrgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(SRESTRGEN_LOG_PATH))