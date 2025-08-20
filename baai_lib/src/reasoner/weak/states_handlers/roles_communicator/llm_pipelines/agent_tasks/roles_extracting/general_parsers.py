from typing import List, Dict

def rextr_custom_formate(task_goal: str, userstory: str, **kwargs) -> Dict[str, str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(userstory) < 1:
        raise ValueError

    return {'task_goal': task_goal, 'us': userstory}

def rextr_custom_postprocess(parsed_answer: List[str], **kwargs) -> List[str]:
    if len(parsed_answer) < 1:
        raise ValueError
    return parsed_answer