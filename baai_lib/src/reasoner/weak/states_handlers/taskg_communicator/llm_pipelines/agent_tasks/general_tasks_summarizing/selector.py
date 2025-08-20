from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import gtsumm_custom_formate, gtsumm_custom_postprocess
from .v1 import GTSUMM_SUITE_V1

GTSUMM_LOG_PATH = 'log/reasoner/weak/taskg_communicator/llm_pipelines/agent_tasks/gt_summ'

AVAILABLE_GTSUMM_TCONFIGS = {
    'v1': GTSUMM_SUITE_V1,
    'v2': ... 
}

class AgentGTSummarisationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_GTSUMM_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="agent_gtsumm_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_GTSUMM_TCONFIGS[base_config_version],
            formate_context_func=gtsumm_custom_formate, postprocess_answer_func=gtsumm_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(GTSUMM_LOG_PATH))