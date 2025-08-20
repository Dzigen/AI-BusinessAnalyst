from .......utils import AgentTaskSuite

from .parsers import ru_cnonfgen_custom_parse

from .prompts import RU_CNONFGEN_SYSTEM_PROMPT, RU_CNONFGEN_USER_PROMPT, RU_CNONFGEN_ASSISTANT_PROMPT

RU_CNONFGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CNONFGEN_SYSTEM_PROMPT,
    user_prompt=RU_CNONFGEN_USER_PROMPT,
    assistant_prompt=RU_CNONFGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_cnonfgen_custom_parse
)

CNONFG_SUITE_V1 = {'ru': RU_CNONFGEN_SUITE, 'en': ...}