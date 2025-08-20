from typing import List

def gfrreform_custom_parse(raw_response: str, **kwargs) -> List[str]:
    if len(raw_response) < 1:
        raise ValueError

    raw_f = list(filter(lambda item: item.startswith("-"), raw_response.split("\n")))
    f_reqs = list(map(lambda item: item.strip("- \n"), raw_f))

    return f_reqs