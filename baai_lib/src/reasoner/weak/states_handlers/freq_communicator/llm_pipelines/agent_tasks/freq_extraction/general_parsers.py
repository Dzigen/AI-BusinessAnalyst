from typing import List, Dict
from ........specification_model.utils import Scenario

def freqextr_custom_formate(task_goal: str, user_story: str, scenario: Scenario, **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(user_story) < 1:
        raise ValueError

    str_scenario = scenario.formate_to_str()

    return {'scenario': str_scenario, 'task_goal': task_goal, 'us': user_story}

def freqextr_custom_postprocess(parsed_response: List[str], **kwargs) -> List[str]:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response