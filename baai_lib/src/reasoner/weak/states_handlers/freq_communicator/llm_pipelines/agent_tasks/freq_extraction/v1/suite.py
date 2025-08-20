from .........utils import AgentTaskSuite

from .parsers import freqextr_custom_parse

from .prompts import RU_FREQEXTR_SYSTEM_PROMPT, RU_FREQEXTR_USER_PROMPT, RU_FREQEXTR_ASSISTANT_PROMPT

RU_FREQEXTR_SUITE = AgentTaskSuite(
    system_prompt=RU_FREQEXTR_SYSTEM_PROMPT,
    user_prompt=RU_FREQEXTR_USER_PROMPT,
    assistant_prompt=RU_FREQEXTR_ASSISTANT_PROMPT,
    parse_answer_func=freqextr_custom_parse
)

FREQEXTR_SUITE_V1 = {'ru': RU_FREQEXTR_SUITE, 'en': ...}