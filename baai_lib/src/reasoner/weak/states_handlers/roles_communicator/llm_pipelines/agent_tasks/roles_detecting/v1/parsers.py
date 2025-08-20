def rdetect_custom_parse(raw_answer: str, **kwargs) -> bool:
    filtered_answer = raw_answer.split("\n")[0].strip(" .,;\t")
    
    formated_answer = None
    if filtered_answer == 'True':
        formated_answer = True
    elif filtered_answer == 'False':
        formated_answer = False
    else:
        raise ValueError
    
    return formated_answer