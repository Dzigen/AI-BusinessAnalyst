from .agent_tasks.sreq_gen import AgentSysRestrGenerationConfigSelector

SRESTR_LOG_PATH = "log/reasoner/weak/srestr_communicator/llm_pipelines/sysrstr_generator"

DEFAULT_SRESTRGEN_TASK_CONFIG = AgentSysRestrGenerationConfigSelector.select(base_config_version='v1')