from typing import List, Dict
from .......utils import DialogueHistory
from ........utils.data_structs import create_id
from ........specification_model.utils import UserStory

def usgen_custom_formate(task_goal: str, base_dhistory: DialogueHistory, detailed_dhistory: DialogueHistory, us_limit: int, **kwargs) -> Dict[str, str]:
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

    us_limit_description = ""
    if us_limit > 0:
        us_limit_description = f"\n## Примечание к задаче\nСформулируй не более {us_limit} пользовательских историй."

    return {'task_goal': task_goal, 'history': general_str_dialogue, 'us_limit': us_limit_description}

def usgen_custom_postprocess(parsed_answer: List[str], **kwargs) -> List[UserStory]:
    if len(parsed_answer) < 1:
        raise ValueError
    formated_userstories = [UserStory(id=create_id(us_text), statement=us_text) for us_text in parsed_answer]
    return formated_userstories