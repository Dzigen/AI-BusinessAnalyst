from .........utils import AgentTaskSuite

from .prompts import \
    EN_REXTR_SYSTEM_PROMPT, EN_REXTR_USER_PROMPT, EN_REXTR_ASSISTANT_PROMPT,\
        RU_REXTR_SYSTEM_PROMPT, RU_REXTR_USER_PROMPT, RU_REXTR_ASSISTANT_PROMPT

from .parsers import rextr_custom_parse

EN_REXTR_SUITE = AgentTaskSuite(
    system_prompt=EN_REXTR_SYSTEM_PROMPT,
    user_prompt=EN_REXTR_USER_PROMPT,
    assistant_prompt=EN_REXTR_ASSISTANT_PROMPT,
    parse_answer_func=rextr_custom_parse
)

RU_REXTR_SUITE = AgentTaskSuite(
    system_prompt=RU_REXTR_SYSTEM_PROMPT,
    user_prompt=RU_REXTR_USER_PROMPT,
    assistant_prompt=RU_REXTR_ASSISTANT_PROMPT,
    parse_answer_func=rextr_custom_parse
)

REXTR_SUITE_V1 = {'ru': RU_REXTR_SUITE, 'en': EN_REXTR_SUITE}