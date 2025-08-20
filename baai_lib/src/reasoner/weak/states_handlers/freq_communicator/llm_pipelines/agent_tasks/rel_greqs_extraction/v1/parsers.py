from typing import List

def relgfrextr_custom_parse(raw_answer: str, **kwargs) -> List[int]:
    filtered_answer = raw_answer.strip("\n .,;\t")
    raw_freq_idx = list(map(lambda raw_fridx: int(raw_fridx.strip())-1, filtered_answer.split(',')))
    return raw_freq_idx