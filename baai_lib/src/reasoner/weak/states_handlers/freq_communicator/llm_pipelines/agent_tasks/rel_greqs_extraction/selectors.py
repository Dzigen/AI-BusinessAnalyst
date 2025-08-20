from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import relgfrextr_custom_formate, relgfrextr_custom_postprocess
from .v1 import RELGFREXTR_SUITE_V1

RELGFREXTR_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/relgfreqs_extr'

AVAILABLE_RELGFREXTR_TCONFIGS = {
    'v1': RELGFREXTR_SUITE_V1
}

class AgentRelevantFuncReqGroupsExtractionionConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_RELGFREXTR_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_relgfrextr_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_RELGFREXTR_TCONFIGS[base_config_version],
            formate_context_func=relgfrextr_custom_formate, postprocess_answer_func=relgfrextr_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(RELGFREXTR_LOG_PATH))