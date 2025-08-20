from typing import List, Dict
from ........specification_model.utils import Scenario

def sstepsgen_custom_formate(task_goal: str, user_story: str, scenario_title: str, **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(user_story) < 1:
        raise ValueError
    if len(scenario_title) < 1:
        raise ValueError

    return {'task_goal': task_goal, 'us': user_story, 's_title': scenario_title}


def sstepsgen_custom_postprocess(parsed_response: List[str], **kwargs) -> List[str]:
    if len(parsed_response) < 1:
        raise ValueError
    
    return parsed_response