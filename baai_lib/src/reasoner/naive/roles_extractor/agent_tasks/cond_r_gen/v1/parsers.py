def ru_condrgen_custom_parse(raw_response: str, **kwargs) -> str:
    if len(raw_response) < 1:
        raise ValueError

    roles = list(map(lambda item: item.strip(), raw_response.split("\n")))

    return roles