from .........utils import AgentTaskSuite

from .parsers import relgfrextr_custom_parse

from .prompts import RU_RELGFREXTR_SYSTEM_PROMPT, RU_RELGFREXTR_USER_PROMPT, RU_RELGFREXTR_ASSISTANT_PROMPT

RU_RELGFREXTR_SUITE = AgentTaskSuite(
    system_prompt=RU_RELGFREXTR_SYSTEM_PROMPT,
    user_prompt=RU_RELGFREXTR_USER_PROMPT,
    assistant_prompt=RU_RELGFREXTR_ASSISTANT_PROMPT,
    parse_answer_func=relgfrextr_custom_parse
)

RELGFREXTR_SUITE_V1 = {'ru': RU_RELGFREXTR_SUITE, 'en': ...}