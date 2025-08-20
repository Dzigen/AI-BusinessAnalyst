def frestrgen_custom_parse(raw_answer: str, **kwargs) -> str:
    filtered_answer = raw_answer.strip("\n .,;\t")
    if len(filtered_answer) < 1:
        raise ValueError
    
    return filtered_answer