from .agent_tasks.clarify_question_gen import AgentClarifyQuestionGenConfigSelector

BPCLARIFIER_LOG_PATH = 'log/reasoner/weak/bp_communicator/llm_pipelines/clarify_q_gen'

DEFAULT_BPCQGEN_TASK_CONFIG = AgentClarifyQuestionGenConfigSelector.select(base_config_version='v1')