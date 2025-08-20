from typing import List

def rextr_custom_parse(raw_response: str, **kwargs) -> List[str]:
    if len(raw_response) < 1:
        raise ValueError

    raw_roles = list(filter(lambda item: item.startswith("-") and len(item) > 1, raw_response.split("\n")))
    roles = list(map(lambda us: us.strip("- "), raw_roles))

    return list(set(roles))