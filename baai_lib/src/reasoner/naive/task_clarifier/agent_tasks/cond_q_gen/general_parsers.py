from typing import List
from .....utils import DialogueHistory

def condqgen_custom_formate(dialogue_history: DialogueHistory) -> str:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }
    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", dialogue_history.sequence)))

    return {'history': str_dialogue if len(str_dialogue) else "<|Empty|>"}

def condqgen_custom_postprocess(parsed_response: str, **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response