from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import bfrggen_custom_formate, bfrggen_custom_postprocess
from .v1 import BFRGGEN_SUITE_V1

BFRGGEN_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/bfrg_gen'

AVAILABLE_BFRGGEN_TCONFIGS = {
    'v1': BFRGGEN_SUITE_V1
}

class AgentBaseFRGroupsGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_BFRGGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_bfrggen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_BFRGGEN_TCONFIGS[base_config_version],
            formate_context_func=bfrggen_custom_formate, postprocess_answer_func=bfrggen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(BFRGGEN_LOG_PATH))