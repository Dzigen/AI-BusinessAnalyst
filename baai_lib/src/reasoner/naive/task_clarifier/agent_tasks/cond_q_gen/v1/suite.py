from .......utils import AgentTaskSuite

from .parsers import ru_condqgen_custom_parse

from .prompts import RU_CONDQGEN_SYSTEM_PROMPT, RU_CONDQGEN_USER_PROMPT, RU_CONDQGEN_ASSISTANT_PROMPT

RU_CONDQGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CONDQGEN_SYSTEM_PROMPT,
    user_prompt=RU_CONDQGEN_USER_PROMPT,
    assistant_prompt=RU_CONDQGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_condqgen_custom_parse
)

CONDQGEN_SUITE_V1 = {'ru': RU_CONDQGEN_SUITE, 'en': ...}