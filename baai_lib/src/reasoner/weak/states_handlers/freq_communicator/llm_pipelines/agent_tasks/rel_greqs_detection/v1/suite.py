from .........utils import AgentTaskSuite

from .parsers import relgfrdetect_custom_parse

from .prompts import RU_RELGFRDETECT_SYSTEM_PROMPT, RU_RELGFRDETECT_USER_PROMPT, RU_RELGFRDETECT_ASSISTANT_PROMPT

RU_RELGFRDETECT_SUITE = AgentTaskSuite(
    system_prompt=RU_RELGFRDETECT_SYSTEM_PROMPT,
    user_prompt=RU_RELGFRDETECT_USER_PROMPT,
    assistant_prompt=RU_RELGFRDETECT_ASSISTANT_PROMPT,
    parse_answer_func=relgfrdetect_custom_parse
)

RELGFRDETECT_SUITE_V1 = {'ru': RU_RELGFRDETECT_SUITE, 'en': ...}