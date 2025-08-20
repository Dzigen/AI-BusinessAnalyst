from ........utils import AgentTaskSolverConfig, Logger
from .general_parsers import freqextr_custom_formate, freqextr_custom_postprocess
from .v1 import FREQEXTR_SUITE_V1

FREQEXTR_LOG_PATH = 'log/reasoner/weak/freq_communicator/llm_pipelines/agent_tasks/freq_extr'

AVAILABLE_FREQEXTR_TCONFIGS = {
    'v1': FREQEXTR_SUITE_V1
}

class AgentFuncReqExtrConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_FREQEXTR_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="agent_freqextr_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_FREQEXTR_TCONFIGS[base_config_version],
            formate_context_func=freqextr_custom_formate, postprocess_answer_func=freqextr_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(FREQEXTR_LOG_PATH))