from typing import List, Dict
from .......utils import DialogueHistory

def tcls_custom_formate(dhistory: DialogueHistory, **kwargs) -> Dict[str, str]:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }

    if len(dhistory.sequence) < 2:
        raise ValueError

    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", dhistory.sequence)))

    return {'history': str_dialogue}

def tcls_custom_postprocess(formated_answer: bool, **kwargs) -> bool:
    return formated_answer