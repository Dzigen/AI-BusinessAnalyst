def ru_condqgen_custom_parse(raw_response: str, **kwargs) -> str:
    if len(raw_response) < 1:
        raise ValueError

    clrf_question = raw_response.strip()

    return clrf_question