def stitlegen_custom_parse(raw_response: str, **kwargs) -> str:
    filtered_stitle = raw_response.strip(" .,\n\t-;")
    if len(filtered_stitle) < 1:
        raise ValueError
    
    return filtered_stitle