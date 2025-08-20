from typing import Dict

from .......utils import DialogueHistory

def cqgen_custom_formate(base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, **kwargs) -> Dict[str, str]:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }

    if len(base_dhistory.sequence) < 2:
        raise ValueError

    general_str_dialogue = None
    base_str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", base_dhistory.sequence)))
    if len(detailed_dhistory.sequence) > 1:
        detailed_str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", detailed_dhistory.sequence)))
        general_str_dialogue = f"{base_str_dialogue}\n{detailed_str_dialogue}"
    else:
        general_str_dialogue = base_str_dialogue

    return {'history': general_str_dialogue}

def cqgen_custom_postprocess(parsed_response: str, **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response