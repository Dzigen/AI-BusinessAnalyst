from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import tcls_custom_formate, tcls_custom_postprocess
from .v1 import TCLS_SUITE_V1

TCLS_LOG_PATH = 'log/reasoner/weak/taskg_communicator/llm_pipelines/agent_tasks/t_cls'

AVAILABLE_TCLS_TCONFIGS = {
    'v1': TCLS_SUITE_V1,
    'v2': ... 
}

class AgentTaskClassificationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_TCLS_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="qa_agent_tcls_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_TCLS_TCONFIGS[base_config_version],
            formate_context_func=tcls_custom_formate, postprocess_answer_func=tcls_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(TCLS_LOG_PATH))