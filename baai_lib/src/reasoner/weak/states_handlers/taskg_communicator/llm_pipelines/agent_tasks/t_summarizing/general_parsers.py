from typing import List, Dict
from .......utils import DialogueHistory

def stsumm_custom_formate(dhistory: DialogueHistory, task_goal: str, **kwargs) -> Dict[str, str]:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }

    if len(dhistory.sequence) < 2:
        raise ValueError
    if len(task_goal) < 1:
        raise ValueError

    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", dhistory.sequence)))

    return {'history': str_dialogue, 'task_goal': task_goal}


def stsumm_custom_postprocess(formated_answer: str, **kwargs) -> str:
    if len(formated_answer) < 1:
        raise ValueError
    
    return formated_answer