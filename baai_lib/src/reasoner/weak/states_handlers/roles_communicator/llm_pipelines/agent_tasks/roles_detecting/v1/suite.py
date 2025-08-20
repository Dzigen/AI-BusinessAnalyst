from .........utils import AgentTaskSuite

from .prompts import \
    EN_RDETECT_SYSTEM_PROMPT, EN_RDETECT_USER_PROMPT, EN_RDETECT_ASSISTANT_PROMPT,\
        RU_RDETECT_SYSTEM_PROMPT, RU_RDETECT_USER_PROMPT, RU_RDETECT_ASSISTANT_PROMPT

from .parsers import rdetect_custom_parse

EN_RDETECT_SUITE = AgentTaskSuite(
    system_prompt=EN_RDETECT_SYSTEM_PROMPT,
    user_prompt=EN_RDETECT_USER_PROMPT,
    assistant_prompt=EN_RDETECT_ASSISTANT_PROMPT,
    parse_answer_func=rdetect_custom_parse
)

RU_RDETECT_SUITE = AgentTaskSuite(
    system_prompt=RU_RDETECT_SYSTEM_PROMPT,
    user_prompt=RU_RDETECT_USER_PROMPT,
    assistant_prompt=RU_RDETECT_ASSISTANT_PROMPT,
    parse_answer_func=rdetect_custom_parse
)

RDETECT_SUITE_V1 = {'ru': RU_RDETECT_SUITE, 'en': EN_RDETECT_SUITE}