from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import stitlegen_custom_formate, stitlegen_custom_postprocess
from .v1 import STITLEGEN_SUITE_V1

STITLEGEN_LOG_PATH = 'log/reasoner/weak/s_communicator/llm_pipelines/agent_tasks/stitle_gen'

AVAILABLE_STITLEGEN_TCONFIGS = {
    'v1': STITLEGEN_SUITE_V1
}

class AgentScenarioTitleGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_STITLEGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_stitlegen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_STITLEGEN_TCONFIGS[base_config_version],
            formate_context_func=stitlegen_custom_formate, postprocess_answer_func=stitlegen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(STITLEGEN_LOG_PATH))