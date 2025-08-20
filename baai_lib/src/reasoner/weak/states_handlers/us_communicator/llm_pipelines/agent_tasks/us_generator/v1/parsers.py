from typing import List

def usgen_custom_parse(raw_response: str, **kwargs) -> List[str]:
    if len(raw_response) < 1:
        raise ValueError

    raw_user_stories = list(filter(lambda item: item.startswith("-") and len(item) > 1, raw_response.split("\n")))
    user_stories = list(map(lambda us: us.strip("- "), raw_user_stories))

    return user_stories