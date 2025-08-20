from enum import Enum

class NonFuncRequirementsExtractorState(Enum):
    greetings: int = 0
    extracting: int = 1
    done: int = 2