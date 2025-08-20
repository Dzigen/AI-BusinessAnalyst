from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import frestrgen_custom_formate, frestrgen_custom_postprocess
from .v1 import FRESTRGEN_SUITE_V1

FRESTRGEN_LOG_PATH = 'log/reasoner/weak/frestr_communicator/llm_pipelines/agent_tasks/frestr_gen'

AVAILABLE_FRESTRGEN_TCONFIGS = {
    'v1': FRESTRGEN_SUITE_V1
}

class AgentFuncRestrGenerationConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_FRESTRGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_frestrgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_FRESTRGEN_TCONFIGS[base_config_version],
            formate_context_func=frestrgen_custom_formate, postprocess_answer_func=frestrgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(FRESTRGEN_LOG_PATH))