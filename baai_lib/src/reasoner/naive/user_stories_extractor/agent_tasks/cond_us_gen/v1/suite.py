from .......utils import AgentTaskSuite

from .parsers import ru_condusgen_custom_parse

from .prompts import RU_CONDUSGEN_SYSTEM_PROMPT, RU_CONDUSGEN_USER_PROMPT, RU_CONDUSGEN_ASSISTANT_PROMPT

RU_CONDUSGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CONDUSGEN_SYSTEM_PROMPT,
    user_prompt=RU_CONDUSGEN_USER_PROMPT,
    assistant_prompt=RU_CONDUSGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_condusgen_custom_parse
)

CONDUSGEN_SUITE_V1 = {'ru': RU_CONDUSGEN_SUITE, 'en': ...}