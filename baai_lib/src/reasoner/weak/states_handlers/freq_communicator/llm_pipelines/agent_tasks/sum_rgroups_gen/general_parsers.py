from typing import List, Dict
from ........specification_model.utils import Scenario

def sfrggen_custom_formate(task_goal: str, base_gnames: List[str], **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(base_gnames) < 1:
        raise ValueError

    str_basegnames = '\n'.join([f"- {gname}" for gname in base_gnames])

    return {'base_gnames': str_basegnames, 'task_goal': task_goal}

def sfrggen_custom_postprocess(parsed_response: List[str], **kwargs) -> List[str]:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response