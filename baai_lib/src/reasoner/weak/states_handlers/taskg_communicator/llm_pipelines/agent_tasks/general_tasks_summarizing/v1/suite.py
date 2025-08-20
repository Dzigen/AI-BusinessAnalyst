from .........utils import AgentTaskSuite

from .prompts import \
    EN_GTSUMM_SYSTEM_PROMPT, EN_GTSUMM_USER_PROMPT, EN_GTSUMM_ASSISTANT_PROMPT,\
        RU_GTSUMM_SYSTEM_PROMPT, RU_GTSUMM_USER_PROMPT, RU_GTSUMM_ASSISTANT_PROMPT

from .parsers import gtsumm_custom_parse

EN_GTSUMM_SUITE = AgentTaskSuite(
    system_prompt=EN_GTSUMM_SYSTEM_PROMPT,
    user_prompt=EN_GTSUMM_USER_PROMPT,
    assistant_prompt=EN_GTSUMM_ASSISTANT_PROMPT,
    parse_answer_func=gtsumm_custom_parse
)

RU_GTSUMM_SUITE = AgentTaskSuite(
    system_prompt=RU_GTSUMM_SYSTEM_PROMPT,
    user_prompt=RU_GTSUMM_USER_PROMPT,
    assistant_prompt=RU_GTSUMM_ASSISTANT_PROMPT,
    parse_answer_func=gtsumm_custom_parse
)

GTSUMM_SUITE_V1 = {'ru': RU_GTSUMM_SUITE, 'en': EN_GTSUMM_SUITE}