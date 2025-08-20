from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import intgrsumm_custom_formate, intgrsumm_custom_postprocess
from .v1 import INTGRSUMM_SUITE_V1

INTGRSUMM_LOG_PATH = 'log/reasoner/weak/taskg_communicator/llm_pipelines/agent_tasks/intgr_summ'

AVAILABLE_INTGRSUMM_TCONFIGS = {
    'v1': INTGRSUMM_SUITE_V1,
    'v2': ... 
}

class AgentIntgrSummarisationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_INTGRSUMM_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_intgrsumm_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_INTGRSUMM_TCONFIGS[base_config_version],
            formate_context_func=intgrsumm_custom_formate, postprocess_answer_func=intgrsumm_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(INTGRSUMM_LOG_PATH))