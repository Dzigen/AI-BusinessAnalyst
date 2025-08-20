from typing import List, Dict

def relgfrdetect_custom_formate(task_goal: str, current_freqt: str, other_freqts: List[str], func_reqs: List[str], **kwargs) -> Dict[str,str]:
    if len(task_goal) < 1:
        raise ValueError
    if len(current_freqt) < 1:
        raise ValueError
    if len(func_reqs) < 1:
        raise ValueError

    str_funcreqs = '\n'.join([f"- {freq}" for freq in func_reqs])
    str_other_titles = "<|Empty|>" if len(other_freqts) == 0 else "\n".join([f"- {freqt}" for freqt in other_freqts])

    return {'freqs': str_funcreqs, 'task_goal': task_goal, 'current_title': current_freqt, 'other_titles': str_other_titles}

def relgfrdetect_custom_postprocess(parsed_response: bool, **kwargs) -> bool:
    if type(parsed_response) is not bool:
        raise ValueError

    return parsed_response