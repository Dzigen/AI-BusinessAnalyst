from .........utils import AgentTaskSuite

from .prompts import \
    EN_USGEN_SYSTEM_PROMPT, EN_USGEN_USER_PROMPT, EN_USGEN_ASSISTANT_PROMPT,\
        RU_USGEN_SYSTEM_PROMPT, RU_USGEN_USER_PROMPT, RU_USGEN_ASSISTANT_PROMPT

from .parsers import usgen_custom_parse

EN_USGEN_SUITE = AgentTaskSuite(
    system_prompt=EN_USGEN_SYSTEM_PROMPT,
    user_prompt=EN_USGEN_USER_PROMPT,
    assistant_prompt=EN_USGEN_ASSISTANT_PROMPT,
    parse_answer_func=usgen_custom_parse
)

RU_USGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_USGEN_SYSTEM_PROMPT,
    user_prompt=RU_USGEN_USER_PROMPT,
    assistant_prompt=RU_USGEN_ASSISTANT_PROMPT,
    parse_answer_func=usgen_custom_parse
)

USGEN_SUITE_V1 = {'ru': RU_USGEN_SUITE, 'en': EN_USGEN_SUITE}