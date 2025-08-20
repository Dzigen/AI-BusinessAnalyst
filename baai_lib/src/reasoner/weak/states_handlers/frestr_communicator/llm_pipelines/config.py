from .agent_tasks.frestr_gen import AgentFuncRestrGenerationConfigSelector

FRESTR_LOG_PATH = "log/reasoner/weak/frestr_communicator/llm_pipelines/frestr_generator"

DEFAULT_FRESTRGEN_TASK_CONFIG = AgentFuncRestrGenerationConfigSelector.select(base_config_version='v1')