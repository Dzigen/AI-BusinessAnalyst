from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import sreqextr_custom_formate, sreqextr_custom_postprocess
from .v1 import SREQEXTR_SUITE_V1

SREQEXTR_LOG_PATH = 'log/reasoner/weak/sreq_communicator/llm_pipelines/agent_tasks/sreq_extr'

AVAILABLE_SREQEXTR_TCONFIGS = {
    'v1': SREQEXTR_SUITE_V1
}

class AgentSysReqExtractionConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_SREQEXTR_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_sreqextr_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_SREQEXTR_TCONFIGS[base_config_version],
            formate_context_func=sreqextr_custom_formate, postprocess_answer_func=sreqextr_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(SREQEXTR_LOG_PATH))