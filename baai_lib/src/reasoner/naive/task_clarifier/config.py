from .agent_tasks.cond_q_gen import AgentCondQGenConfigSelector

DEFAULT_CQG_TASK_CONFIG =  AgentCondQGenConfigSelector.select(base_config_version='v1')

BA_TASKCLAR_NOTICE = "Начинаю уточнять информацию по вашей предметной области"
BA_MESSAGE_WITH_STOP_QCLARIFICATION_NOTICE = "Завершаем уточнение предметной области проекта."