from .........utils import AgentTaskSuite

from .prompts import \
    EN_INTGRSUMM_SYSTEM_PROMPT, EN_INTGRSUMM_USER_PROMPT, EN_INTGRSUMM_ASSISTANT_PROMPT,\
        RU_INTGRSUMM_SYSTEM_PROMPT, RU_INTGRSUMM_USER_PROMPT, RU_INTGRSUMM_ASSISTANT_PROMPT

from .parsers import intgrsumm_custom_parse

EN_INTGRSUMM_SUITE = AgentTaskSuite(
    system_prompt=EN_INTGRSUMM_SYSTEM_PROMPT,
    user_prompt=EN_INTGRSUMM_USER_PROMPT,
    assistant_prompt=EN_INTGRSUMM_ASSISTANT_PROMPT,
    parse_answer_func=intgrsumm_custom_parse
)

RU_INTGRSUMM_SUITE = AgentTaskSuite(
    system_prompt=RU_INTGRSUMM_SYSTEM_PROMPT,
    user_prompt=RU_INTGRSUMM_USER_PROMPT,
    assistant_prompt=RU_INTGRSUMM_ASSISTANT_PROMPT,
    parse_answer_func=intgrsumm_custom_parse
)

INTGRSUMM_SUITE_V1 = {'ru': RU_INTGRSUMM_SUITE, 'en': EN_INTGRSUMM_SUITE}