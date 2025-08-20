from typing import List, Dict
from ........specification_model.utils import Scenario

def stitlegen_custom_formate(task_goal: str, user_story: str, accepted_scenarios: List[Scenario], 
                             declined_scenarios: List[Scenario], **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(user_story) < 1:
        raise ValueError

    if len(accepted_scenarios) > 0:
        str_accepted_scenarios = '\n'.join([f"- {scenario.title}" for scenario in accepted_scenarios])
    else:
        str_accepted_scenarios = "<|Empty|>"
    
    if len(declined_scenarios) > 0:
        str_declined_scenarios = '\n'.join([f"- {scenario.title}" for scenario in declined_scenarios])
    else:
        str_declined_scenarios = "<|Empty|>"

    return {'task_goal': task_goal, 'us': user_story, 'accepted_s': str_accepted_scenarios, 'declined_s': str_declined_scenarios}


def stitlegen_custom_postprocess(parsed_response: str, **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError
    
    return parsed_response