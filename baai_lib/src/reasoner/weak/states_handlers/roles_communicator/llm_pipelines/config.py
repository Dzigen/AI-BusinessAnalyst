from .agent_tasks.roles_detecting import AgentRolesDetectrTaskConfigSelector
from .agent_tasks.roles_extracting import AgentRolesExtrTaskConfigSelector

REXTR_LOG_PATH = 'log/reasoner/weak/r_communicator/llm_pipelines/r_extractor'

DEFAULT_RDETECT_TASK_CONFIG = AgentRolesDetectrTaskConfigSelector.select(base_config_version='v1')
DEFAULT_TEXTR_TASK_CONFIG = AgentRolesExtrTaskConfigSelector.select(base_config_version='v1')