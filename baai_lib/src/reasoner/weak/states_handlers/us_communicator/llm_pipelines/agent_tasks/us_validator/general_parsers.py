from typing import List, Dict

def usvalid_custom_formate(task_goal: str, user_story: str, **kwargs) -> Dict[str, str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(user_story) < 1:
        raise ValueError
    
    return {'task_goal': task_goal, 'user_story': user_story}

def usvalid_custom_postprocess(parsed_answer: bool, **kwargs) -> bool:
    return parsed_answer