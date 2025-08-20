from typing import List, Dict
from time import time
from ........utils.data_structs import create_id
from ........specification_model.utils import FunctionalRestriction

def frestrgen_custom_formate(task_goal: str,  func_req: str, 
                             accepted_frestrs: List[FunctionalRestriction], 
                             declined_frestrs: List[FunctionalRestriction], **kwargs) -> Dict[str, str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(func_req) < 1:
        raise ValueError

    if len(accepted_frestrs) > 0:
        str_accepted_frestr = "\n".join([f"- {sys_restr.statement}" for sys_restr in accepted_frestrs])
    else:
        str_accepted_frestr = "<|Empty|>"

    if len(declined_frestrs) > 0:
        str_declined_frestr = "\n".join([f"- {sys_restr.statement}" for sys_restr in declined_frestrs])
    else:
        str_declined_frestr = "<|Empty|>"
        
    return {'task_goal': task_goal, 'func_req': func_req, 
        'accepted_f': str_accepted_frestr, 
        'declined_f': str_declined_frestr}

def frestrgen_custom_postprocess(parsed_response: List[str], **kwargs) -> FunctionalRestriction:
    if len(parsed_response) < 1:
        raise ValueError
    
    func_restr = FunctionalRestriction(id=create_id(parsed_response), statement=parsed_response)

    return func_restr