from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import gfrreform_custom_formate, gfrreform_custom_postprocess
from .v1 import GFRREFORM_SUITE_V1

GFRREFORM_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/gfreqs_reform'

AVAILABLE_GFRREFORM_TCONFIGS = {
    'v1': GFRREFORM_SUITE_V1
}

class AgentFuncReqGroupReformConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_GFRREFORM_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_gfrreform_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_GFRREFORM_TCONFIGS[base_config_version],
            formate_context_func=gfrreform_custom_formate, postprocess_answer_func=gfrreform_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(GFRREFORM_LOG_PATH))