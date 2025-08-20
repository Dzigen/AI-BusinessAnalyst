from .agent_tasks.cond_r_gen import AgentCondRGenConfigSelector

DEFAULT_CRG_TASK_CONFIG = AgentCondRGenConfigSelector.select(base_config_version='v1')

BA_ROLES_EXTRACTING_NOTICE = "Извлекаем роли."
BA_EXTRACTED_ROLES_NOTICE = "В вашем описании предметной области было найдено {extracted_r_amount} ролей."