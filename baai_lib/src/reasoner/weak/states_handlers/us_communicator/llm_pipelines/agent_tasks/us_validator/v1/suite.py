from .........utils import AgentTaskSuite

from .prompts import \
    EN_USVALID_SYSTEM_PROMPT, EN_USVALID_USER_PROMPT, EN_USVALID_ASSISTANT_PROMPT,\
        RU_USVALID_SYSTEM_PROMPT, RU_USVALID_USER_PROMPT, RU_USVALID_ASSISTANT_PROMPT

from .parsers import usvalid_custom_parse

EN_USVALID_SUITE = AgentTaskSuite(
    system_prompt=EN_USVALID_SYSTEM_PROMPT,
    user_prompt=EN_USVALID_USER_PROMPT,
    assistant_prompt=EN_USVALID_ASSISTANT_PROMPT,
    parse_answer_func=usvalid_custom_parse
)

RU_USVALID_SUITE = AgentTaskSuite(
    system_prompt=RU_USVALID_SYSTEM_PROMPT,
    user_prompt=RU_USVALID_USER_PROMPT,
    assistant_prompt=RU_USVALID_ASSISTANT_PROMPT,
    parse_answer_func=usvalid_custom_parse
)

USVALID_SUITE_V1 = {'ru': RU_USVALID_SUITE, 'en': EN_USVALID_SUITE}