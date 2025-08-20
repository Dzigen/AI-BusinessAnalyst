from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import stsumm_custom_formate, stsumm_custom_postprocess
from .v1 import STSUMM_SUITE_V1

STSUMM_LOG_PATH = 'log/reasoner/weak/taskg_communicator/llm_pipelines/agent_tasks/st_summ'

AVAILABLE_STSUMM_TCONFIGS = {
    'v1': STSUMM_SUITE_V1,
    'v2': ... 
}

class AgentSTSummarisationTaskConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_STSUMM_TCONFIGS

    @staticmethod
    def select(base_config_version:str='v1', cache_table_name:str="wr_agent_stsumm_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_STSUMM_TCONFIGS[base_config_version],
            formate_context_func=stsumm_custom_formate, postprocess_answer_func=stsumm_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(STSUMM_LOG_PATH))