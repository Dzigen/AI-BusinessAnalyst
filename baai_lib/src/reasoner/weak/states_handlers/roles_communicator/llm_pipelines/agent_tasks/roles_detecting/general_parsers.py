from typing import List, Dict
from .......utils import DialogueHistory

def rdetect_custom_formate(task_goal: str, userstory: str, **kwargs) -> Dict[str, str]:

    if len(task_goal) < 1:
        raise ValueError
    if len(userstory) < 1:
        raise ValueError

    return {'task_goal': task_goal, 'us': userstory}

def rdetect_custom_postprocess(formated_answer: bool, **kwargs) -> bool:
    return formated_answer