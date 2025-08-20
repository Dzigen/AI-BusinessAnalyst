from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import sfrggen_custom_formate, sfrggen_custom_postprocess
from .v1 import SFRGGEN_SUITE_V1

SFRGGEN_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/sfrg_gen'

AVAILABLE_SFRGGEN_TCONFIGS = {
    'v1': SFRGGEN_SUITE_V1
}

class AgentSummFRGroupsGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_SFRGGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_sfrggen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_SFRGGEN_TCONFIGS[base_config_version],
            formate_context_func=sfrggen_custom_formate, postprocess_answer_func=sfrggen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(SFRGGEN_LOG_PATH))