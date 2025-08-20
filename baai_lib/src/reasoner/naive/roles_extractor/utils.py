from enum import Enum

class RolesExtractorState(Enum):
    greetings: int = 0
    extracting: int = 1
    done: int = 2