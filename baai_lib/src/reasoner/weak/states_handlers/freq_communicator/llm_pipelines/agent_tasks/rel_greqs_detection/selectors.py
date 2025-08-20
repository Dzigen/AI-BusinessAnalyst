from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import relgfrdetect_custom_formate, relgfrdetect_custom_postprocess
from .v1 import RELGFRDETECT_SUITE_V1

RELGFRDETECT_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/relgfreqs_detect'

AVAILABLE_RELGFRDETECT_TCONFIGS = {
    'v1': RELGFRDETECT_SUITE_V1
}

class AgentRelevantFuncReqGroupsDetectionConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_RELGFRDETECT_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_relgfrdetect_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_RELGFRDETECT_TCONFIGS[base_config_version],
            formate_context_func=relgfrdetect_custom_formate, postprocess_answer_func=relgfrdetect_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(RELGFRDETECT_LOG_PATH))