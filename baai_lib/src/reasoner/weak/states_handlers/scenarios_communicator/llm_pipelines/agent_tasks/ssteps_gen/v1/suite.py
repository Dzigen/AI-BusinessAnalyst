from .parsers import sstepsgen_custom_parse
from .prompts import RU_SSTEPSGEN_SYSTEM_PROMPT, RU_SSTEPSGEN_USER_PROMPT, RU_SSTEPSGEN_ASSISTANT_PROMPT
from .........utils import AgentTaskSuite

RU_SSTEPSGEN_SUITE = AgentTaskSuite(
    system_prompt=RU_SSTEPSGEN_SYSTEM_PROMPT,
    user_prompt=RU_SSTEPSGEN_USER_PROMPT,
    assistant_prompt=RU_SSTEPSGEN_ASSISTANT_PROMPT,
    parse_answer_func=sstepsgen_custom_parse
)

SSTEPSGEN_SUITE_V1 = {'ru': RU_SSTEPSGEN_SUITE, 'en': ...}