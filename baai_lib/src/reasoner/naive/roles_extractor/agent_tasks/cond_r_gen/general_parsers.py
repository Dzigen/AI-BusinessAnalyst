from typing import List
from .....utils import DialogueHistory

def condrgen_custom_formate(user_story: str) -> str:
    if len(user_story) < 1:
        raise ValueError
     
    return {'user_story': user_story}

def condrgen_custom_postprocess(parsed_response: List[str], **kwargs) -> str:
    if len(parsed_response) < 1:
        raise ValueError

    return parsed_response