def intgrsumm_custom_parse(raw_answer: str, **kwargs) -> bool:
    if len(raw_answer) < 1:
        raise ValueError
    
    return raw_answer