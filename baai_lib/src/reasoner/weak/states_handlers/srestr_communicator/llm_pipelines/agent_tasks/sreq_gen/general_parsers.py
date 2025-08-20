from typing import List, Dict
from time import time
from ........utils.data_structs import create_id
from ........specification_model.utils import SystemRestriction

def srestrgen_custom_formate(task_goal: str,  sys_req: str, 
                             accepted_sys_restrs: List[SystemRestriction], 
                             declined_sys_restrs: List[SystemRestriction], **kwargs) -> Dict[str, str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(sys_req) < 1:
        raise ValueError

    if len(accepted_sys_restrs) < 1:
        str_accepted_srestr = "<|Empty|>"
    else:
        str_accepted_srestr = "\n".join([f"- {sys_restr.statement}" for sys_restr in accepted_sys_restrs])
    
    if len(declined_sys_restrs) < 1:
        str_declined_srestr = "<|Empty|>"
    else:
        str_declined_srestr = "\n".join([f"- {sys_restr.statement}" for sys_restr in declined_sys_restrs])

    return {'task_goal': task_goal, 'sys_req': sys_req, 
        'accepted_s': str_accepted_srestr, 
        'declined_s': str_declined_srestr}

def srestrgen_custom_postprocess(parsed_response: List[str], **kwargs) -> SystemRestriction:
    if len(parsed_response) < 1:
        raise ValueError

    sys_restr = SystemRestriction(id=create_id(parsed_response), statement=parsed_response)
    return sys_restr