from .........utils import AgentTaskSuite

from .parsers import srestrgen_custom_parse

from .prompts import RU_SRESTRGEN_SYSTEM_PROMPT, RU_SRESTRGEN_USER_PROMPT, RU_SRESTRGEN_ASSISTANT_PROMPT

RU_SRESTRGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_SRESTRGEN_SYSTEM_PROMPT,
    user_prompt=RU_SRESTRGEN_USER_PROMPT,
    assistant_prompt=RU_SRESTRGEN_ASSISTANT_PROMPT,
    parse_answer_func=srestrgen_custom_parse
)

SRESTRGEN_SUITE_V1 = {'ru': RU_SRESTRGEN_SUITE, 'en': ...}