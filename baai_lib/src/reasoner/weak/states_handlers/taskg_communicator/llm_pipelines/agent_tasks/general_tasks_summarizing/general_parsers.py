from typing import Dict
from .......utils import DialogueHistory

def gtsumm_custom_formate(dhistory: DialogueHistory, **kwargs) -> Dict[str, str]:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }

    if len(dhistory.sequence) < 2:
        raise ValueError

    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", dhistory.sequence)))

    return {'history': str_dialogue}

def gtsumm_custom_postprocess(formated_answer: str, **kwargs) -> str:
    if len(formated_answer) < 1:
        raise ValueError
    
    return formated_answer