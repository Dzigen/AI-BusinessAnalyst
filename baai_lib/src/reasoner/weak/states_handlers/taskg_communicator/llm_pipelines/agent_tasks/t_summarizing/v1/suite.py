from .........utils import AgentTaskSuite

from .prompts import \
    EN_STSUMM_SYSTEM_PROMPT, EN_STSUMM_USER_PROMPT, EN_STSUMM_ASSISTANT_PROMPT,\
        RU_STSUMM_SYSTEM_PROMPT, RU_STSUMM_USER_PROMPT, RU_STSUMM_ASSISTANT_PROMPT

from .parsers import stsumm_custom_parse

EN_STSUMM_SUITE = AgentTaskSuite(
    system_prompt=EN_STSUMM_SYSTEM_PROMPT,
    user_prompt=EN_STSUMM_USER_PROMPT,
    assistant_prompt=EN_STSUMM_ASSISTANT_PROMPT,
    parse_answer_func=stsumm_custom_parse
)

RU_STSUMM_SUITE = AgentTaskSuite(
    system_prompt=RU_STSUMM_SYSTEM_PROMPT,
    user_prompt=RU_STSUMM_USER_PROMPT,
    assistant_prompt=RU_STSUMM_ASSISTANT_PROMPT,
    parse_answer_func=stsumm_custom_parse
)

STSUMM_SUITE_V1 = {'ru': RU_STSUMM_SUITE, 'en': EN_STSUMM_SUITE}