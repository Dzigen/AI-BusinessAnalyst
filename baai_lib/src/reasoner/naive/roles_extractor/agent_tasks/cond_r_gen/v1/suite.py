from .......utils import AgentTaskSuite

from .parsers import ru_condrgen_custom_parse

from .prompts import RU_CONDRGEN_SYSTEM_PROMPT, RU_CONDRGEN_USER_PROMPT, RU_CONDRGEN_ASSISTANT_PROMPT

RU_CONDRGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CONDRGEN_SYSTEM_PROMPT,
    user_prompt=RU_CONDRGEN_USER_PROMPT,
    assistant_prompt=RU_CONDRGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_condrgen_custom_parse
)

CONDRGEN_SUITE_V1 = {'ru': RU_CONDRGEN_SUITE, 'en': ...}