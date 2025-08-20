from typing import List

def sfrggen_custom_parse(raw_response: str, **kwargs) -> List[str]:
    if len(raw_response) < 1:
        raise ValueError

    raw_gnames = list(filter(lambda item: item.startswith("-"), raw_response.split("\n")))
    g_names = list(map(lambda item: item.strip("- \n"), raw_gnames))

    return g_names