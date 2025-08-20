from .........utils import AgentTaskSuite

from .prompts import \
    EN_TCLS_SYSTEM_PROMPT, EN_TCLS_USER_PROMPT, EN_TCLS_ASSISTANT_PROMPT,\
        RU_TCLS_SYSTEM_PROMPT, RU_TCLS_USER_PROMPT, RU_TCLS_ASSISTANT_PROMPT

from .parsers import tcls_custom_parse

EN_TCLS_SUITE = AgentTaskSuite(
    system_prompt=EN_TCLS_SYSTEM_PROMPT,
    user_prompt=EN_TCLS_USER_PROMPT,
    assistant_prompt=EN_TCLS_ASSISTANT_PROMPT,
    parse_answer_func=tcls_custom_parse
)

RU_TCLS_SUITE = AgentTaskSuite(
    system_prompt=RU_TCLS_SYSTEM_PROMPT,
    user_prompt=RU_TCLS_USER_PROMPT,
    assistant_prompt=RU_TCLS_ASSISTANT_PROMPT,
    parse_answer_func=tcls_custom_parse
)

TCLS_SUITE_V1 = {'ru': RU_TCLS_SUITE, 'en': EN_TCLS_SUITE}