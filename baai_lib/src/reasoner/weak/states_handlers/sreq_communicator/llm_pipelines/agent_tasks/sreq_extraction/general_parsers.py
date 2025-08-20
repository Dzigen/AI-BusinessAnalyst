from typing import List, Dict
from time import time
from .......utils import DialogueHistory
from ........specification_model.utils import SystemRequirement
from ........utils.data_structs import create_id

def sreqextr_custom_formate(task_goal: str, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, sr_limit: int , **kwargs) -> Dict[str, str]:
    roles_map = {
        'user': 'Заказчик',
        'ba': 'Бизнес-аналитик'
    }

    if len(base_dhistory.sequence) < 2:
        raise ValueError
    if len(task_goal) < 1:
        raise ValueError

    general_str_dialogue = None
    base_str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", base_dhistory.sequence)))
    if len(detailed_dhistory.sequence) > 1:
        detailed_str_dialogue = "\n".join(list(map(lambda item: f"{roles_map[item.role]}: {item.text}", detailed_dhistory.sequence)))
        general_str_dialogue = f"{base_str_dialogue}\n{detailed_str_dialogue}"
    else:
        general_str_dialogue = base_str_dialogue

    sr_limit_description = ""
    if sr_limit > 0:
        sr_limit_description = f"\n## Примечание к задаче\nСформируй не более {sr_limit} системных требований."

    return {'history': general_str_dialogue, 'task_goal': task_goal, 'sr_limit': sr_limit_description}

def sreqextr_custom_postprocess(parsed_response: List[str], **kwargs) -> List[SystemRequirement]:
    if len(parsed_response) < 1:
        raise ValueError
    
    formated_sysreqs = [SystemRequirement(id=create_id(sys_req), statement=sys_req) for sys_req in parsed_response]
    return formated_sysreqs