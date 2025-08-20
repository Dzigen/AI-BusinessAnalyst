from .......utils import AgentTaskSuite

from .parsers import ru_condsgen_custom_parse

from .prompts import RU_CONDSGEN_SYSTEM_PROMPT, RU_CONDSGEN_USER_PROMPT, RU_CONDSGEN_ASSISTANT_PROMPT

RU_CONDSGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CONDSGEN_SYSTEM_PROMPT,
    user_prompt=RU_CONDSGEN_USER_PROMPT,
    assistant_prompt=RU_CONDSGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_condsgen_custom_parse
)

CONDSGEN_SUITE_V1 = {'ru': RU_CONDSGEN_SUITE, 'en': ...}