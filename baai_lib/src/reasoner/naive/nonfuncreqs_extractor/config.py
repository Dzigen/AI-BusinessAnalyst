from .agent_tasks.cond_nonfreq_gen import AgentCNonFGConfigSelector

DEFAULT_CNONFG_TASK_CONFIG = AgentCNonFGConfigSelector.select(base_config_version='v1')

BA_NONFUNCREQ_EXTRACT_NOTICE = "Извлекаем нефункциональные требования"
BA_EXTRACTED_NONFREQ_NOTICE = "В вашем описании предметной области было найдено {nonfreq_amount} нефункциональных требований."

