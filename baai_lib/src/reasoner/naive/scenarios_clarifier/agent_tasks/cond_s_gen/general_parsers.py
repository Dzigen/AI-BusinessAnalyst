from typing import List
from .....utils import DialogueHistory

def condsgen_custom_formate(user_story: str, dialogue_history: DialogueHistory) -> str:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }
    str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", dialogue_history.sequence)))

    return {'user_story': user_story, 'history': str_dialogue if len(str_dialogue) else "<|Empty|>"}

def condsgen_custom_postprocess(parsed_response: str, **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response