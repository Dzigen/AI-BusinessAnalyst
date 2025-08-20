from ......utils import AgentTaskSolverConfig, Logger
from .general_parsers import cfgen_custom_formate, cfgen_custom_postprocess
from .v1 import CFG_SUITE_V1

CFG_LOG_PATH = 'log/reasoner/naive/freq_extractor/agent_tasks/cond_f_gen'

AVAILABLE_CFG_TCONFIGS = {
    'v1': CFG_SUITE_V1
}

class AgentCFGConfigSelector:
    @staticmethod
    def get_available_configs():
        return AVAILABLE_CFG_TCONFIGS

    @staticmethod
    def select(base_config_version:str = 'v1', cache_table_name:str="nr_agent_cg_task_cache") -> AgentTaskSolverConfig:
        return AgentTaskSolverConfig(
            version=base_config_version,
            suites=AVAILABLE_CFG_TCONFIGS[base_config_version],
            formate_context_func=cfgen_custom_formate, postprocess_answer_func=cfgen_custom_postprocess,
            cache_table_name=cache_table_name,
            log=Logger(CFG_LOG_PATH))