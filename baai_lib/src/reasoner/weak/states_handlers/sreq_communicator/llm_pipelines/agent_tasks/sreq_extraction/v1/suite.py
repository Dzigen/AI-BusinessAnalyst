from .parsers import sreqextr_custom_parse
from .prompts import RU_SREQEXTR_SYSTEM_PROMPT, RU_SREQEXTR_USER_PROMPT, RU_SREQEXTR_ASSISTANT_PROMPT
from .........utils import AgentTaskSuite

RU_SREQEXTR_SUITE = AgentTaskSuite(
    system_prompt=RU_SREQEXTR_SYSTEM_PROMPT,
    user_prompt=RU_SREQEXTR_USER_PROMPT,
    assistant_prompt=RU_SREQEXTR_ASSISTANT_PROMPT,
    parse_answer_func=sreqextr_custom_parse
)

SREQEXTR_SUITE_V1 = {'ru': RU_SREQEXTR_SUITE, 'en': ...}