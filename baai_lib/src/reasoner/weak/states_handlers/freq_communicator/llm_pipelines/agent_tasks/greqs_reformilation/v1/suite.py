from .........utils import AgentTaskSuite

from .parsers import gfrreform_custom_parse

from .prompts import RU_GFRREFORM_SYSTEM_PROMPT, RU_GFRREFORM_USER_PROMPT, RU_GFRREFORM_ASSISTANT_PROMPT

RU_GFRREFORM_SUITE = AgentTaskSuite(
    system_prompt=RU_GFRREFORM_SYSTEM_PROMPT,
    user_prompt=RU_GFRREFORM_USER_PROMPT,
    assistant_prompt=RU_GFRREFORM_ASSISTANT_PROMPT,
    parse_answer_func=gfrreform_custom_parse
)

GFRREFORM_SUITE_V1 = {'ru': RU_GFRREFORM_SUITE, 'en': ...}