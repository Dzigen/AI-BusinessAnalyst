def ru_cnonfgen_custom_parse(raw_response: str, **kwargs) -> str:
    if len(raw_response) < 1:
        raise ValueError

    raw_nonf = list(filter(lambda item: item.startswith("-"), raw_response.split("\n")))
    nonf_reqs = list(map(lambda item: item.strip("- \n"), raw_nonf))

    return nonf_reqs