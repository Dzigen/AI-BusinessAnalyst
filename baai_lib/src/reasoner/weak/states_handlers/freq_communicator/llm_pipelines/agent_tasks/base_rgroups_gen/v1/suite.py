from .........utils import AgentTaskSuite

from .parsers import bfrggen_custom_parse

from .prompts import RU_BFRGGEN_SYSTEM_PROMPT, RU_BFRGGEN_USER_PROMPT, RU_BFRGGEN_ASSISTANT_PROMPT

RU_BFRGGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_BFRGGEN_SYSTEM_PROMPT,
    user_prompt=RU_BFRGGEN_USER_PROMPT,
    assistant_prompt=RU_BFRGGEN_ASSISTANT_PROMPT,
    parse_answer_func=bfrggen_custom_parse
)

BFRGGEN_SUITE_V1 = {'ru': RU_BFRGGEN_SUITE, 'en': ...}