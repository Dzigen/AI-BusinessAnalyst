from typing import List
import re

def sstepsgen_custom_parse(raw_response: str, **kwargs) -> List[str]:
    raw_steps = list(filter(lambda item: len(item), raw_response.split("\n")[1:]))
    filtered_steps = []
    for step in raw_steps:
        step_info = re.match(r"^[0-9]+\.", step)
        if step_info is None:
            raise ValueError
        else:
            raw_step = step[step_info.span()[1]:]
            filtered_steps.append(raw_step.strip("\t,.; "))
    
    return filtered_steps