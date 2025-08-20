from .agent_tasks.sreq_extraction import AgentSysReqExtractionConfigSelector

SREQ_LOG_PATH = "log/reasoner/weak/sreq_communicator/llm_pipelines/sysreq_extractor"

DEFAULT_SREQEXTR_TASK_CONFIG = AgentSysReqExtractionConfigSelector.select(base_config_version='v1')