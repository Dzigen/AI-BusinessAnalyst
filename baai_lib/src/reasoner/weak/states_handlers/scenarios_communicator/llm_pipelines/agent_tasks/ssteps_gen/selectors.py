from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import sstepsgen_custom_formate, sstepsgen_custom_postprocess
from .v1 import SSTEPSGEN_SUITE_V1

SSTEPSGEN_LOG_PATH = 'log/reasoner/weak/s_communicator/llm_pipelines/agent_tasks/ssteps_gen'

AVAILABLE_SSTEPSGEN_TCONFIGS = {
    'v1': SSTEPSGEN_SUITE_V1
}

class AgentScenarioStepsGenConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_SSTEPSGEN_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_sstepsgen_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_SSTEPSGEN_TCONFIGS[base_config_version],
            formate_context_func=sstepsgen_custom_formate, postprocess_answer_func=sstepsgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(SSTEPSGEN_LOG_PATH))