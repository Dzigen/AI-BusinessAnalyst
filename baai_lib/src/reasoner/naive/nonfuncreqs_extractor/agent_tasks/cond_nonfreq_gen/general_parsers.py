from typing import List
from copy import deepcopy
from .....utils import DialogueHistory

def cnonfgen_custom_formate(scenario: str, dialogue_history: DialogueHistory) -> str:
    if len(scenario) < 1:
        raise ValueError

    fixed_dh = deepcopy(dialogue_history.sequence)
    if len(fixed_dh) % 2 != 0:
        fixed_dh = fixed_dh[:-1]

    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }
     
    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", fixed_dh)))

    return {'scenario': scenario, 'history': str_dialogue}

def cnonfgen_custom_postprocess(parsed_response: List[str], **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response