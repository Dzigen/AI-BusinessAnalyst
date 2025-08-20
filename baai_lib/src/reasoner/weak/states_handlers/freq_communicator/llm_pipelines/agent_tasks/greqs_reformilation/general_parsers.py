from typing import List, Dict
from time import time
from ........specification_model.utils import FunctionalRequirement
from ........utils.data_structs import create_id

def gfrreform_custom_formate(task_goal: str, freq_title: str, freqs: List[str], **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(freq_title) < 1:
        raise ValueError
    if len(freqs) < 1:
        raise ValueError

    str_freqs = '\n'.join([f"- {freq}" for freq in freqs ])

    return {'freqs_title': freq_title, 'task_goal': task_goal, 'freqs': str_freqs}

def gfrreform_custom_postprocess(parsed_response: List[str], **kwargs) -> List[FunctionalRequirement]:
    if len(parsed_response) < 1:
        raise ValueError

    formated_freqs = [FunctionalRequirement(id=create_id(str(time())), statement=freq) for freq in parsed_response]

    return formated_freqs