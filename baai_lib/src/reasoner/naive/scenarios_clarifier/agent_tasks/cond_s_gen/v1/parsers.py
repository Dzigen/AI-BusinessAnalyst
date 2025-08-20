def ru_condsgen_custom_parse(raw_response: str, **kwargs) -> str:
    if len(raw_response) < 1:
        raise ValueError

    scenario = raw_response.strip()

    return scenario