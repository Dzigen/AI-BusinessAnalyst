from .parsers import stitlegen_custom_parse
from .prompts import RU_STITLEGEN_SYSTEM_PROMPT, RU_STITLEGEN_USER_PROMPT, RU_STITLEGEN_ASSISTANT_PROMPT
from .........utils import AgentTaskSuite

RU_STITLEGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_STITLEGEN_SYSTEM_PROMPT,
    user_prompt=RU_STITLEGEN_USER_PROMPT,
    assistant_prompt=RU_STITLEGEN_ASSISTANT_PROMPT,
    parse_answer_func=stitlegen_custom_parse
)

STITLEGEN_SUITE_V1 = {'ru': RU_STITLEGEN_SUITE, 'en': ...}