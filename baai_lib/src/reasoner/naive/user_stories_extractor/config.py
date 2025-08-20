from .agent_tasks.cond_us_gen import AgentCondUSGenConfigSelector

DEFAULT_CUSG_TASK_CONFIG =  AgentCondUSGenConfigSelector.select(base_config_version='v1')

BA_USERSTORIES_SEARCH_NOTICE = "Ищем user-истории в вашем варианте описания предметной области."
BA_EXTRACTED_USERSTORIES_NOTICE = "В вашем описании предметной области было найдено {extracted_us_amount} user-историй."