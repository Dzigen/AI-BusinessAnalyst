from .agent_tasks.us_generator import AgentUSGenerationTaskConfigSelector
from .agent_tasks.us_validator import AgentUSValidationTaskConfigSelector


USEXTR_LOG_PATH = 'log/reasoner/weak/us_communicator/llm_pipelines/us_extractor'

DEFAULT_USGEN_TASK_CONFIG = AgentUSGenerationTaskConfigSelector.select(base_config_version='v1')
DEFAULT_USVALID_TASK_CONFIG = AgentUSValidationTaskConfigSelector.select(base_config_version='v1')