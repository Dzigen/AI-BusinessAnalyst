from .agent_tasks.cond_freq_gen import AgentCFGConfigSelector

DEFAULT_CFG_TASK_CONFIG = AgentCFGConfigSelector.select(base_config_version='v1')

BA_FUNCREQ_EXTRACT_NOTICE = "Извлекаю функциональные требования"
BA_EXTRACTED_FREQ_NOTICE = "В вашем описании предметной области было найдено {freq_amount} функциональных требований."