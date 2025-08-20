from .......utils import AgentTaskSuite

from .parsers import ru_cfgen_custom_parse

from .prompts import RU_CFGEN_SYSTEM_PROMPT, RU_CFGEN_USER_PROMPT, RU_CFGEN_ASSISTANT_PROMPT

RU_CFGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_CFGEN_SYSTEM_PROMPT,
    user_prompt=RU_CFGEN_USER_PROMPT,
    assistant_prompt=RU_CFGEN_ASSISTANT_PROMPT,
    parse_answer_func=ru_cfgen_custom_parse
)

CFG_SUITE_V1 = {'ru': RU_CFGEN_SUITE, 'en': ...}