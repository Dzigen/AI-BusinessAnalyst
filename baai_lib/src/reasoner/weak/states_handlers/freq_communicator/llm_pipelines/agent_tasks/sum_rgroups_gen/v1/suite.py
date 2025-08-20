from .........utils import AgentTaskSuite

from .parsers import sfrggen_custom_parse

from .prompts import RU_SFRGGEN_SYSTEM_PROMPT, RU_SFRGGEN_USER_PROMPT, RU_SFRGGEN_ASSISTANT_PROMPT

RU_SFRGGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_SFRGGEN_SYSTEM_PROMPT,
    user_prompt=RU_SFRGGEN_USER_PROMPT,
    assistant_prompt=RU_SFRGGEN_ASSISTANT_PROMPT,
    parse_answer_func=sfrggen_custom_parse
)

SFRGGEN_SUITE_V1 = {'ru': RU_SFRGGEN_SUITE, 'en': ...}