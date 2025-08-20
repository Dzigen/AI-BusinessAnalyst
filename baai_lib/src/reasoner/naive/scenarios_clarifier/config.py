from .agent_tasks.cond_s_gen import AgentCondSGenConfigSelector
from ..utils import NaiveStateSignal
from ...utils import SignalInfo

DEFAULT_CSG_TASK_CONFIG =  AgentCondSGenConfigSelector.select(base_config_version='v1')

BA_SCENARIOS_CLARIFYING_NOTICE = "Начнём уточнять возможные сценарии по каждой user-истории."
BA_FIXING_USERSTORY_NOTICE = "Сейчас будем уточнять сценарии для user-истории {us_id}: {us_text}"
BA_SCENARIOS_LIMIT_NOTICE = "Был достигнут лимит по возможному количеству сценариев для одной user-истории"
BA_ALLSTORIES_CLARIFIED_NOTICE = "Сценарии для всех user-историй уточнены"


SC_STATE_SIGNALSINFO = {
    'next_scenario': SignalInfo(
        signal=NaiveStateSignal.continue_operation,
        shortcut="Следующий сценарий"
    )
}