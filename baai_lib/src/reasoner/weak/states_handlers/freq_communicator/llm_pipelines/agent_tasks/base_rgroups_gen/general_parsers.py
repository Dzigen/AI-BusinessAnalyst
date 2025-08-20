from typing import List, Dict
from ........specification_model.utils import Scenario

def bfrggen_custom_formate(task_goal: str, user_story: str, func_reqs: List[str], **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(user_story) < 1:
        raise ValueError
    if len(func_reqs) < 1:
        raise ValueError

    str_funcreqs = '\n'.join([f"- {freq}" for freq in func_reqs])

    return {'freqs': str_funcreqs, 'task_goal': task_goal, 'us': user_story}

def bfrggen_custom_postprocess(parsed_response: List[str], **kwargs) -> List[str]:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response