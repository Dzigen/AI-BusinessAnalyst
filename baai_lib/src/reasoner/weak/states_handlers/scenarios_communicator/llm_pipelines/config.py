from .agent_tasks.ssteps_gen import AgentScenarioStepsGenConfigSelector
from .agent_tasks.stitle_gen import AgentScenarioTitleGenConfigSelector

SGEN_LOG_PATH = "log/reasoner/weak/s_communicator/llm_pipelines/s_generator"

DEFAULT_SSTEPSGEN_TASK_CONFIG = AgentScenarioStepsGenConfigSelector.select(base_config_version='v1')
DEFAULT_STITLEGEN_TASK_CONFIG = AgentScenarioTitleGenConfigSelector.select(base_config_version='v1')